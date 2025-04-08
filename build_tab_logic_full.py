import os

def write_file(path, content):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# --- Smart Tab Generator ---
def smart_tab(folder, label, description, inputs=None, gpt=False, sheets=False, pdf=False, link=None):
    code = f'''import streamlit as st
import pandas as pd
{"import openai" if gpt else ""}
{"import io\nfrom reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import letter" if pdf else ""}

{"openai.api_key = st.secrets['openai']['api_key']" if gpt else ""}

def run():
    st.title("{label}")
    st.markdown("### {description}")

'''
    if link:
        code += f'    st.link_button("Launch Portal", "{link}")\n'

    if inputs:
        for i in inputs:
            if i["type"] == "text":
                code += f'    {i["id"]} = st.text_input("{i["label"]}")\n'
            elif i["type"] == "select":
                code += f'    {i["id"]} = st.selectbox("{i["label"]}", {i["options"]})\n'
            elif i["type"] == "textarea":
                code += f'    {i["id"]} = st.text_area("{i["label"]}")\n'
            elif i["type"] == "number":
                code += f'    {i["id"]} = st.number_input("{i["label"]}", min_value={i.get("min",0)}, value={i.get("value",0)}, step={i.get("step",1)})\n'
            elif i["type"] == "slider":
                code += f'    {i["id"]} = st.slider("{i["label"]}", min_value={i["min"]}, max_value={i["max"]}, value={i["value"]})\n'

    if gpt:
        code += '''
    if st.button("Run GPT Analysis"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Analyze the following input: "},
                {"role": "user", "content": business_name if 'business_name' in locals() else 'N/A'}
            ]
        )
        st.success(response['choices'][0]['message']['content'].strip())
'''

    if sheets:
        code += '''
    # Google Sheets saving (optional backend logic)
    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals())
        st.info("✅ Data saved to Google Sheets.")
    except:
        st.warning("Google Sheets not connected.")
'''

    if pdf:
        code += '''
    if st.button("Export to PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Consulting Report")
        c.drawString(100, 735, "------------------")
        y = 720
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")
'''

    write_file(f"{folder}/{folder}_app.py", code)

# --- Define All Tabs ---
tabs = [
    ("forecasting", "📈 Revenue Forecasting", "Project revenue growth.",
     [{"type": "text", "id": "business_name", "label": "Business Name"},
      {"type": "number", "id": "revenue", "label": "Starting Revenue", "value": 1000},
      {"type": "slider", "id": "growth", "label": "Growth %", "min": 0, "max": 100, "value": 10}],
     False, True, True, None),

    ("sentiment_analysis", "📊 Sentiment Analyzer", "Gauge public or client sentiment.",
     [{"type": "text", "id": "query", "label": "Enter topic or text"}],
     True, True, True, None),

    ("strategic_simulator", "🧠 Strategic Simulator", "Run what-if business scenarios.",
     [{"type": "select", "id": "scenario", "label": "Choose Scenario", "options": ["Cut prices", "Hire staff", "Launch product"]}],
     True, True, True, None),

    ("client_intake", "📝 Client Intake Form", "Collect client onboarding info.",
     [{"type": "text", "id": "client_name", "label": "Client Name"},
      {"type": "text", "id": "industry", "label": "Industry"},
      {"type": "textarea", "id": "goals", "label": "Client Goals"}],
     False, True, False, None),

    ("brand_positioning", "🎯 Brand Positioning", "Clarify brand message.",
     [{"type": "text", "id": "brand_promise", "label": "Brand Promise"},
      {"type": "text", "id": "target_market", "label": "Target Market"}],
     True, True, True, None),

    ("kpi_tracker", "📊 KPI Tracker", "Track key performance indicators.",
     [{"type": "text", "id": "kpi_name", "label": "KPI Name"},
      {"type": "number", "id": "kpi_value", "label": "Current Value", "value": 0}],
     False, True, False, None),

    ("strategy_designer", "📐 Strategy Designer", "Draft your business strategy.",
     [{"type": "textarea", "id": "plan", "label": "Write your strategic plan"}],
     True, False, True, None),

    ("business_model_canvas", "🧱 Business Model Canvas", "Define key elements of your model.",
     [{"type": "text", "id": "value_prop", "label": "Value Proposition"},
      {"type": "text", "id": "customer_segments", "label": "Customer Segments"}],
     False, True, False, None),

    ("operations_audit", "⚙️ Ops Audit", "Audit internal systems.",
     [{"type": "textarea", "id": "systems", "label": "Describe Current Systems"}],
     False, True, True, None),

    ("lead_generation", "🧲 Lead Generator", "Generate targeted leads.",
     [{"type": "text", "id": "niche", "label": "Target Niche"},
      {"type": "text", "id": "region", "label": "Region"}],
     True, True, False, None),

    ("crm_manager", "📇 CRM Manager", "Track and manage clients.",
     [{"type": "text", "id": "client", "label": "Client Name"},
      {"type": "text", "id": "email", "label": "Email"},
      {"type": "select", "id": "stage", "label": "Stage", "options": ["Lead", "Prospect", "Customer"]}],
     False, True, True, None),

    ("network_builder", "🌐 Network Builder", "Build your referral map.",
     [{"type": "text", "id": "partner_name", "label": "Partner Name"},
      {"type": "text", "id": "area", "label": "Area of Support"}],
     False, False, False, None),

    ("business_development", "💼 Business Development", "Plan business expansion.",
     [{"type": "textarea", "id": "dev_goals", "label": "Growth Goals"}],
     True, True, False, None),

    ("self_enhancement", "🧠 Self Enhancement", "Founder/owner growth area.",
     [{"type": "textarea", "id": "focus", "label": "Personal Development Focus"}],
     False, False, False, None),

    ("marketing_hub", "📢 Marketing Hub", "Marketing scripts and tools.",
     [{"type": "text", "id": "campaign", "label": "Campaign Name"},
      {"type": "textarea", "id": "copy", "label": "Marketing Copy"}],
     True, False, True, None),

    ("credit_repair", "💳 Credit Repair", "Portal for credit clients.",
     [], False, False, False, "https://findyourwaynmc.creditmyreport.com")
]

# --- Build Tabs ---
for folder, label, desc, inputs, gpt, sheets, pdf, link in tabs:
    smart_tab(folder, label, desc, inputs, gpt, sheets, pdf, link)

print("✅ All enhanced tabs built with logic, inputs, GPT, Sheets, PDF, and roles.")
