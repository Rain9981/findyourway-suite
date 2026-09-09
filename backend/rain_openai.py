"""
OpenAI Responses API connection for RAIN Intelligence.

This module:
- uses a faster model for live consultation assistance
- uses a higher-reasoning model for final analysis
- enforces strict JSON schemas
- records usage only in the current Streamlit session
- does not save anything to Google Sheets
"""

import json

import streamlit as st
from openai import OpenAI

from backend.ai_config import (
    RAIN_FINAL_MODEL,
    RAIN_LIVE_MODEL,
)

from rain_intelligence.rain_prompts import (
    build_client_game_plan_prompt,
    build_final_internal_analysis_prompt,
    build_live_consultation_prompt,
)

from rain_intelligence.rain_schemas import (
    CLIENT_GAME_PLAN_SCHEMA,
    FINAL_ANALYSIS_SCHEMA,
    LIVE_RESPONSE_SCHEMA,
)


class RainOpenAIError(Exception):
    """
    User-safe RAIN API exception.
    """

    pass


def get_rain_client():
    """
    Create the OpenAI client using the existing Streamlit secret.
    """

    try:
        api_key = st.secrets["openai"]["api_key"]
    except Exception as error:
        raise RainOpenAIError(
            "The OpenAI API key is missing from Streamlit secrets."
        ) from error

    if not api_key:
        raise RainOpenAIError(
            "The OpenAI API key is empty."
        )

    return OpenAI(api_key=api_key)


def _usage_value(usage, name):
    """
    Safely read a token value from the API usage object.
    """

    if usage is None:
        return 0

    if isinstance(usage, dict):
        return int(usage.get(name, 0) or 0)

    return int(getattr(usage, name, 0) or 0)


def _extract_usage(response):
    """
    Return temporary usage information from one API response.
    """

    usage = getattr(response, "usage", None)

    return {
        "input_tokens": _usage_value(
            usage,
            "input_tokens",
        ),
        "output_tokens": _usage_value(
            usage,
            "output_tokens",
        ),
        "total_tokens": _usage_value(
            usage,
            "total_tokens",
        ),
    }


def _parse_structured_output(response, required_keys):
    """
    Convert structured response text into a Python dictionary.
    """

    output_text = getattr(response, "output_text", None)

    if not output_text:
        raise RainOpenAIError(
            "RAIN returned an empty response."
        )

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError as error:
        raise RainOpenAIError(
            "RAIN returned output that could not be read as structured data."
        ) from error

    if not isinstance(parsed, dict):
        raise RainOpenAIError(
            "RAIN returned an unexpected response structure."
        )

    missing_keys = [
        key
        for key in required_keys
        if key not in parsed
    ]

    if missing_keys:
        raise RainOpenAIError(
            "RAIN's response is missing required information: "
            + ", ".join(missing_keys)
        )

    return parsed


def _structured_response(
    model,
    prompt,
    schema_name,
    schema,
    required_keys,
    max_output_tokens,
    reasoning_effort=None,
):
    """
    Make one schema-constrained Responses API call.
    """

    client = get_rain_client()

    request = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "strict": True,
                "schema": schema,
            }
        },
        "max_output_tokens": max_output_tokens,
    }

    if reasoning_effort:
        request["reasoning"] = {
            "effort": reasoning_effort,
        }

    try:
        response = client.responses.create(**request)

    except Exception as error:
        error_text = str(error)

        if "model" in error_text.lower():
            raise RainOpenAIError(
                f"RAIN could not use the configured model '{model}'. "
                "Confirm that this model is available to your OpenAI API project."
            ) from error

        if "api key" in error_text.lower():
            raise RainOpenAIError(
                "The OpenAI API key was rejected."
            ) from error

        if "rate" in error_text.lower():
            raise RainOpenAIError(
                "RAIN temporarily reached an API usage or rate limit. "
                "Wait briefly and try again."
            ) from error

        raise RainOpenAIError(
            f"RAIN could not complete the AI request: {error}"
        ) from error

    parsed = _parse_structured_output(
        response=response,
        required_keys=required_keys,
    )

    return {
        "data": parsed,
        "usage": _extract_usage(response),
        "model": model,
        "response_id": getattr(response, "id", ""),
    }


def analyze_live_consultation(consultation):
    """
    Use the lower-cost model for live analysis and the next question.
    """

    prompt = build_live_consultation_prompt(
        consultation=consultation,
    )

    required_keys = [
        "consultation_stage",
        "recommendation_readiness",
        "next_best_question",
        "what_rain_is_seeing",
        "important_signal",
        "missing_information",
        "possible_direction",
        "do_not_assume",
        "state_updates",
    ]

    return _structured_response(
        model=RAIN_LIVE_MODEL,
        prompt=prompt,
        schema_name="rain_live_consultation",
        schema=LIVE_RESPONSE_SCHEMA,
        required_keys=required_keys,
        max_output_tokens=3500,
    )


def generate_final_internal_analysis(consultation):
    """
    Use the higher-reasoning model for James's private final analysis.
    """

    prompt = build_final_internal_analysis_prompt(
        consultation=consultation,
    )

    required_keys = [
        "consultation_objective",
        "executive_interpretation",
        "current_state",
        "desired_state",
        "underlying_goal_hypotheses",
        "strengths_and_assets",
        "barriers_and_constraints",
        "risks",
        "contradictions",
        "opportunity_signals",
        "premature_opportunities",
        "readiness",
        "routes_considered",
        "primary_direction",
        "recommended_fyw_route",
        "secondary_route",
        "recommended_sequence",
        "what_not_to_recommend",
        "immediate_next_action",
        "overall_confidence",
    ]

    return _structured_response(
        model=RAIN_FINAL_MODEL,
        prompt=prompt,
        schema_name="rain_final_internal_analysis",
        schema=FINAL_ANALYSIS_SCHEMA,
        required_keys=required_keys,
        max_output_tokens=8000,
        reasoning_effort="high",
    )


def generate_client_game_plan(
    consultation,
    final_internal_analysis,
):
    """
    Use the higher-reasoning model to create the client-facing game plan.
    """

    prompt = build_client_game_plan_prompt(
        consultation=consultation,
        final_internal_analysis=final_internal_analysis,
    )

    required_keys = [
        "report_title",
        "client_name",
        "business_name",
        "strategic_snapshot",
        "current_position",
        "desired_outcome",
        "core_challenges",
        "strengths_and_assets",
        "primary_opportunity",
        "strategic_direction",
        "immediate_priorities",
        "step_by_step_game_plan",
        "first_30_days",
        "days_31_to_60",
        "days_61_to_90",
        "recommended_fyw_support",
        "risks_and_things_to_avoid",
        "final_strategic_guidance",
    ]

    return _structured_response(
        model=RAIN_FINAL_MODEL,
        prompt=prompt,
        schema_name="rain_client_game_plan",
        schema=CLIENT_GAME_PLAN_SCHEMA,
        required_keys=required_keys,
        max_output_tokens=8000,
        reasoning_effort="high",
    )


def add_usage_to_session(
    consultation,
    usage,
    call_type,
):
    """
    Add token usage to the current temporary consultation.

    Nothing is permanently saved.
    """

    if "usage" not in consultation:
        consultation["usage"] = {
            "live_calls": 0,
            "final_calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
        }

    consultation["usage"]["input_tokens"] += int(
        usage.get("input_tokens", 0)
    )

    consultation["usage"]["output_tokens"] += int(
        usage.get("output_tokens", 0)
    )

    if call_type == "live":
        consultation["usage"]["live_calls"] += 1

    elif call_type == "final":
        consultation["usage"]["final_calls"] += 1

    return consultation