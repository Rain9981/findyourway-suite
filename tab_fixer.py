import os

def write_tab_file(filename, title, description):
    content = f'''import streamlit as st

def run():
    st.title("📌 {title} Dashboard")
    st.markdown(\"\"\"
    ### {description}
    This section will help you work through your business strategy in this area.
    \"\"\")
'''
    with open(os.path.join("tabs", filename), "w", encoding="utf-8") as f:
        f.write(content)

# Make sure 'tabs' folder exists
os.makedirs("tabs", exist_ok=True)

tabs_info = [
    ("forecasting.py", "Revenue Forecasting", "Project monthly revenue growth and plan financials."),
    ("sentiment.py", "Market Sentiment Analyzer", "Gauge public or customer sentiment around trends or products."),
    ("simulator.py", "Strategic Simulator", "Simulate different business decisions and their potential outcomes."),
    ("intake.py", "Client Intake Form", "Capture key business info and onboarding details."),
    ("brand_positioning.py", "Brand Positioning Map", "Define your brand strengths, values, and position in the market."),
    ("business_plan.py", "Business Plan Builder", "Build core sections of a strategic business plan."),
    ("leads.py", "Lead Generator", "Generate target leads based on niche, service, and location."),
    ("crm.py", "CRM Dashboard", "Track and manage your client relationships."),
    ("kpi.py", "KPI Tracker", "Set and monitor key performance indicators."),
    ("funnel.py", "Sales Funnel Optimizer", "Map and analyze your lead-to-sale conversion process."),
    ("email.py", "Email Campaign Manager", "Draft and prepare strategic email sequences."),
    ("audit.py", "Website/Brand Audit", "Assess and improve brand assets or site performance."),
    ("social.py", "Social Media Strategy", "Plan social content and channel strategy."),
    ("credit.py", "Credit Repair Portal", "Integration area for credit clients and reports."),
    ("toolkit.py", "Marketing Toolkit", "Resources and templates for client growth."),
    ("admin_settings.py", "Admin Panel", "Export reports, manage users, access private tools.")
]

for filename, title, description in tabs_info:
    write_tab_file(filename, title, description)

print("✅ All 16 tabs updated with branded dashboards.")
