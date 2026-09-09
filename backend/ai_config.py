"""
Find Your Way Consulting Suite
Central AI Model Configuration

Model names are kept here so FYW tools can change models
without editing their full application code.
"""

# Find Where You Win flagship model
FIND_WHERE_YOU_WIN_MODEL = "gpt-5.6"

# RAIN live consultation model
# Used repeatedly for extraction, intelligence updates,
# contradiction detection, and next-best-question generation.
RAIN_LIVE_MODEL = "gpt-5.6-terra"

# RAIN final strategic analysis model
# Used once near the end for the deeper consultation analysis
# and polished client-facing Strategic Game Plan.
RAIN_FINAL_MODEL = "gpt-6-astra"