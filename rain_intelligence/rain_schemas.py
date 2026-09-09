"""
RAIN Intelligence data structures and JSON schemas.

RAIN V1 stores information only in Streamlit session state.
Nothing in this module writes to Google Sheets or permanent storage.
"""

from copy import deepcopy
from datetime import datetime
from uuid import uuid4


# =========================================================
# CONSULTATION STAGES
# =========================================================

CONSULTATION_STAGES = [
    "OPENING",
    "CURRENT_STATE",
    "DESIRED_STATE",
    "GAP_DISCOVERY",
    "ASSET_CAPACITY",
    "OPPORTUNITY_READINESS",
    "RECOMMENDATION",
    "CLOSE",
]


# =========================================================
# RECOMMENDATION READINESS
# =========================================================

READINESS_STATUSES = [
    "INSUFFICIENT_CONTEXT",
    "EXPLORING",
    "NEEDS_MORE_EVIDENCE",
    "READY_FOR_PROVISIONAL_DIRECTION",
    "READY_FOR_RECOMMENDATION",
    "NOT_READY",
    "NO_PAID_ROUTE",
]


# =========================================================
# QUESTION TYPES
# =========================================================

QUESTION_TYPES = [
    "CLARIFICATION",
    "EVIDENCE",
    "CONTRADICTION",
    "PRIORITY",
    "CONSTRAINT",
    "MOTIVATION",
    "READINESS",
    "OPPORTUNITY",
    "CONSEQUENCE",
    "DECISION",
]


# =========================================================
# CONFIDENCE LEVELS
# =========================================================

CONFIDENCE_LEVELS = [
    "LOW",
    "MEDIUM",
    "HIGH",
]


# =========================================================
# ROUTE STATUSES
# =========================================================

ROUTE_STATUSES = [
    "CONSIDER",
    "PROVISIONAL",
    "RECOMMEND",
    "DEFER",
    "RULE_OUT",
    "SPECIALIST_REVIEW",
]


# =========================================================
# INITIAL CONSULTATION STATE
# =========================================================

def create_empty_consultation():
    """
    Create a fresh temporary RAIN consultation.

    This object is intended to live inside st.session_state.
    It is not written to Google Sheets or permanent storage.
    """

    now = datetime.now().isoformat(timespec="seconds")

    return {
        "consultation_id": str(uuid4()),
        "created_at": now,
        "updated_at": now,
        "status": "DRAFT",
        "consultation_stage": "OPENING",
        "recommendation_readiness": "INSUFFICIENT_CONTEXT",

        "client": {
            "name": "",
            "business_name": "",
            "client_type": "",
            "industry": "",
            "consultation_type": "",
        },

        "session_objective": "",

        "conversation": [],

        "current_state": {
            "summary": "",
            "evidence": [],
            "confidence": "LOW",
        },

        "desired_state": {
            "summary": "",
            "outcomes": [],
            "time_horizon": "",
            "success_measures": [],
            "confidence": "LOW",
        },

        "goals": [],
        "priorities": [],
        "strengths": [],
        "assets": [],
        "competencies": [],
        "barriers": [],
        "constraints": [],
        "concerns": [],
        "motivations": [],
        "opportunities": [],
        "risks": [],
        "missing_information": [],
        "contradictions": [],
        "hypotheses": [],
        "possible_routes": [],
        "routes_ruled_out": [],

        "next_best_question": {
            "question": "",
            "question_type": "",
            "reason": "",
        },

        "important_signal": {
            "signal_type": "",
            "statement": "",
        },

        "possible_direction": {
            "status": "NONE",
            "statement": "",
        },

        "do_not_assume": [],

        "recommendation": {
            "primary_direction": "",
            "recommended_fyw_route": "",
            "secondary_route": "",
            "sequence": [],
            "rationale": "",
            "prerequisites": [],
            "what_not_to_recommend": [],
            "immediate_next_action": "",
            "owner": "",
            "target_date": "",
        },

        "final_analysis": None,
        "client_game_plan": None,
        "pdf_buffer": None,

        "usage": {
            "live_calls": 0,
            "final_calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
        },
    }


def fresh_consultation():
    """
    Return a fully independent consultation dictionary.
    """

    return deepcopy(create_empty_consultation())


# =========================================================
# CONVERSATION ENTRY
# =========================================================

def create_conversation_entry(
    text,
    source_type="JAMES_NOTE",
    consultation_stage="OPENING",
):
    """
    Create one timestamped consultation entry.

    source_type examples:
    - JAMES_NOTE
    - CLIENT_QUOTE
    - JAMES_OBSERVATION
    - UNKNOWN
    - CORRECTION
    """

    return {
        "entry_id": str(uuid4()),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "source_type": source_type,
        "consultation_stage": consultation_stage,
        "text": str(text).strip(),
    }


# =========================================================
# LIVE RAIN STRUCTURED OUTPUT SCHEMA
# =========================================================

LIVE_RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "consultation_stage": {
            "type": "string",
            "enum": CONSULTATION_STAGES,
        },
        "recommendation_readiness": {
            "type": "string",
            "enum": READINESS_STATUSES,
        },
        "next_best_question": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "question": {
                    "type": ["string", "null"],
                },
                "question_type": {
                    "type": ["string", "null"],
                    "enum": QUESTION_TYPES + [None],
                },
                "reason": {
                    "type": ["string", "null"],
                },
            },
            "required": [
                "question",
                "question_type",
                "reason",
            ],
        },
        "what_rain_is_seeing": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "statement": {
                        "type": "string",
                    },
                    "confidence": {
                        "type": "string",
                        "enum": CONFIDENCE_LEVELS,
                    },
                    "evidence": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                    "counterevidence": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                },
                "required": [
                    "statement",
                    "confidence",
                    "evidence",
                    "counterevidence",
                ],
            },
        },
        "important_signal": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "signal_type": {
                    "type": "string",
                    "enum": [
                        "STRENGTH",
                        "OPPORTUNITY",
                        "CONCERN",
                        "CONTRADICTION",
                        "CONSTRAINT",
                        "MOTIVATION",
                        "BEHAVIORAL",
                        "BUSINESS",
                        "NONE",
                    ],
                },
                "statement": {
                    "type": ["string", "null"],
                },
            },
            "required": [
                "signal_type",
                "statement",
            ],
        },
        "missing_information": {
            "type": "array",
            "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "information_needed": {
                        "type": "string",
                    },
                    "decision_impact": {
                        "type": "string",
                    },
                },
                "required": [
                    "information_needed",
                    "decision_impact",
                ],
            },
        },
        "possible_direction": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "status": {
                    "type": "string",
                    "enum": [
                        "NONE",
                        "PRELIMINARY",
                    ],
                },
                "statement": {
                    "type": ["string", "null"],
                },
            },
            "required": [
                "status",
                "statement",
            ],
        },
        "do_not_assume": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "string",
            },
        },
        "state_updates": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "current_state_summary": {
                    "type": "string",
                },
                "desired_state_summary": {
                    "type": "string",
                },
                "goals": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "priorities": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "strengths": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "assets": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "competencies": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "barriers": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "constraints": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "concerns": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "motivations": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "opportunities": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "risks": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "contradictions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "possible_routes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "route_name": {
                                "type": "string",
                            },
                            "status": {
                                "type": "string",
                                "enum": ROUTE_STATUSES,
                            },
                            "reason": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "route_name",
                            "status",
                            "reason",
                        ],
                    },
                },
                "routes_ruled_out": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "route_name": {
                                "type": "string",
                            },
                            "reason": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "route_name",
                            "reason",
                        ],
                    },
                },
            },
            "required": [
                "current_state_summary",
                "desired_state_summary",
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
                "possible_routes",
                "routes_ruled_out",
            ],
        },
    },
    "required": [
        "consultation_stage",
        "recommendation_readiness",
        "next_best_question",
        "what_rain_is_seeing",
        "important_signal",
        "missing_information",
        "possible_direction",
        "do_not_assume",
        "state_updates",
    ],
}


# =========================================================
# FINAL INTERNAL ANALYSIS SCHEMA
# =========================================================

FINAL_ANALYSIS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "consultation_objective": {
            "type": "string",
        },
        "executive_interpretation": {
            "type": "string",
        },
        "current_state": {
            "type": "string",
        },
        "desired_state": {
            "type": "string",
        },
        "underlying_goal_hypotheses": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "hypothesis": {
                        "type": "string",
                    },
                    "confidence": {
                        "type": "string",
                        "enum": CONFIDENCE_LEVELS,
                    },
                    "supporting_evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "alternative_explanation": {
                        "type": "string",
                    },
                },
                "required": [
                    "hypothesis",
                    "confidence",
                    "supporting_evidence",
                    "alternative_explanation",
                ],
            },
        },
        "strengths_and_assets": {
            "type": "array",
            "items": {"type": "string"},
        },
        "barriers_and_constraints": {
            "type": "array",
            "items": {"type": "string"},
        },
        "risks": {
            "type": "array",
            "items": {"type": "string"},
        },
        "contradictions": {
            "type": "array",
            "items": {"type": "string"},
        },
        "opportunity_signals": {
            "type": "array",
            "items": {"type": "string"},
        },
        "premature_opportunities": {
            "type": "array",
            "items": {"type": "string"},
        },
        "readiness": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "level": {
                    "type": "string",
                    "enum": [
                        "READY",
                        "CONDITIONALLY_READY",
                        "NOT_READY",
                        "UNDETERMINED",
                    ],
                },
                "ready_for": {
                    "type": "string",
                },
                "not_ready_for": {
                    "type": "string",
                },
                "reason": {
                    "type": "string",
                },
                "prerequisites": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": [
                "level",
                "ready_for",
                "not_ready_for",
                "reason",
                "prerequisites",
            ],
        },
        "routes_considered": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "route_name": {
                        "type": "string",
                    },
                    "status": {
                        "type": "string",
                        "enum": ROUTE_STATUSES,
                    },
                    "reason": {
                        "type": "string",
                    },
                },
                "required": [
                    "route_name",
                    "status",
                    "reason",
                ],
            },
        },
        "primary_direction": {
            "type": "string",
        },
        "recommended_fyw_route": {
            "type": ["string", "null"],
        },
        "secondary_route": {
            "type": ["string", "null"],
        },
        "recommended_sequence": {
            "type": "array",
            "items": {"type": "string"},
        },
        "what_not_to_recommend": {
            "type": "array",
            "items": {"type": "string"},
        },
        "immediate_next_action": {
            "type": "string",
        },
        "overall_confidence": {
            "type": "string",
            "enum": CONFIDENCE_LEVELS,
        },
    },
    "required": [
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
    ],
}


# =========================================================
# CLIENT STRATEGIC GAME PLAN SCHEMA
# =========================================================

CLIENT_GAME_PLAN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "report_title": {
            "type": "string",
        },
        "client_name": {
            "type": "string",
        },
        "business_name": {
            "type": "string",
        },
        "strategic_snapshot": {
            "type": "string",
        },
        "current_position": {
            "type": "string",
        },
        "desired_outcome": {
            "type": "string",
        },
        "core_challenges": {
            "type": "array",
            "items": {"type": "string"},
        },
        "strengths_and_assets": {
            "type": "array",
            "items": {"type": "string"},
        },
        "primary_opportunity": {
            "type": "string",
        },
        "strategic_direction": {
            "type": "string",
        },
        "immediate_priorities": {
            "type": "array",
            "items": {"type": "string"},
        },
        "step_by_step_game_plan": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "step": {
                        "type": "integer",
                    },
                    "action": {
                        "type": "string",
                    },
                    "purpose": {
                        "type": "string",
                    },
                    "success_indicator": {
                        "type": "string",
                    },
                },
                "required": [
                    "step",
                    "action",
                    "purpose",
                    "success_indicator",
                ],
            },
        },
        "first_30_days": {
            "type": "array",
            "items": {"type": "string"},
        },
        "days_31_to_60": {
            "type": "array",
            "items": {"type": "string"},
        },
        "days_61_to_90": {
            "type": "array",
            "items": {"type": "string"},
        },
        "recommended_fyw_support": {
            "type": "array",
            "items": {"type": "string"},
        },
        "risks_and_things_to_avoid": {
            "type": "array",
            "items": {"type": "string"},
        },
        "final_strategic_guidance": {
            "type": "string",
        },
    },
    "required": [
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
    ],
}


# =========================================================
# SCHEMA WRAPPERS FOR THE RESPONSES API
# =========================================================

RAIN_LIVE_TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "rain_live_analysis",
        "strict": True,
        "schema": LIVE_RESPONSE_SCHEMA,
    }
}


RAIN_FINAL_TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "rain_final_analysis",
        "strict": True,
        "schema": FINAL_ANALYSIS_SCHEMA,
    }
}


RAIN_CLIENT_GAME_PLAN_TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "rain_client_game_plan",
        "strict": True,
        "schema": CLIENT_GAME_PLAN_SCHEMA,
    }
}