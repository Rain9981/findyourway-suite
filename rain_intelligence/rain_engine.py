"""
RAIN Intelligence temporary consultation engine.

This module:
- manages Streamlit session-state consultations
- adds consultation notes and client answers
- applies structured live RAIN results
- counts generated questions
- enforces soft and hard stopping rules
- generates final internal and client-facing analyses
- does not use Google Sheets or permanent storage
"""

from datetime import datetime

from backend.rain_openai import (
    RainOpenAIError,
    add_usage_to_session,
    analyze_live_consultation,
    generate_client_game_plan,
    generate_final_internal_analysis,
)

from rain_intelligence.rain_schemas import (
    create_conversation_entry,
    fresh_consultation,
)


RAIN_SESSION_KEY = "rain_consultation"

SOFT_QUESTION_REVIEW = 10
MAX_QUESTION_COUNT = 18

STOP_READINESS_STATUSES = {
    "READY_FOR_RECOMMENDATION",
    "NOT_READY",
    "NO_PAID_ROUTE",
}


def initialize_rain_session(session_state):
    """
    Ensure a temporary RAIN consultation exists.
    """

    if RAIN_SESSION_KEY not in session_state:
        session_state[RAIN_SESSION_KEY] = fresh_consultation()

    consultation = session_state[RAIN_SESSION_KEY]

    consultation.setdefault("question_count", 0)
    consultation.setdefault("soft_review_required", False)
    consultation.setdefault("manual_stop_requested", False)
    consultation.setdefault("stop_reason", "")
    consultation.setdefault("last_error", "")
    consultation.setdefault("james_override", "")

    return consultation


def start_consultation(
    session_state,
    client_name,
    business_name,
    client_type,
    industry,
    consultation_type,
    session_objective,
):
    """
    Start a new temporary consultation.
    """

    consultation = fresh_consultation()

    consultation["status"] = "ACTIVE"

    consultation["client"] = {
        "name": str(client_name).strip(),
        "business_name": str(business_name).strip(),
        "client_type": str(client_type).strip(),
        "industry": str(industry).strip(),
        "consultation_type": str(consultation_type).strip(),
    }

    consultation["session_objective"] = str(
        session_objective
    ).strip()

    consultation["question_count"] = 0
    consultation["soft_review_required"] = False
    consultation["manual_stop_requested"] = False
    consultation["stop_reason"] = ""
    consultation["last_error"] = ""
    consultation["james_override"] = ""

    consultation["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    session_state[RAIN_SESSION_KEY] = consultation

    return consultation


def clear_consultation(session_state):
    """
    Permanently clear the current in-memory consultation.

    Since RAIN V1 has no permanent storage, the cleared information
    cannot be recovered from RAIN.
    """

    session_state[RAIN_SESSION_KEY] = fresh_consultation()

    return session_state[RAIN_SESSION_KEY]


def pause_consultation(consultation):
    """
    Pause the current consultation within the active Streamlit session.
    """

    consultation["status"] = "PAUSED"
    consultation["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return consultation


def resume_consultation(consultation):
    """
    Resume a paused consultation during the same Streamlit session.
    """

    consultation["status"] = "ACTIVE"
    consultation["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return consultation


def add_consultation_entry(
    consultation,
    text,
    source_type="JAMES_NOTE",
):
    """
    Add one note, client quote, observation, unknown, or correction.
    """

    clean_text = str(text).strip()

    if not clean_text:
        return consultation

    entry = create_conversation_entry(
        text=clean_text,
        source_type=source_type,
        consultation_stage=consultation.get(
            "consultation_stage",
            "OPENING",
        ),
    )

    consultation.setdefault("conversation", [])
    consultation["conversation"].append(entry)

    consultation["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return consultation


def _normalize_string(value):
    """
    Create a consistent comparison value.
    """

    return " ".join(
        str(value).strip().lower().split()
    )


def _merge_unique(existing_items, new_items):
    """
    Merge string lists without adding duplicates.
    """

    existing_items = existing_items or []
    new_items = new_items or []

    merged = list(existing_items)

    known_values = {
        _normalize_string(item)
        for item in merged
        if str(item).strip()
    }

    for item in new_items:
        clean_item = str(item).strip()

        if not clean_item:
            continue

        normalized = _normalize_string(clean_item)

        if normalized not in known_values:
            merged.append(clean_item)
            known_values.add(normalized)

    return merged


def _question_is_new(consultation, new_question):
    """
    Prevent a repeated API run from increasing the question count
    for the same question.
    """

    new_question = str(new_question or "").strip()

    if not new_question:
        return False

    previous_question = consultation.get(
        "next_best_question",
        {},
    ).get(
        "question",
        "",
    )

    return (
        _normalize_string(new_question)
        != _normalize_string(previous_question)
    )


def apply_live_result(
    consultation,
    live_data,
):
    """
    Apply a schema-validated live RAIN response to session state.
    """

    new_question = live_data.get(
        "next_best_question",
        {},
    ).get(
        "question",
        "",
    )

    if _question_is_new(
        consultation,
        new_question,
    ):
        consultation["question_count"] = (
            consultation.get("question_count", 0) + 1
        )

    consultation["consultation_stage"] = live_data.get(
        "consultation_stage",
        consultation.get(
            "consultation_stage",
            "OPENING",
        ),
    )

    consultation["recommendation_readiness"] = live_data.get(
        "recommendation_readiness",
        consultation.get(
            "recommendation_readiness",
            "EXPLORING",
        ),
    )

    consultation["next_best_question"] = live_data.get(
        "next_best_question",
        {
            "question": "",
            "question_type": "",
            "reason": "",
        },
    )

    consultation["hypotheses"] = live_data.get(
        "what_rain_is_seeing",
        [],
    )

    consultation["important_signal"] = live_data.get(
        "important_signal",
        {
            "signal_type": "NONE",
            "statement": "",
        },
    )

    consultation["missing_information"] = live_data.get(
        "missing_information",
        [],
    )

    consultation["possible_direction"] = live_data.get(
        "possible_direction",
        {
            "status": "NONE",
            "statement": "",
        },
    )

    consultation["do_not_assume"] = live_data.get(
        "do_not_assume",
        [],
    )

    state_updates = live_data.get(
        "state_updates",
        {},
    )

    current_summary = state_updates.get(
        "current_state_summary",
        "",
    ).strip()

    if current_summary:
        consultation["current_state"]["summary"] = (
            current_summary
        )

    desired_summary = state_updates.get(
        "desired_state_summary",
        "",
    ).strip()

    if desired_summary:
        consultation["desired_state"]["summary"] = (
            desired_summary
        )

    list_fields = [
        "goals",
        "priorities",
        "strengths",
        "assets",
        "competencies",
        "barriers",
        "constraints",
        "concerns",
        "motivations",
        "opportunities",
        "risks",
        "contradictions",
    ]

    for field in list_fields:
        consultation[field] = _merge_unique(
            consultation.get(field, []),
            state_updates.get(field, []),
        )

    # Route assessments represent RAIN's current view.
    # Replace them rather than accumulating old route judgments.
    consultation["possible_routes"] = state_updates.get(
        "possible_routes",
        consultation.get("possible_routes", []),
    )

    consultation["routes_ruled_out"] = state_updates.get(
        "routes_ruled_out",
        consultation.get("routes_ruled_out", []),
    )

    consultation["soft_review_required"] = (
        consultation.get("question_count", 0)
        >= SOFT_QUESTION_REVIEW
    )

    consultation["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    consultation["last_error"] = ""

    return consultation


def evaluate_stopping_status(consultation):
    """
    Determine whether live questioning should stop.

    Returns a dictionary so the interface can explain the result.
    """

    question_count = consultation.get(
        "question_count",
        0,
    )

    readiness = consultation.get(
        "recommendation_readiness",
        "INSUFFICIENT_CONTEXT",
    )

    next_question = consultation.get(
        "next_best_question",
        {},
    ).get(
        "question",
        "",
    )

    if consultation.get("manual_stop_requested", False):
        return {
            "should_stop": True,
            "reason": (
                "James ended the questioning and requested "
                "the final strategic analysis."
            ),
            "trigger": "MANUAL_STOP",
        }

    if question_count >= MAX_QUESTION_COUNT:
        return {
            "should_stop": True,
            "reason": (
                f"RAIN reached the {MAX_QUESTION_COUNT}-question "
                "safety limit and will prepare the strongest "
                "analysis supported by the available evidence."
            ),
            "trigger": "MAX_QUESTION_LIMIT",
        }

    if readiness in STOP_READINESS_STATUSES:
        readiness_reasons = {
            "READY_FOR_RECOMMENDATION": (
                "RAIN has enough evidence to prepare a strategic "
                "recommendation."
            ),
            "NOT_READY": (
                "RAIN has enough evidence to explain why the client "
                "is not ready and what prerequisite should happen first."
            ),
            "NO_PAID_ROUTE": (
                "RAIN has enough evidence to provide a useful next "
                "move without recommending a paid FYW route."
            ),
        }

        return {
            "should_stop": True,
            "reason": readiness_reasons[readiness],
            "trigger": readiness,
        }

    if not str(next_question or "").strip():
        return {
            "should_stop": True,
            "reason": (
                "RAIN determined that another question would not "
                "materially improve the immediate recommendation."
            ),
            "trigger": "NO_NEXT_QUESTION",
        }

    if question_count >= SOFT_QUESTION_REVIEW:
        return {
            "should_stop": False,
            "reason": (
                "RAIN has reached the strategic review point. "
                "James should decide whether the remaining unknowns "
                "justify additional questions."
            ),
            "trigger": "SOFT_REVIEW",
        }

    return {
        "should_stop": False,
        "reason": (
            "Additional questioning can still materially improve "
            "the strategic analysis."
        ),
        "trigger": "CONTINUE",
    }


def request_manual_stop(consultation):
    """
    Allow James to stop questioning at any time.
    """

    consultation["manual_stop_requested"] = True

    consultation["stop_reason"] = (
        "James manually ended the questioning."
    )

    consultation["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return consultation


def continue_after_soft_review(consultation):
    """
    Allow James to continue after the ten-question review point.
    """

    consultation["soft_review_required"] = False
    consultation["manual_stop_requested"] = False
    consultation["stop_reason"] = ""

    consultation["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return consultation


def run_live_analysis(consultation):
    """
    Call the live RAIN model and safely apply its response.
    """

    consultation["last_error"] = ""

    try:
        result = analyze_live_consultation(
            consultation=consultation,
        )

        apply_live_result(
            consultation=consultation,
            live_data=result["data"],
        )

        add_usage_to_session(
            consultation=consultation,
            usage=result["usage"],
            call_type="live",
        )

        stopping_status = evaluate_stopping_status(
            consultation
        )

        consultation["stop_reason"] = (
            stopping_status["reason"]
            if stopping_status["should_stop"]
            else ""
        )

        return {
            "success": True,
            "consultation": consultation,
            "stopping_status": stopping_status,
            "model": result["model"],
            "usage": result["usage"],
        }

    except RainOpenAIError as error:
        consultation["last_error"] = str(error)

        return {
            "success": False,
            "consultation": consultation,
            "error": str(error),
        }

    except Exception as error:
        message = (
            "RAIN encountered an unexpected live-analysis error: "
            f"{error}"
        )

        consultation["last_error"] = message

        return {
            "success": False,
            "consultation": consultation,
            "error": message,
        }


def run_final_analysis(consultation):
    """
    Generate:
    1. James's private final strategic analysis
    2. The client's Strategic Game Plan

    Both outputs remain temporary.
    """

    consultation["last_error"] = ""

    try:
        internal_result = generate_final_internal_analysis(
            consultation=consultation,
        )

        consultation["final_analysis"] = internal_result[
            "data"
        ]

        add_usage_to_session(
            consultation=consultation,
            usage=internal_result["usage"],
            call_type="final",
        )

        client_result = generate_client_game_plan(
            consultation=consultation,
            final_internal_analysis=consultation[
                "final_analysis"
            ],
        )

        consultation["client_game_plan"] = client_result[
            "data"
        ]

        add_usage_to_session(
            consultation=consultation,
            usage=client_result["usage"],
            call_type="final",
        )

        consultation["status"] = "ANALYSIS_COMPLETE"
        consultation["consultation_stage"] = "CLOSE"

        consultation["updated_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

        return {
            "success": True,
            "consultation": consultation,
            "internal_model": internal_result["model"],
            "client_model": client_result["model"],
        }

    except RainOpenAIError as error:
        consultation["last_error"] = str(error)

        return {
            "success": False,
            "consultation": consultation,
            "error": str(error),
        }

    except Exception as error:
        message = (
            "RAIN encountered an unexpected final-analysis error: "
            f"{error}"
        )

        consultation["last_error"] = message

        return {
            "success": False,
            "consultation": consultation,
            "error": message,
        }