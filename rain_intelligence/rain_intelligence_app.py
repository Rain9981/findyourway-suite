import json
import re

import streamlit as st

from rain_intelligence.rain_engine import (
    MAX_QUESTION_COUNT,
    SOFT_QUESTION_REVIEW,
    add_consultation_entry,
    clear_consultation,
    continue_after_soft_review,
    evaluate_stopping_status,
    initialize_rain_session,
    pause_consultation,
    request_manual_stop,
    resume_consultation,
    run_final_analysis,
    run_live_analysis,
    start_consultation,
)
from rain_intelligence.rain_reports import build_rain_game_plan_pdf


SOURCE_TYPES = {
    "Client answer": "CLIENT_QUOTE",
    "James note": "JAMES_NOTE",
    "James observation": "JAMES_OBSERVATION",
    "Unknown / needs verification": "UNKNOWN",
    "Correction": "CORRECTION",
}

READINESS_LABELS = {
    "INSUFFICIENT_CONTEXT": "Insufficient context",
    "EXPLORING": "Exploring",
    "NEEDS_MORE_EVIDENCE": "Needs more evidence",
    "READY_FOR_PROVISIONAL_DIRECTION": (
        "Provisional direction available"
    ),
    "READY_FOR_RECOMMENDATION": "Ready for recommendation",
    "NOT_READY": "Not ready",
    "NO_PAID_ROUTE": "No paid route needed",
}


def _inject_styles():
    st.markdown(
        """
        <style>
        .rain-hero {
            padding: 1.25rem 1.4rem;
            border: 1px solid #d8c487;
            border-left: 6px solid #c4a24d;
            border-radius: 12px;
            background: linear-gradient(
                135deg,
                #f8f6ef 0%,
                #ffffff 72%
            );
            margin-bottom: 1rem;
        }

        .rain-kicker {
            color: #a58535;
            font-size: .78rem;
            font-weight: 800;
            letter-spacing: .12em;
            margin-bottom: .25rem;
        }

        .rain-title {
            color: #17324d;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0;
        }

        .rain-subtitle {
            color: #536273;
            margin-top: .45rem;
        }

        .rain-card {
            padding: 1rem 1.05rem;
            border: 1px solid #dfe4e8;
            border-radius: 10px;
            background: #ffffff;
            margin: .35rem 0 .8rem 0;
        }

        .rain-card-label {
            color: #a58535;
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-bottom: .35rem;
        }

        .rain-card-main {
            color: #17324d;
            font-size: 1.08rem;
            font-weight: 700;
            line-height: 1.45;
        }

        .rain-muted {
            color: #62717f;
            font-size: .9rem;
        }

        .rain-history {
            padding: .7rem .85rem;
            border-left: 3px solid #c4a24d;
            background: #f8f9fa;
            border-radius: 0 8px 8px 0;
            margin-bottom: .55rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid #e1e5e8;
            padding: .7rem .8rem;
            border-radius: 10px;
            background: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _safe_html(value):
    value = str(value or "")

    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _friendly(value):
    return (
        str(value or "")
        .replace("_", " ")
        .strip()
        .title()
    )


def _slug(value):
    clean = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        str(value or "RAIN_Client"),
    )

    return clean.strip("_") or "RAIN_Client"


def _render_string_list(
    items,
    empty_text="Nothing identified yet.",
):
    clean_items = [
        str(item).strip()
        for item in (items or [])
        if str(item).strip()
    ]

    if not clean_items:
        st.caption(empty_text)
        return

    for item in clean_items:
        st.markdown(f"- {item}")


def _render_value(value):
    if value is None or value == "" or value == [] or value == {}:
        st.caption("Not established.")
        return

    if isinstance(value, dict):
        for key, item in value.items():
            st.markdown(f"**{_friendly(key)}**")
            _render_value(item)

        return

    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                with st.container(border=True):
                    _render_value(item)
            else:
                st.markdown(f"- {item}")

        return

    if isinstance(value, bool):
        st.write("Yes" if value else "No")
        return

    st.write(value)


def _show_error(result):
    st.error(
        result.get(
            "error",
            "RAIN could not complete this request.",
        )
    )


def _run_live(consultation):
    with st.spinner(
        "RAIN is analyzing the evidence and selecting "
        "the next best question..."
    ):
        result = run_live_analysis(consultation)

    if not result.get("success"):
        _show_error(result)
        return False

    return True


def _render_setup():
    st.subheader("Start a New Consultation")

    st.caption(
        "This consultation exists only in the current browser "
        "session. It is not saved to Google Sheets and cannot "
        "be recovered after it is cleared."
    )

    with st.form("rain_new_consultation_form"):
        left, right = st.columns(2)

        with left:
            client_name = st.text_input(
                "Client name *"
            )

            business_name = st.text_input(
                "Business or organization"
            )

            client_type = st.selectbox(
                "Client type",
                [
                    "Business owner",
                    "Entrepreneur / aspiring entrepreneur",
                    "Professional",
                    "Organization / nonprofit",
                    "Consumer / individual",
                    "Existing FYW client",
                    "Other",
                ],
            )

        with right:
            industry = st.text_input(
                "Industry or field"
            )

            consultation_type = st.selectbox(
                "Consultation type",
                [
                    "Strategic direction",
                    "Business growth",
                    "Opportunity discovery",
                    "Branding and marketing",
                    "Business development",
                    "Operations and systems",
                    "Network and partnerships",
                    "Personal or professional direction",
                    "Other",
                ],
            )

        session_objective = st.text_area(
            "What should this consultation help clarify "
            "or accomplish? *",
            height=120,
            placeholder=(
                "Example: Determine the strongest realistic "
                "growth direction, what is blocking progress, "
                "and the best first move."
            ),
        )

        submitted = st.form_submit_button(
            "Start Consultation",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not client_name.strip():
            st.error(
                "Enter the client's name before starting."
            )
            return

        if not session_objective.strip():
            st.error(
                "Enter the consultation objective before starting."
            )
            return

        consultation = start_consultation(
            session_state=st.session_state,
            client_name=client_name,
            business_name=business_name,
            client_type=client_type,
            industry=industry,
            consultation_type=consultation_type,
            session_objective=session_objective,
        )

        if _run_live(consultation):
            st.rerun()


def _render_session_header(consultation):
    client = consultation.get("client", {})

    client_name = (
        client.get("name")
        or "Current client"
    )

    business_name = client.get("business_name")

    title = client_name

    if business_name:
        title += f" — {business_name}"

    st.subheader(title)

    st.caption(
        consultation.get(
            "session_objective",
            "",
        )
    )

    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )

    metric_1.metric(
        "Status",
        _friendly(
            consultation.get(
                "status",
                "DRAFT",
            )
        ),
    )

    metric_2.metric(
        "Stage",
        _friendly(
            consultation.get(
                "consultation_stage",
                "OPENING",
            )
        ),
    )

    readiness = consultation.get(
        "recommendation_readiness",
        "INSUFFICIENT_CONTEXT",
    )

    metric_3.metric(
        "Readiness",
        READINESS_LABELS.get(
            readiness,
            _friendly(readiness),
        ),
    )

    metric_4.metric(
        "Questions",
        (
            f"{consultation.get('question_count', 0)} "
            f"/ {MAX_QUESTION_COUNT}"
        ),
    )


def _render_conversation_history(consultation):
    entries = consultation.get(
        "conversation",
        [],
    )

    if not entries:
        return

    with st.expander(
        f"Consultation history ({len(entries)} entries)",
        expanded=False,
    ):
        for entry in entries:
            source = _friendly(
                entry.get(
                    "source_type",
                    "Note",
                )
            )

            stage = _friendly(
                entry.get(
                    "consultation_stage",
                    "",
                )
            )

            text = _safe_html(
                entry.get(
                    "text",
                    "",
                )
            )

            st.markdown(
                f"""
                <div class="rain-history">
                    <strong>{_safe_html(source)}</strong>
                    <span class="rain-muted">
                        · {_safe_html(stage)}
                    </span>
                    <br>
                    {text}
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_next_question(consultation):
    next_question = (
        consultation.get(
            "next_best_question",
            {},
        )
        or {}
    )

    question = next_question.get("question")

    if not question:
        return

    st.markdown(
        f"""
        <div class="rain-card">
            <div class="rain-card-label">
                RAIN's next best question
            </div>
            <div class="rain-card-main">
                {_safe_html(question)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_evidence_form(consultation):
    status = consultation.get("status")

    stopping = evaluate_stopping_status(
        consultation
    )

    if status == "PAUSED":
        st.info(
            "This consultation is paused. Resume it to add "
            "and analyze new evidence."
        )
        return

    if stopping.get("should_stop"):
        st.info(
            stopping.get(
                "reason",
                "Live questioning is complete.",
            )
        )
        return

    with st.form(
        "rain_evidence_form",
        clear_on_submit=True,
    ):
        source_label = st.selectbox(
            "Entry type",
            list(SOURCE_TYPES.keys()),
        )

        response = st.text_area(
            "Client answer or consultation note",
            height=145,
            placeholder=(
                "Enter the client's answer, your note, "
                "an observation, an unknown, or a correction."
            ),
        )

        save_column, analyze_column = st.columns(2)

        with save_column:
            save_only = st.form_submit_button(
                "Save Without Analysis",
                use_container_width=True,
            )

        with analyze_column:
            analyze = st.form_submit_button(
                "Save and Analyze",
                type="primary",
                use_container_width=True,
            )

    if save_only or analyze:
        if not response.strip():
            st.warning(
                "Enter an answer or note first."
            )
            return

        add_consultation_entry(
            consultation=consultation,
            text=response,
            source_type=SOURCE_TYPES[
                source_label
            ],
        )

        if analyze:
            if _run_live(consultation):
                st.rerun()

        else:
            st.success(
                "Saved in this temporary consultation session."
            )
            st.rerun()


def _render_conversation(consultation):
    st.markdown(
        "### Conversation and Notes"
    )

    _render_conversation_history(
        consultation
    )

    _render_next_question(
        consultation
    )

    _render_evidence_form(
        consultation
    )


def _render_intelligence(consultation):
    st.markdown(
        "### Client Intelligence"
    )

    current_summary = (
        consultation.get(
            "current_state",
            {},
        ).get(
            "summary"
        )
    )

    desired_summary = (
        consultation.get(
            "desired_state",
            {},
        ).get(
            "summary"
        )
    )

    with st.expander(
        "Current and desired state",
        expanded=True,
    ):
        st.markdown(
            "**Current state**"
        )

        st.write(
            current_summary
            or "Not established yet."
        )

        st.markdown(
            "**Desired state**"
        )

        st.write(
            desired_summary
            or "Not established yet."
        )

    categories = [
        (
            "Goals and priorities",
            consultation.get(
                "goals",
                [],
            )
            + consultation.get(
                "priorities",
                [],
            ),
        ),
        (
            "Strengths and assets",
            consultation.get(
                "strengths",
                [],
            )
            + consultation.get(
                "assets",
                [],
            ),
        ),
        (
            "Barriers and constraints",
            consultation.get(
                "barriers",
                [],
            )
            + consultation.get(
                "constraints",
                [],
            ),
        ),
        (
            "Opportunities",
            consultation.get(
                "opportunities",
                [],
            ),
        ),
        (
            "Risks and concerns",
            consultation.get(
                "risks",
                [],
            )
            + consultation.get(
                "concerns",
                [],
            ),
        ),
        (
            "Contradictions",
            consultation.get(
                "contradictions",
                [],
            ),
        ),
    ]

    expanded_sections = {
        "Strengths and assets",
        "Barriers and constraints",
    }

    for label, items in categories:
        with st.expander(
            label,
            expanded=(
                label in expanded_sections
            ),
        ):
            _render_string_list(items)

    with st.expander(
        "Possible FYW routes",
        expanded=False,
    ):
        _render_value(
            consultation.get(
                "possible_routes",
                [],
            )
        )


def _render_rain_guidance(consultation):
    st.markdown(
        "### RAIN Intelligence"
    )

    next_question = (
        consultation.get(
            "next_best_question",
            {},
        )
        or {}
    )

    reason = next_question.get("reason")

    if reason:
        st.markdown(
            "**Why this question**"
        )

        st.write(reason)

    hypotheses = consultation.get(
        "hypotheses",
        [],
    )

    with st.expander(
        "What RAIN is seeing",
        expanded=True,
    ):
        if not hypotheses:
            st.caption(
                "RAIN is still gathering evidence."
            )

        for hypothesis in hypotheses:
            confidence = hypothesis.get(
                "confidence",
                "",
            )

            statement = hypothesis.get(
                "statement",
                "",
            )

            st.markdown(
                f"**{statement}**  \n"
                f"Confidence: `{confidence}`"
            )

    signal = (
        consultation.get(
            "important_signal",
            {},
        )
        or {}
    )

    if signal.get("statement"):
        with st.expander(
            "Important signal",
            expanded=True,
        ):
            st.caption(
                _friendly(
                    signal.get(
                        "signal_type",
                        "",
                    )
                )
            )

            st.write(
                signal.get(
                    "statement",
                    "",
                )
            )

    missing = consultation.get(
        "missing_information",
        [],
    )

    with st.expander(
        "Missing information",
        expanded=bool(missing),
    ):
        if not missing:
            st.caption(
                "No decision-critical unknowns "
                "are currently listed."
            )

        for item in missing[:5]:
            st.markdown(
                "- **Needed:** "
                f"{item.get('information_needed', '')}"
            )

            if item.get("decision_impact"):
                st.caption(
                    item.get(
                        "decision_impact"
                    )
                )

    direction = (
        consultation.get(
            "possible_direction",
            {},
        )
        or {}
    )

    if direction.get("statement"):
        with st.expander(
            "Possible direction",
            expanded=True,
        ):
            st.caption(
                _friendly(
                    direction.get(
                        "status",
                        "",
                    )
                )
            )

            st.write(
                direction.get(
                    "statement",
                    "",
                )
            )

    cautions = consultation.get(
        "do_not_assume",
        [],
    )

    if cautions:
        with st.expander(
            "Do not assume",
            expanded=True,
        ):
            _render_string_list(cautions)


def _render_soft_review(
    consultation,
    stopping,
):
    question_count = consultation.get(
        "question_count",
        0,
    )

    if (
        question_count >= SOFT_QUESTION_REVIEW
        and question_count < MAX_QUESTION_COUNT
        and not stopping.get("should_stop")
    ):
        st.warning(
            f"RAIN has reached the "
            f"{SOFT_QUESTION_REVIEW}-question strategic "
            "review point. Continue only if the remaining "
            "unknowns could materially change the direction."
        )


def _retry_failed_live_analysis(
    consultation,
):
    last_error = consultation.get(
        "last_error",
        "",
    )

    next_question = (
        consultation.get(
            "next_best_question",
            {},
        )
        or {}
    ).get(
        "question"
    )

    if (
        not last_error
        or next_question
        or consultation.get("final_analysis")
    ):
        return

    st.error(last_error)

    if st.button(
        "Retry Opening Analysis",
        type="primary",
        use_container_width=True,
    ):
        if _run_live(consultation):
            st.rerun()


def _generate_final_strategy(
    consultation,
):
    with st.spinner(
        "RAIN is completing the private analysis and "
        "polished client game plan. This uses the "
        "higher-reasoning model and may take a few minutes..."
    ):
        result = run_final_analysis(
            consultation
        )

    if result.get("success"):
        st.success(
            "RAIN completed both final outputs."
        )

        st.rerun()

    else:
        _show_error(result)


def _render_controls(consultation):
    st.divider()

    status = consultation.get("status")

    stopping = evaluate_stopping_status(
        consultation
    )

    question_count = consultation.get(
        "question_count",
        0,
    )

    _retry_failed_live_analysis(
        consultation
    )

    _render_soft_review(
        consultation,
        stopping,
    )

    if (
        stopping.get("should_stop")
        and not consultation.get("last_error")
    ):
        st.success(
            stopping.get(
                "reason",
                "RAIN is ready for final analysis.",
            )
        )

    control_1, control_2, control_3 = (
        st.columns(3)
    )

    with control_1:
        if status == "ACTIVE":
            if st.button(
                "Pause Consultation",
                use_container_width=True,
            ):
                pause_consultation(
                    consultation
                )

                st.rerun()

        elif status == "PAUSED":
            if st.button(
                "Resume Consultation",
                type="primary",
                use_container_width=True,
            ):
                resume_consultation(
                    consultation
                )

                st.rerun()

    with control_2:
        if (
            status == "ACTIVE"
            and not stopping.get(
                "should_stop"
            )
        ):
            if st.button(
                "End Questions and Prepare Analysis",
                use_container_width=True,
            ):
                request_manual_stop(
                    consultation
                )

                st.rerun()

    with control_3:
        final_available = (
            consultation.get(
                "final_analysis"
            )
            is not None
        )

        can_generate = (
            stopping.get("should_stop")
            or status == "PAUSED"
        )

        has_evidence = bool(
            consultation.get(
                "conversation"
            )
        )

        if (
            not final_available
            and can_generate
            and has_evidence
            and not consultation.get(
                "last_error"
            )
        ):
            if st.button(
                "Generate Final Strategy",
                type="primary",
                use_container_width=True,
            ):
                _generate_final_strategy(
                    consultation
                )

    if (
        question_count >= SOFT_QUESTION_REVIEW
        and question_count < MAX_QUESTION_COUNT
        and consultation.get(
            "manual_stop_requested"
        )
        and consultation.get(
            "final_analysis"
        )
        is None
    ):
        if st.button(
            "Return to Questioning"
        ):
            continue_after_soft_review(
                consultation
            )

            st.rerun()


def _render_internal_analysis(
    final_analysis,
    consultation,
):
    st.warning(
        "Internal only: this analysis may include hypotheses, "
        "risks, route deliberation, and items that should not "
        "be handed directly to the client."
    )

    sections = [
        (
            "Executive Interpretation",
            "executive_interpretation",
        ),
        (
            "Current State",
            "current_state",
        ),
        (
            "Desired State",
            "desired_state",
        ),
        (
            "Underlying Goal Hypotheses",
            "underlying_goal_hypotheses",
        ),
        (
            "Strengths and Assets",
            "strengths_and_assets",
        ),
        (
            "Barriers and Constraints",
            "barriers_and_constraints",
        ),
        (
            "Risks",
            "risks",
        ),
        (
            "Contradictions",
            "contradictions",
        ),
        (
            "Opportunity Signals",
            "opportunity_signals",
        ),
        (
            "Premature Opportunities",
            "premature_opportunities",
        ),
        (
            "Readiness",
            "readiness",
        ),
        (
            "Routes Considered",
            "routes_considered",
        ),
        (
            "Primary Direction",
            "primary_direction",
        ),
        (
            "Recommended FYW Route",
            "recommended_fyw_route",
        ),
        (
            "Secondary Route",
            "secondary_route",
        ),
        (
            "Recommended Sequence",
            "recommended_sequence",
        ),
        (
            "What Not to Recommend",
            "what_not_to_recommend",
        ),
        (
            "Immediate Next Action",
            "immediate_next_action",
        ),
        (
            "Overall Confidence",
            "overall_confidence",
        ),
    ]

    expanded_sections = {
        "executive_interpretation",
        "primary_direction",
    }

    for label, key in sections:
        with st.expander(
            label,
            expanded=(
                key in expanded_sections
            ),
        ):
            _render_value(
                final_analysis.get(key)
            )

    client_name = (
        consultation.get(
            "client",
            {},
        ).get(
            "name"
        )
        or "Client"
    )

    st.download_button(
        "Download Private Analysis JSON",
        data=json.dumps(
            final_analysis,
            indent=2,
        ),
        file_name=(
            f"RAIN_Internal_"
            f"{_slug(client_name)}.json"
        ),
        mime="application/json",
    )


def _render_client_game_plan(
    game_plan,
    consultation,
):
    st.success(
        "This is the client-facing version. Private hypotheses "
        "and internal route deliberation are kept out of the PDF."
    )

    st.subheader(
        game_plan.get(
            "report_title",
            "RAIN Strategic Game Plan",
        )
    )

    st.write(
        game_plan.get(
            "strategic_snapshot",
            "",
        )
    )

    try:
        pdf_buffer = build_rain_game_plan_pdf(
            game_plan
        )

        pdf_bytes = (
            pdf_buffer.getvalue()
        )

    except Exception as error:
        st.error(
            "The strategy was generated, but the PDF "
            f"could not be built: {error}"
        )

        pdf_bytes = None

    client_name = (
        consultation.get(
            "client",
            {},
        ).get(
            "name"
        )
        or "Client"
    )

    if pdf_bytes:
        st.download_button(
            "Download Polished Client PDF",
            data=pdf_bytes,
            file_name=(
                "RAIN_Strategic_Game_Plan_"
                f"{_slug(client_name)}.pdf"
            ),
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

    with st.expander(
        "Preview client game-plan content",
        expanded=False,
    ):
        _render_value(game_plan)


def _render_final_outputs(
    consultation,
):
    final_analysis = consultation.get(
        "final_analysis"
    )

    game_plan = consultation.get(
        "client_game_plan"
    )

    if not final_analysis and not game_plan:
        return

    st.divider()

    st.header(
        "Completed RAIN Outputs"
    )

    internal_tab, client_tab = st.tabs(
        [
            "James's Private Analysis",
            "Client Strategic Game Plan",
        ]
    )

    with internal_tab:
        if final_analysis:
            _render_internal_analysis(
                final_analysis,
                consultation,
            )
        else:
            st.info(
                "The private analysis is not available."
            )

    with client_tab:
        if game_plan:
            _render_client_game_plan(
                game_plan,
                consultation,
            )
        else:
            st.info(
                "The client game plan is not available."
            )


def _render_usage(consultation):
    usage = consultation.get(
        "usage",
        {},
    )

    with st.expander(
        "Temporary API usage for this consultation",
        expanded=False,
    ):
        col_1, col_2, col_3, col_4 = (
            st.columns(4)
        )

        col_1.metric(
            "Live calls",
            usage.get(
                "live_calls",
                0,
            ),
        )

        col_2.metric(
            "Final calls",
            usage.get(
                "final_calls",
                0,
            ),
        )

        col_3.metric(
            "Input tokens",
            f"{usage.get('input_tokens', 0):,}",
        )

        col_4.metric(
            "Output tokens",
            f"{usage.get('output_tokens', 0):,}",
        )

        st.caption(
            "Usage is shown only for this active "
            "Streamlit session and is not saved by RAIN."
        )


def _render_reset():
    with st.expander(
        "Clear this temporary consultation",
        expanded=False,
    ):
        st.warning(
            "Clearing removes the consultation, analysis, "
            "and PDF from this browser session. RAIN cannot "
            "recover them."
        )

        confirmed = st.checkbox(
            "I have downloaded anything I need and understand "
            "this cannot be undone.",
            key="rain_clear_confirmed",
        )

        if st.button(
            "Clear Consultation",
            disabled=not confirmed,
        ):
            clear_consultation(
                st.session_state
            )

            st.session_state.pop(
                "rain_clear_confirmed",
                None,
            )

            st.rerun()


def _render_workspace(
    consultation,
):
    _render_session_header(
        consultation
    )

    (
        conversation_column,
        intelligence_column,
        rain_column,
    ) = st.columns(
        [1.4, 1.0, 1.0],
        gap="large",
    )

    with conversation_column:
        _render_conversation(
            consultation
        )

    with intelligence_column:
        _render_intelligence(
            consultation
        )

    with rain_column:
        _render_rain_guidance(
            consultation
        )

    _render_controls(
        consultation
    )

    _render_final_outputs(
        consultation
    )

    _render_usage(
        consultation
    )

    _render_reset()


def run():
    _inject_styles()

    st.markdown(
        """<div class="rain-hero">
<div class="rain-kicker">FIND YOUR WAY NMC</div>
<div class="rain-title">RAIN Intelligence</div>
<div class="rain-subtitle">Live strategic consultation support, deeper analysis, and a polished client game plan.</div>
</div>""",
        unsafe_allow_html=True,
    )

    st.caption(
        "RAIN assists James's judgment; it does not "
        "automatically sell a service or replace legal, "
        "financial, medical, licensing, or other qualified "
        "professional advice."
    )

    consultation = initialize_rain_session(
        st.session_state
    )

    if consultation.get("status") == "DRAFT":
        _render_setup()

    else:
        _render_workspace(
            consultation
        )