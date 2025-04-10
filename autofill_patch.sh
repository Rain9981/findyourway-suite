#!/bin/bash
cd ~/FindYourWay_CleanPush

# 🔁 Patch autofill for brand_positioning
sed -i '/st.text_area.*key.*brand_positioning_input.*/a \
    if st.button("✨ Autofill Suggestion", key="brand_positioning_fill"):\n        user_input = "Suggest something for brand positioning"\n' brand_positioning/brand_positioning_app.py

# 🔁 Patch autofill for business_development
sed -i '/st.text_area.*key.*business_development_input.*/a \
    if st.button("✨ Autofill Suggestion", key="business_development_fill"):\n        user_input = "Suggest something for business development"\n' business_development/business_development_app.py

# 🔁 Patch autofill for business_model_canvas
sed -i '/st.text_area.*key.*business_model_canvas_input.*/a \
    if st.button("✨ Autofill Suggestion", key="business_model_canvas_fill"):\n        user_input = "Suggest something for business model canvas"\n' business_model_canvas/business_model_canvas_app.py

# 🔁 Patch autofill for canvas
sed -i '/st.text_area.*key.*canvas_input.*/a \
    if st.button("✨ Autofill Suggestion", key="canvas_fill"):\n        user_input = "Suggest something for canvas"\n' canvas/canvas_app.py

# 🔁 Patch autofill for client_intake
sed -i '/st.text_area.*key.*client_intake_input.*/a \
    if st.button("✨ Autofill Suggestion", key="client_intake_fill"):\n        user_input = "Suggest something for client intake"\n' client_intake/client_intake_app.py

# 🔁 Patch autofill for consulting_guide
sed -i '/st.text_area.*key.*consulting_guide_input.*/a \
    if st.button("✨ Autofill Suggestion", key="consulting_guide_fill"):\n        user_input = "Suggest something for consulting guide"\n' consulting_guide/consulting_guide_app.py

# 🔁 Patch autofill for credit_repair
sed -i '/st.text_area.*key.*credit_repair_input.*/a \
    if st.button("✨ Autofill Suggestion", key="credit_repair_fill"):\n        user_input = "Suggest something for credit repair"\n' credit_repair/credit_repair_app.py

# 🔁 Patch autofill for email_marketing
sed -i '/st.text_area.*key.*email_marketing_input.*/a \
    if st.button("✨ Autofill Suggestion", key="email_marketing_fill"):\n        user_input = "Suggest something for email marketing"\n' email_marketing/email_marketing_app.py

# 🔁 Patch autofill for forecasting
sed -i '/st.text_area.*key.*forecasting_input.*/a \
    if st.button("✨ Autofill Suggestion", key="forecasting_fill"):\n        user_input = "Suggest something for forecasting"\n' forecasting/forecasting_app.py

# 🔁 Patch autofill for growth
sed -i '/st.text_area.*key.*growth_input.*/a \
    if st.button("✨ Autofill Suggestion", key="growth_fill"):\n        user_input = "Suggest something for growth"\n' growth/growth_app.py

# 🔁 Patch autofill for homepage
sed -i '/st.text_area.*key.*homepage_input.*/a \
    if st.button("✨ Autofill Suggestion", key="homepage_fill"):\n        user_input = "Suggest something for homepage"\n' homepage/homepage_app.py

# 🔁 Patch autofill for kpi_tracker
sed -i '/st.text_area.*key.*kpi_tracker_input.*/a \
    if st.button("✨ Autofill Suggestion", key="kpi_tracker_fill"):\n        user_input = "Suggest something for kpi tracker"\n' kpi_tracker/kpi_tracker_app.py

# 🔁 Patch autofill for lead_generation
sed -i '/st.text_area.*key.*lead_generation_input.*/a \
    if st.button("✨ Autofill Suggestion", key="lead_generation_fill"):\n        user_input = "Suggest something for lead generation"\n' lead_generation/lead_generation_app.py

# 🔁 Patch autofill for marketing_hub
sed -i '/st.text_area.*key.*marketing_hub_input.*/a \
    if st.button("✨ Autofill Suggestion", key="marketing_hub_fill"):\n        user_input = "Suggest something for marketing hub"\n' marketing_hub/marketing_hub_app.py

# 🔁 Patch autofill for marketing_planner
sed -i '/st.text_area.*key.*marketing_planner_input.*/a \
    if st.button("✨ Autofill Suggestion", key="marketing_planner_fill"):\n        user_input = "Suggest something for marketing planner"\n' marketing_planner/marketing_planner_app.py

# 🔁 Patch autofill for network
sed -i '/st.text_area.*key.*network_input.*/a \
    if st.button("✨ Autofill Suggestion", key="network_fill"):\n        user_input = "Suggest something for network"\n' network/network_app.py

# 🔁 Patch autofill for network_builder
sed -i '/st.text_area.*key.*network_builder_input.*/a \
    if st.button("✨ Autofill Suggestion", key="network_builder_fill"):\n        user_input = "Suggest something for network builder"\n' network_builder/network_builder_app.py

# 🔁 Patch autofill for oops_audit
sed -i '/st.text_area.*key.*oops_audit_input.*/a \
    if st.button("✨ Autofill Suggestion", key="oops_audit_fill"):\n        user_input = "Suggest something for oops audit"\n' oops_audit/oops_audit_app.py

# 🔁 Patch autofill for operations_audit
sed -i '/st.text_area.*key.*operations_audit_input.*/a \
    if st.button("✨ Autofill Suggestion", key="operations_audit_fill"):\n        user_input = "Suggest something for operations audit"\n' operations_audit/operations_audit_app.py

# 🔁 Patch autofill for self_enhancement
sed -i '/st.text_area.*key.*self_enhancement_input.*/a \
    if st.button("✨ Autofill Suggestion", key="self_enhancement_fill"):\n        user_input = "Suggest something for self enhancement"\n' self_enhancement/self_enhancement_app.py

# 🔁 Patch autofill for sentiment_analysis
sed -i '/st.text_area.*key.*sentiment_analysis_input.*/a \
    if st.button("✨ Autofill Suggestion", key="sentiment_analysis_fill"):\n        user_input = "Suggest something for sentiment analysis"\n' sentiment_analysis/sentiment_analysis_app.py

# 🔁 Patch autofill for strategic_simulator
sed -i '/st.text_area.*key.*strategic_simulator_input.*/a \
    if st.button("✨ Autofill Suggestion", key="strategic_simulator_fill"):\n        user_input = "Suggest something for strategic simulator"\n' strategic_simulator/strategic_simulator_app.py

# 🔁 Patch autofill for strategy_designer
sed -i '/st.text_area.*key.*strategy_designer_input.*/a \
    if st.button("✨ Autofill Suggestion", key="strategy_designer_fill"):\n        user_input = "Suggest something for strategy designer"\n' strategy_designer/strategy_designer_app.py

# 🔁 Patch autofill for subscription_plans
sed -i '/st.text_area.*key.*subscription_plans_input.*/a \
    if st.button("✨ Autofill Suggestion", key="subscription_plans_fill"):\n        user_input = "Suggest something for subscription plans"\n' subscription_plans/subscription_plans_app.py

echo "\n✅ Autofill buttons added. Now run:"
echo "git add . && git commit -m '✨ Add autofill suggestion buttons to all tabs' && git push"
