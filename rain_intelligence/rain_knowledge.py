"""
RAIN Intelligence FYW knowledge and routing rules.

This file provides operational knowledge for internal strategic reasoning.
It is not marketing copy and does not automatically sell FYW services.
"""

import json


RAIN_IDENTITY = {
    "name": "RAIN Intelligence",
    "owner": "James Bailey",
    "organization": "Find Your Way Network Marketing Consultants",
    "purpose": (
        "A private strategic consulting copilot used by James Bailey during "
        "consultations, discovery conversations, business diagnosis, personal "
        "direction discussions, opportunity analysis, and and ongoing strategy consultations."
    ),
    "client_facing": False,
    "decision_authority": "James Bailey",
}


CONSULTING_PRINCIPLES = [
    "Client benefit and strategic fit take precedence over selling an FYW service.",
    "Diagnose the situation before recommending a service, tool, or program.",
    "Never route from keywords alone.",
    "Treat client statements as evidence to investigate, not automatically confirmed facts.",
    "Clearly label hypotheses, uncertainty, missing information, and contradictions.",
    "Consider more than one explanation when the underlying problem is uncertain.",
    "Prefer the smallest sufficient next move over the largest engagement.",
    "Respect the client's time, money, skills, authority, attention, and delivery capacity.",
    "A valuable service offered before the client is ready is still a poor recommendation.",
    "RAIN may recommend more investigation, a prerequisite, an outside resource, or no paid FYW service.",
    "RAIN remains advisory. James may accept, modify, ignore, or override its interpretation.",
]


FYW_ROUTE_FAMILIES = {
    "management_consulting": {
        "name": "Management Consulting",
        "addresses": [
            "Cross-functional business problems",
            "Unclear priorities or strategic direction",
            "Business-model decisions",
            "Leadership and decision problems",
            "Problems involving multiple business functions",
        ],
        "fit_signals": [
            "The stated problem involves more than one business function",
            "The client needs diagnosis and sequencing before execution",
            "Several possible explanations remain credible",
            "The owner needs help making consequential business choices",
        ],
        "prerequisites": [
            "Access to enough business information for responsible analysis",
            "Participation by the appropriate decision-maker",
            "Willingness to examine assumptions and alternatives",
        ],
        "premature_signals": [
            "The request is one clearly bounded execution task",
            "The client will not provide decision-critical information",
            "A personal-stability issue must be addressed first",
        ],
        "usual_sequence": [
            "Strategic diagnosis",
            "Decision and priority clarification",
            "Specialist or execution route",
            "Review and adjustment",
        ],
        "ask_before_routing": [
            "What decision must this consultation help the client make?",
            "Which business functions are involved?",
            "What evidence supports the client's explanation of the problem?",
            "Who has authority to act on the recommendation?",
        ],
    },

    "branding": {
        "name": "Branding",
        "addresses": [
            "Unclear or inconsistent brand identity",
            "Weak brand expression",
            "Mismatch between intended positioning and market perception",
            "Visual or verbal identity problems",
        ],
        "fit_signals": [
            "The audience, offer, and strategic position are sufficiently clear",
            "The brand does not communicate the intended value",
            "Visual inconsistency is creating a measurable trust or recognition problem",
        ],
        "prerequisites": [
            "Defined target audience",
            "Defined offer or service",
            "Clear value promise",
            "Stable strategic direction",
            "Decision authority and usable creative brief",
        ],
        "premature_signals": [
            "The audience is everyone",
            "The offer changes constantly",
            "The client is using a logo redesign to avoid a strategy decision",
            "Operations or service quality is the supported underlying problem",
        ],
        "usual_sequence": [
            "Strategy and positioning",
            "Brand direction",
            "DWD IE creative execution when appropriate",
            "Marketing deployment",
        ],
        "ask_before_routing": [
            "What must the brand help the correct audience understand?",
            "Is the offer stable enough to build an identity around?",
            "What evidence shows branding is contributing to the problem?",
            "Would a new identity solve the underlying constraint?",
        ],
    },

    "marketing": {
        "name": "Marketing",
        "addresses": [
            "Visibility",
            "Demand generation",
            "Content and campaign planning",
            "Customer journey",
            "Channel strategy",
            "Conversion support",
        ],
        "fit_signals": [
            "The offer and audience are defined",
            "The business can fulfill additional demand",
            "A measurable awareness, acquisition, or conversion gap exists",
            "The client has capacity to maintain the selected channels",
        ],
        "prerequisites": [
            "Stable offer",
            "Defined target audience",
            "Clear call to action",
            "Lead follow-up process",
            "Delivery capacity",
            "Realistic time or budget",
        ],
        "premature_signals": [
            "The business cannot currently fulfill more work",
            "The offer is not clear",
            "The client does not know who the customer is",
            "There is no follow-up or conversion pathway",
            "Marketing is being blamed without funnel evidence",
        ],
        "usual_sequence": [
            "Positioning",
            "Marketing plan",
            "Campaign or content execution",
            "Lead follow-up",
            "KPI review",
        ],
        "ask_before_routing": [
            "Where is the customer journey currently breaking down?",
            "Can the business fulfill more demand?",
            "What marketing has been attempted and what happened?",
            "How are leads followed up and converted?",
        ],
    },

    "business_development": {
        "name": "Business Development",
        "addresses": [
            "Sales process",
            "Partnerships",
            "Pipeline development",
            "Offer relationships",
            "Revenue opportunities",
        ],
        "fit_signals": [
            "The client has a clear value exchange",
            "Partnerships or sales execution are supported bottlenecks",
            "The business can fulfill resulting opportunities",
            "A repeatable opportunity pipeline can be developed",
        ],
        "prerequisites": [
            "Clear offer",
            "Defined customer or partner",
            "Follow-up ownership",
            "Fulfillment capacity",
        ],
        "premature_signals": [
            "The client wants connections without a clear value proposition",
            "The business cannot deliver what would be sold",
            "There is no ownership for follow-up",
        ],
        "usual_sequence": [
            "Offer clarification",
            "Pipeline or partnership strategy",
            "CRM and follow-up",
            "Opportunity review",
        ],
        "ask_before_routing": [
            "What specific value can the client exchange?",
            "Which relationships could advance the goal?",
            "Who owns follow-up?",
            "What happens operationally if an opportunity closes?",
        ],
    },

    "network_building": {
        "name": "Network Building",
        "addresses": [
            "Relationship development",
            "Referral systems",
            "Reciprocal opportunity",
            "Connection strategy",
            "Service routing",
        ],
        "fit_signals": [
            "A specific connection could create mutual value",
            "The client can both contribute and receive value",
            "Permission and follow-up responsibilities can be established",
        ],
        "prerequisites": [
            "Clear give-and-get proposition",
            "Credibility",
            "Appropriate consent",
            "Follow-up ownership",
            "Respect for confidentiality and attribution",
        ],
        "premature_signals": [
            "The client only wants access to other people's relationships",
            "No mutual value exists",
            "The client is not ready to follow through",
            "A proposed introduction could damage trust",
        ],
        "usual_sequence": [
            "Clarify value",
            "Qualify both parties",
            "Obtain permission",
            "Make a bounded introduction",
            "Track outcome and reciprocity",
        ],
        "ask_before_routing": [
            "What does each party gain?",
            "What is expected from each party?",
            "Has permission been obtained?",
            "Who owns the next action and attribution?",
        ],
    },

    "self_enhancement": {
        "name": "Self Enhancement and Personal Direction",
        "addresses": [
            "Personal direction",
            "Identity and future-self clarity",
            "Confidence",
            "Goals and structure",
            "Execution discipline",
            "Personal readiness before entrepreneurship",
        ],
        "fit_signals": [
            "Personal uncertainty is blocking action",
            "The client repeatedly changes direction",
            "Goals exist without structure",
            "Confidence or self-concept conflict is stopping execution",
            "Personal stability should precede business building",
        ],
        "prerequisites": [
            "Willingness to reflect honestly",
            "Willingness to take appropriate personal action",
            "The situation remains within FYW's nonclinical scope",
        ],
        "premature_signals": [
            "The situation suggests clinical, crisis, or safety needs",
            "The client already has personal clarity and only needs a business execution system",
        ],
        "usual_sequence": [
            "Direction and self-understanding",
            "Goals and structure",
            "Execution",
            "Entrepreneurship or business pathway when appropriate",
        ],
        "ask_before_routing": [
            "Is the main barrier personal direction, business strategy, or execution?",
            "What pattern repeatedly prevents action?",
            "Does the client need clarity, structure, confidence, or outside professional support?",
        ],
    },

    "expertise_to_opportunity": {
        "name": "Expertise to Opportunity",
        "addresses": [
            "Turning proven expertise into an offer",
            "Creating a customized client outcome",
            "Building a service, tool, or guided product",
            "Packaging a repeatable method",
        ],
        "fit_signals": [
            "The client has solved or repeatedly handled a meaningful problem",
            "Other people already request the client's help",
            "A defined audience wants a different outcome",
            "The client's method can be customized or repeated",
        ],
        "prerequisites": [
            "Evidence of relevant expertise",
            "A defined beneficiary",
            "A meaningful problem and desired outcome",
            "No employer, confidentiality, licensing, or intellectual-property conflict",
            "Capacity to pilot the offer",
        ],
        "premature_signals": [
            "There is no evidence of expertise",
            "The client cannot identify who benefits",
            "The client wants to build technology before validating the outcome",
            "The opportunity conflicts with employment or legal restrictions",
        ],
        "usual_sequence": [
            "Proof",
            "Audience",
            "Customization",
            "Kickoff",
            "Pilot",
            "Refine and launch",
        ],
        "ask_before_routing": [
            "What has the client already solved or figured out?",
            "Who has this problem and what do they want instead?",
            "What must be customized for each customer?",
            "What evidence would validate the offer?",
        ],
    },

    "fyw_labs": {
        "name": "FYW Labs",
        "addresses": [
            "Guided creation",
            "Done-with-you creation",
            "Done-for-you creation",
            "Offer, service, tool, or system development",
        ],
        "fit_signals": [
            "The build target is clearly defined",
            "The intended user and outcome are known",
            "A pilot or validation method exists",
            "The client has the resources and commitment to complete the build",
        ],
        "prerequisites": [
            "Defined problem",
            "Defined audience",
            "Defined outcome",
            "Defined minimum build",
            "Owner and success test",
        ],
        "premature_signals": [
            "The client is still exploring unrelated ideas",
            "The problem has not been validated",
            "The build is being used to avoid customer discovery",
        ],
        "usual_sequence": [
            "Diagnosis",
            "Scope",
            "Minimum build",
            "Pilot",
            "Validation",
            "Refinement",
        ],
        "ask_before_routing": [
            "What exactly needs to be built?",
            "Who will use it?",
            "What outcome must it create?",
            "What is the smallest version that can be tested?",
        ],
    },

    "business_growth_systems": {
        "name": "Business and Growth Systems",
        "addresses": [
            "Measurement",
            "Forecasting",
            "CRM",
            "Operations",
            "Campaign systems",
            "Lead management",
            "Repeatable execution",
        ],
        "fit_signals": [
            "The business already performs meaningful activity",
            "The client needs consistency, measurement, or repeatability",
            "A process owner and usable baseline exist",
        ],
        "prerequisites": [
            "Defined process",
            "Process owner",
            "Reliable baseline information",
            "Commitment to maintain the system",
        ],
        "premature_signals": [
            "The client wants software instead of process ownership",
            "The activity being measured is not defined",
            "The client will not maintain the system",
        ],
        "usual_sequence": [
            "Strategy",
            "Process definition",
            "System implementation",
            "Adoption",
            "Measurement and adjustment",
        ],
        "ask_before_routing": [
            "What process needs to become repeatable?",
            "Who owns it?",
            "What information is currently available?",
            "How will the system be maintained?",
        ],
    },
}


SELF_ENHANCEMENT_PATHWAYS = {
    "Ascendant Prism": (
        "Accessible initial reflection on the client's current self, desired self, "
        "and personal direction."
    ),
    "Ignite Inner Vision": (
        "Deeper articulation of internal vision and the future the client wants "
        "to see clearly enough to pursue."
    ),
    "Ignite Destiny": (
        "Commitment to a larger personal direction after meaningful vision "
        "has been identified."
    ),
    "Initiation Protocol": (
        "Transition from reflection into a disciplined beginning."
    ),
    "Goals and Structure": (
        "Priority, milestone, scheduling, and execution structure for a defined goal."
    ),
    "Goal Life Sheet": (
        "Structured representation of goals, life areas, priorities, and actions."
    ),
    "Breakthrough and Execute": (
        "Execution support when a defined plan repeatedly stalls."
    ),
    "FYW Goal Dashboard": (
        "Ongoing visibility and measurement for goals the client is prepared to maintain."
    ),
    "FYW Legacy Architecture": (
        "Long-horizon impact, assets, succession, family, business, or community legacy."
    ),
}


FYW_INTELLIGENCE_PATHWAYS = {
    "Discover Your Path Within Find Your Way": (
        "Broad FYW orientation when the correct pathway remains unclear."
    ),
    "Opportunity Discovery": (
        "Structured identification and prioritization of opportunities. "
        "It is a specialist system beneath RAIN and should not be duplicated inside RAIN."
    ),
    "Find Where You Win": (
        "Market, capability, location, and opportunity-fit analysis."
    ),
    "Business Genius Engine": (
        "Business intelligence and strategic possibility synthesis."
    ),
    "Strategic Simulator": (
        "Comparison of defined strategic scenarios, assumptions, and consequences."
    ),
    "Mastermind Analyzer": (
        "Structured synthesis of multi-person insights and perspectives."
    ),
}


FYW_BUSINESS_TOOLS = {
    "Growth": "Growth planning and execution.",
    "KPI Tracker": "Measurement of defined performance indicators.",
    "Forecasting": "Forward planning based on usable assumptions and baseline data.",
    "CRM": "Relationship and opportunity records.",
    "CRM Manager": "CRM workflow and record management.",
    "CRM Dashboard": "CRM visibility and performance review.",
    "Brand Positioning": "Audience, differentiation, value, and market-position decisions.",
    "Business Development": "Sales, partnerships, pipeline, and revenue relationships.",
    "Strategy Designer": "Structured strategic choices and priorities.",
    "Business Model Canvas": "Business-model components and their relationships.",
    "Email Marketing": "Permission-based email strategy and execution.",
    "AI CMO Engine": "Marketing and growth diagnosis from a CMO perspective.",
    "Campaign Engine": "Campaign planning and execution.",
    "Marketing Hub": "Central marketing direction and resources.",
    "Marketing Planner": "Marketing planning and scheduling.",
    "Sentiment Analysis": "Interpretation of sufficient customer or stakeholder language data.",
    "Operations Audit": "Process, workflow, ownership, and operational diagnosis.",
    "OOPS Audit": "Operational problem and execution review.",
    "Lead Generation": "Customer-acquisition planning after offer and conversion readiness.",
    "Network Builder": "Relationship and network strategy.",
    "Service Creation Engine": "Service design after problem, audience, and outcome validation.",
}


NETWORK_ECOSYSTEM = {
    "FYW InterNetwork": {
        "purpose": (
            "Opportunity, referral, relationship, and service-routing ecosystem."
        ),
        "public_line": "Navigate. Connect. Grow.",
    },
    "Contractors Compass": {
        "purpose": (
            "Connection of Contractors Network and Professionals Network pathways."
        ),
    },
    "Contractors Network": {
        "purpose": "Qualified contractor relationships and property-service opportunities.",
    },
    "Professionals Network": {
        "purpose": "Professional relationships, expertise, and opportunity connection.",
    },
    "Business Network": {
        "purpose": "Business relationships, partnerships, and reciprocal growth.",
    },
    "categories": [
        "Professional Services",
        "Retail Services",
        "Media and Entertainment",
        "Business and Trade Services",
    ],
    "routing_requirements": [
        "Specific mutual value",
        "Permission",
        "Appropriate readiness",
        "Follow-up ownership",
        "Attribution",
        "Protection of relationship trust",
    ],
}


RELATED_ECOSYSTEM = {
    "DWD IE": {
        "name": "Dynasty White Design Innovative Enterprise",
        "capabilities": [
            "Graphic Design",
            "Visual Concepts and Image Reinvention",
            "Website Design",
            "Custom Apparel",
            "Video Production and Editing",
            "Create M'EYE Visionz spatial and interior design",
            "Creator Network",
        ],
        "routing_rule": (
            "Route only when creative execution is the supported next constraint "
            "and strategy, audience, scope, ownership, and resources are sufficiently clear."
        ),
    },
    "Better N Clean": {
        "capabilities": [
            "Residential cleaning",
            "Commercial cleaning",
            "Property and Service Solutions",
            "Workforce and Opportunity Intake",
            "Property Request routing",
        ],
        "routing_rule": (
            "Route only when there is a verified property or service need, "
            "appropriate scope, location, timing, permission, and service capacity."
        ),
    },
}


UNIVERSAL_ROUTE_GATES = [
    "What outcome is the client actually trying to achieve?",
    "What evidence supports the believed underlying problem?",
    "What has already been attempted and what happened?",
    "What strengths and assets already exist?",
    "What limitations and constraints affect feasibility?",
    "What time, money, attention, skill, authority, and support are available?",
    "What material contradictions remain unresolved?",
    "What prerequisites must happen first?",
    "What non-FYW option may serve the client better?",
    "What is the smallest responsible immediate next move?",
]


DO_NOT_RECOMMEND_RULES = [
    "Do not recommend branding when strategy, audience, or offer is unresolved.",
    "Do not recommend marketing when fulfillment, positioning, or follow-up is unresolved.",
    "Do not recommend lead generation when the business cannot convert or fulfill demand.",
    "Do not recommend CRM when no repeatable relationship or opportunity process exists.",
    "Do not recommend forecasting without usable assumptions and baseline data.",
    "Do not recommend FYW Labs before the build target and outcome are validated.",
    "Do not recommend network introductions without mutual value and permission.",
    "Do not recommend entrepreneurship when personal direction or stability must come first.",
    "Do not recommend a paid FYW route merely because one is available.",
    "Do not replace qualified legal, medical, mental-health, tax, or financial advice.",
]


def get_full_rain_knowledge():
    """
    Return the full operational FYW knowledge package.
    """

    return {
        "rain_identity": RAIN_IDENTITY,
        "consulting_principles": CONSULTING_PRINCIPLES,
        "route_families": FYW_ROUTE_FAMILIES,
        "self_enhancement_pathways": SELF_ENHANCEMENT_PATHWAYS,
        "fyw_intelligence_pathways": FYW_INTELLIGENCE_PATHWAYS,
        "fyw_business_tools": FYW_BUSINESS_TOOLS,
        "network_ecosystem": NETWORK_ECOSYSTEM,
        "related_ecosystem": RELATED_ECOSYSTEM,
        "universal_route_gates": UNIVERSAL_ROUTE_GATES,
        "do_not_recommend_rules": DO_NOT_RECOMMEND_RULES,
    }


def get_rain_knowledge_context():
    """
    Convert the knowledge package into prompt-ready JSON.

    The model must reason across this information.
    It must not perform automatic keyword-to-service matching.
    """

    return json.dumps(
        get_full_rain_knowledge(),
        indent=2,
        ensure_ascii=False,
    )