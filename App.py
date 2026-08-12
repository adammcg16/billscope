import streamlit as st
import pandas as pd
import pdfplumber
import urllib.parse

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

CONCIERGE_EMAIL = "adammcg_16@hotmail.com"

# --- LOAD BENCHMARK DATA FROM EXCEL ---
@st.cache_data
def load_data():
    file_path = "billscope_tabs.xlsx"
    electricity = pd.read_excel(file_path, sheet_name="Electricity")
    internet = pd.read_excel(file_path, sheet_name="Internet")
    return electricity, internet

try:
    elec_df, net_df = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}. Please ensure 'billscope_tabs.xlsx' is uploaded to your GitHub repository.")
    st.stop()

# --- NAVIGATION SESSION STATE MANAGEMENT ---
if "app_page" not in st.session_state:
    st.session_state.app_page = "Home"

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("🔍 BillScope Menu")

# Pages list
pages = ["Home", "Instant Bill Auditor", "Contact Concierge", "Terms & Conditions"]

# Sync radio with session state
selected_page = st.sidebar.radio(
    "Navigation", 
    pages, 
    index=pages.index(st.session_state.app_page)
)

if selected_page != st.session_state.app_page:
    st.session_state.app_page = selected_page

st.sidebar.divider()
st.sidebar.caption("© 2026 BillScope. Household Expense Concierge.")

# ==========================================
# PAGE 0: HOME / LANDING PAGE
# ==========================================
if st.session_state.app_page == "Home":
    st.title("🔍 Welcome to BillScope")
    st.subheader("Beat the QLD 'Lazy Tax' on Your Household Bills")
    
    st.write(
        "Are you paying too much for electricity or internet? BillScope lets you upload your bill or "
        "enter your details to instantly benchmark your costs against regional averages and unlock real savings."
    )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚡ Electricity Audit")
        st.write("Compare your quarterly or monthly energy bills against QLD regional benchmark ranges.")
    with col2:
        st.markdown("### 🌐 Internet / NBN")
        st.write("Find out if your broadband plan is overpriced compared to current market averages.")
        
    st.divider()
    
    st.markdown("### How it works:")
    st.markdown("1. **Upload or Type:** Drop your PDF bill or enter your postcode and cost.\n"
                "2. **Instant Check:** Our engine detects if you're paying more than your neighbors.\n"
                "3. **Let Us Fix It:** Click to connect directly with your Living Expense Concierge.")
    
    if st.button("Start Bill Audit Now 🚀", type="primary"):
        st.session_state.app_page = "Instant Bill Auditor"
        st.rerun()

# ==========================================
# PAGE 1: INSTANT BILL AUDITOR
# ==========================================
elif st.session_state.app_page == "Instant Bill Auditor":
    st.title("⚡ Household Bill Auditor")
    st.subheader("Upload your bill or enter details to uncover potential savings.")

    # Choice of Input Method
    input_method = st.radio("Choose Input Method", ["Quick Manual Entry", "Upload Bill (PDF)"], horizontal=True)
    
    category = st.selectbox("Select Bill Type", ["Electricity", "Internet"])
    df = elec_df if category == "Electricity" else net_df
    
    user_postcode = 4557
    current_cost = 150.0
    billing_cycle = "Monthly"
    provider_name = "Unknown"
    nbn_tier = "NBN 50"  # Default tier
    
    # Standard Options
    internet_providers = [
        "Telstra", "Optus", "TPG", "Aussie Broadband", "Superloop", 
        "Vodafone", "Dodo", "iPrimus", "Exetel", "Leaptel", "AGL Energy", "Other"
    ]
    
    nbn_tiers = [
        "NBN 12", "NBN 25", "NBN 50", "NBN 100", 
        "NBN 250", "NBN 500", "NBN 1000", "NBN 2000"
    ]
    
    # --- METHOD A: QUICK MANUAL ENTRY ---
    if input_method == "Quick Manual Entry":
        st.markdown("#### Enter Bill Details")
        col1, col2 = st.columns(2)
        with col1:
            user_postcode = st.number_input("Your Postcode", min_value=1000, max_value=9999, value=4557, step=1)
            
            if category == "Internet":
                provider_name = st.selectbox("Current Internet Provider", internet_providers)
                nbn_tier = st.selectbox("NBN Speed Tier", nbn_tiers)
            else:
                provider_name = st.text_input("Current Provider", "e.g. Origin, AGL")
                
        with col2:
            if category == "Electricity":
                billing_cycle = st.selectbox("Billing Cycle", ["Monthly", "Quarterly"])
                current_cost = st.number_input("Current Cost ($)", min_value=0.0, value=150.0, step=5.0)
            else:
                billing_cycle = "Monthly"  # Force monthly for internet
                current_cost = st.number_input("Current Cost per Month ($)", min_value=0.0, value=85.0, step=5.0)

    # --- METHOD B: UPLOAD PDF BILL ---
    else:
        st.markdown("#### Upload PDF Bill")
        uploaded_file = st.file_uploader("Upload your recent bill statement", type=["pdf"])
        
        user_postcode = st.number_input("Confirm Your Postcode", min_value=1000, max_value=9999, value=4557, step=1)
        
        if category == "Internet":
            provider_name = st.selectbox("Confirm Internet Provider", internet_providers)
            nbn_tier = st.selectbox("Confirm NBN Speed Tier", nbn_tiers)
        
        if uploaded_file is not None:
            with st.spinner("Reading bill details..."):
                try:
                    with pdfplumber.open(uploaded_file) as pdf:
                        extracted_text = ""
                        for page in pdf.pages:
                            extracted_text += page.extract_text() or ""
                    st.success("Bill successfully scanned!")
                except Exception as ex:
                    st.warning(f"Could not automatically parse PDF text ({ex}). Please enter cost manually below.")
            
            if category == "Electricity":
                billing_cycle = st.selectbox("Billing Cycle", ["Monthly", "Quarterly"])
                current_cost = st.number_input("Confirmed Bill Cost ($ from statement)", min_value=0.0, value=200.0, step=5.0)
            else:
                current_cost = st.number_input("Confirmed Cost per Month ($ from statement)", min_value=0.0, value=85.0, step=5.0)
        else:
            st.info("Please upload a PDF file to begin extraction.")

    st.divider()

    # --- BENCHMARK EXECUTION & RESULTS ---
    if st.button("Run Savings Analysis 🔍", type="primary"):
        match = df[(df["postcode_start"] <= user_postcode) & (df["postcode_end"] >= user_postcode)]
        
        if not match.empty:
            region_name = match.iloc[0]["region"]
            benchmark = match.iloc[0]["benchmark_cost"]
            suggested_provider = match.iloc[0]["provider_example"]
            
            # Normalize to annual cost
            if category == "Electricity":
                monthly_user = current_cost / 3 if billing_cycle == "Quarterly" else current_cost
            else:
                monthly_user = current_cost  # Internet is monthly
                
            annual_user_cost = monthly_user * 12
            annual_benchmark_cost = benchmark * 12
            
            savings = annual_user_cost - annual_benchmark_cost
            
            st.subheader(f"📊 Audit Results for Postcode {user_postcode}")
            if category == "Internet":
                st.caption(f"Matched Region: **{region_name}** | Provider: **{provider_name}** | Tier: **{nbn_tier}**")
            else:
                st.caption(f"Matched Region: **{region_name}** | Provider: **{provider_name}**")
            
            col1, col2 = st.columns(2)
            col1.metric("Your Estimated Annual Cost", f"${annual_user_cost:,.2f}")
            col2.metric("Regional Benchmark Target", f"${annual_benchmark_cost:,.2f}")
            
            st.markdown("---")
            
            if savings > 0:
                st.error(f"⚠️ **Lazy Tax Detected!** You are paying approximately **${savings:,.2f} more per year** than the regional benchmark.")
                
                st.markdown("### Want us to slash this bill for you?")
                st.write("Click below to email your audit details directly to your Living Expense Concierge.")
                
                # Generate a secure mailto link with pre-filled details
                email_body_text = f"Hi Adam,\n\nI ran my {category} bill through BillScope and found potential savings!\n\n- Bill Type: {category}\n- Postcode: {user_postcode}\n- Provider: {provider_name}\n"
                if category == "Internet":
                    email_body_text += f"- NBN Tier: {nbn_tier}\n"
                email_body_text += f"- Current Cost: ${current_cost} per month\n- Estimated Annual Overspend: ~${savings:,.2f}/yr\n\nPlease help me look into cheaper alternatives."
                
                email_subject = urllib.parse.quote(f"Bill Audit Assistance Request - Postcode {user_postcode}")
                email_body = urllib.parse.quote(email_body_text)
                mailto_url = f"mailto:{CONCIERGE_EMAIL}?subject={email_subject}&body={email_body}"
                
                st.markdown(
                    f'<a href="{mailto_url}" target="_self"><button style="background-color:#FF4B4B; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">📧 Email Concierge to Fix My Bill</button></a>',
                    unsafe_allow_html=True
                )
            else:
                st.success(f"✅ **Great Job!** Your current rate is competitive and sitting at or below the regional benchmark.")
        else:
            st.warning("⚠️ Postcode not found within current QLD regional tracking ranges. Please double-check your postcode.")

# ==========================================
# PAGE 2: CONTACT CONCIERGE (CUSTOM NOTE FORM)
# ==========================================
elif app_page == "Contact Concierge":
    st.title("💬 Living Expense Concierge")
    st.subheader("Have custom bills or multiple items you want reviewed? Send a note directly.")
    
    st.write("Fill out the details below and click send to open your email client with your message pre-loaded for Adam.")
    
    with st.form("custom_concierge_form"):
        client_name = st.text_input("Your Name")
        client_phone = st.text_input("Phone Number")
        client_email = st.text_input("Your Email Address")
        bill_types = st.multiselect("What bills do you want help with?", ["Electricity", "Internet / NBN", "Mobile Phone", "Insurance", "Streaming / Subscriptions", "Other"])
        notes = st.text_area("Custom Note / Details", placeholder="e.g., My energy bill just jumped up and I want to see if I can switch to a cheaper provider.")
        
        submitted = st.form_submit_button("Generate & Send Email to Concierge 🚀")
        
        if submitted:
            if client_name and notes:
                subject = urllib.parse.quote(f"Custom Concierge Request from {client_name}")
                body = urllib.parse.quote(
                    f"Hi Adam,\n\nI would like help with my household expenses.\n\n"
                    f"Name: {client_name}\n"
                    f"Phone: {client_phone}\n"
                    f"Email: {client_email}\n"
                    f"Bills to review: {', '.join(bill_types)}\n\n"
                    f"Notes:\n{notes}"
                )
                custom_mailto = f"mailto:{CONCIERGE_EMAIL}?subject={subject}&body={body}"
                
                st.success("Ready! Click the button below to launch your email client and send your request:")
                st.markdown(
                    f'<a href="{custom_mailto}" target="_self"><button style="background-color:#0083B8; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">📬 Open Email Client & Send</button></a>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("Please provide at least your name and some notes before submitting.")

# ==========================================
# PAGE 3: TERMS & CONDITIONS
# ==========================================
elif app_page == "Terms & Conditions":
    st.title("⚖️ Terms of Service & Disclaimers")
    st.markdown("""
    ### 1. General Information Only
    BillScope is an independent software tool designed for general information, calculation, and benchmarking purposes only. It does not constitute personal financial, tax, or legal advice.
    
    ### 2. Concierge Services
    Our bill reduction concierge service assists with administrative guidance and comparison referrals. We do not provide credit assistance or mortgage products.
    
    ### 3. Limitation of Liability
    To the maximum extent permitted by law, BillScope accepts no liability for any financial loss or variation in utility contract pricing.
    """)
