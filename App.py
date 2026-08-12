import streamlit as st
import pandas as pd
import pdfplumber
import resend
import base64

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

# --- RESEND API CONFIGURATION (Using Streamlit Secrets) ---
resend.api_key = st.secrets["resend_api_key"]
RECEIVER_EMAIL = "adammcg_16@hotmail.com"

def send_resend_email(subject, body):
    """Sends an email notification directly via Resend API to your verified inbox."""
    try:
        params = {
            "from": "BillScope <onboarding@resend.dev>", 
            "to": [RECEIVER_EMAIL],
            "subject": subject,
            "text": body,
        }
        resend.Emails.send(params)
        return True
    except Exception as e:
        st.error(f"Email Dispatch Error: {e}")
        return False

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

# --- CUSTOM CSS FOR DARK MODE & SIDEBAR READABILITY ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    /* Fixed Sidebar Styling for Perfect Readability */
    [data-testid="stSidebar"] {
        background-color: #1F2937 !important;
        border-right: 1px solid #374151;
    }
    [data-testid="stSidebar"] .stRadio label p {
        color: #FFFFFF !important;
        font-weight: 500;
    }
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] caption {
        color: #E5E7EB !important;
    }

    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    p, label, span {
        color: #D1D5DB !important;
    }
    .hero-container {
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #1E1B4B 0%, #0B0F19 100%);
        border: 1px solid #1F2937;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGO HELPER WITH DARK MODE BACKGROUND BLENDING ---
def render_top_logo():
    try:
        with open("logo.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Wrapped in a subtle matching dark card container with rounded corners so the white box matches the theme seamlessly
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 1.5rem; padding: 12px; background-color: #111827; border: 1px solid #1F2937; border-radius: 16px; max-width: 320px; margin-left: auto; margin-right: auto;">
                <img src="data:image/png;base64,{encoded_string}" style="max-width: 100%; height: auto; border-radius: 8px;" />
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        st.markdown("<h2 style='text-align: center; color: #3B82F6;'>🔍 BILLSCOPE</h2>", unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
try:
    with open("logo.png", "rb") as image_file:
        encoded_sidebar_logo = base64.b64encode(image_file.read()).decode()
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 1rem; padding: 8px; background-color: #111827; border-radius: 12px; border: 1px solid #374151;">
            <img src="data:image/png;base64,{encoded_sidebar_logo}" style="max-width: 100%; height: auto; border-radius: 6px;" />
        </div>
        """,
        unsafe_allow_html=True
    )
except Exception:
    st.sidebar.title("🔍 BillScope")

pages = ["Home", "Instant Bill Auditor", "Contact Concierge", "Terms & Conditions"]

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
# PAGE 0: HOME / LANDING PAGE (SAAS REDESIGN)
# ==========================================
if st.session_state.app_page == "Home":
    render_top_logo()
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-container">
            <h1 style='font-size: 2.2rem; font-weight: 800; letter-spacing: -0.025em; margin-bottom: 1rem;'>
                Take Control of Your Bills & <br><span style='color: #3B82F6;'>Start Saving Money Instantly.</span>
            </h1>
            <p style='font-size: 1.1rem; color: #9CA3AF; max-width: 600px; margin: 0 auto 1.5rem auto;'>
                BILLSCOPE reviews your monthly expenses, finds better deals, and negotiates lower rates on your behalf. Effortless savings, guaranteed.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.success(
        "✨ **Short on time?** Don't spend hours comparing providers and hunting down better deals. "
        "Let our Living Expense Concierge handle the hard work for you. **If we can't save you money, our service is completely free.**"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### How BILLSCOPE Works")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h4>1. Upload Bills</h4>
                <p style='font-size: 0.85rem; color: #9CA3AF;'>Securely upload your bills via PDF or quick manual form.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h4>2. We Analyze</h4>
                <p style='font-size: 0.85rem; color: #9CA3AF;'>Engine scans for savings, pricing padding, and regional discrepancies.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h4>3. You Save</h4>
                <p style='font-size: 0.85rem; color: #9CA3AF;'>Get notified of lower rates and approve your real household savings.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("Secure My Savings 🚀", type="primary", use_container_width=True):
            st.session_state.app_page = "Instant Bill Auditor"
            st.rerun()

# ==========================================
# PAGE 1: INSTANT BILL AUDITOR
# ==========================================
elif st.session_state.app_page == "Instant Bill Auditor":
    render_top_logo()
    st.title("⚡ Household Bill Auditor")
    st.subheader("Upload your bill or enter details to uncover potential savings.")

    input_method = st.radio("Choose Input Method", ["Quick Manual Entry", "Upload Bill (PDF)"], horizontal=True)
    
    category = st.selectbox("Select Bill Type", ["Electricity", "Internet"])
    df = elec_df if category == "Electricity" else net_df
    
    user_postcode = 4557
    current_cost = 150.0
    billing_cycle = "Monthly"
    provider_name = "Unknown"
    nbn_tier = "NBN 50"
    
    internet_providers = [
        "Telstra", "Optus", "TPG", "Aussie Broadband", "Superloop", 
        "Vodafone", "Dodo", "iPrimus", "Exetel", "Leaptel", "AGL Energy", "Other"
    ]
    
    nbn_tiers = [
        "NBN 12", "NBN 25", "NBN 50", "NBN 100", 
        "NBN 250", "NBN 500", "NBN 1000", "NBN 2000"
    ]
    
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
                billing_cycle = "Monthly"
                current_cost = st.number_input("Current Cost per Month ($)", min_value=0.0, value=85.0, step=5.0)

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

    if "audit_run" not in st.session_state:
        st.session_state.audit_run = False

    if st.button("Run Savings Analysis 🔍", type="primary"):
        st.session_state.audit_run = True
        st.session_state.audited_category = category
        st.session_state.audited_postcode = user_postcode
        st.session_state.audited_provider = provider_name
        st.session_state.audited_nbn_tier = nbn_tier
        st.session_state.audited_current_cost = current_cost
        
        match = df[(df["postcode_start"] <= user_postcode) & (df["postcode_end"] >= user_postcode)]
        if not match.empty:
            region_name = match.iloc[0]["region"]
            benchmark = match.iloc[0]["benchmark_cost"]
            monthly_user = current_cost / 3 if (category == "Electricity" and billing_cycle == "Quarterly") else current_cost
            st.session_state.audited_savings = (monthly_user * 12) - (benchmark * 12)
            st.session_state.audited_user_cost = monthly_user * 12
            st.session_state.audited_benchmark_cost = benchmark * 12
            st.session_state.audited_region = region_name
        else:
            st.session_state.audited_savings = None

    if st.session_state.audit_run:
        if st.session_state.audited_savings is not None:
            st.subheader(f"📊 Audit Results for Postcode {st.session_state.audited_postcode}")
            if st.session_state.audited_category == "Internet":
                st.caption(f"Matched Region: **{st.session_state.audited_region}** | Provider: **{st.session_state.audited_provider}** | Tier: **{st.session_state.audited_nbn_tier}**")
            else:
                st.caption(f"Matched Region: **{st.session_state.audited_region}** | Provider: **{st.session_state.audited_provider}**")
            
            col1, col2 = st.columns(2)
            col1.metric("Your Estimated Annual Cost", f"${st.session_state.audited_user_cost:,.2f}")
            col2.metric("Regional Benchmark Target", f"${st.session_state.audited_benchmark_cost:,.2f}")
            
            st.markdown("---")
            
            if st.session_state.audited_savings > 0:
                st.error(f"⚠️ **Lazy Tax Detected!** You are paying approximately **${st.session_state.audited_savings:,.2f} more per year** than the regional benchmark.")
                
                st.markdown("### Want us to slash this bill for you?")
                st.write("Fill out your details below to send your audit request straight to your living expense concierge.")
                
                with st.form("audit_enquiry_form"):
                    client_name = st.text_input("Your Full Name")
                    client_mobile = st.text_input("Mobile Number")
                    client_email = st.text_input("Email Address")
                    user_notes = st.text_area("Notes / What you want reviewed", value=f"Please help me review my {st.session_state.audited_category} bill. Current cost is ${st.session_state.audited_current_cost} with {st.session_state.audited_provider}.")
                    
                    submitted = st.form_submit_button("Send Request to Your Living Expense Concierge 🚀")
                    
                    if submitted:
                        if client_name and client_mobile and client_email:
                            email_subject = f"New BillScope Lead: {client_name} (Postcode {st.session_state.audited_postcode})"
                            email_body = (
                                f"A new audit request has been submitted through BillScope:\n\n"
                                f"--- Client Details ---\n"
                                f"Name: {client_name}\n"
                                f"Mobile: {client_mobile}\n"
                                f"Email: {client_email}\n\n"
                                f"--- Audit Information ---\n"
                                f"Bill Type: {st.session_state.audited_category}\n"
                                f"Postcode: {st.session_state.audited_postcode}\n"
                                f"Provider: {st.session_state.audited_provider}\n"
                                f"NBN Tier: {st.session_state.audited_nbn_tier if st.session_state.audited_category == 'Internet' else 'N/A'}\n"
                                f"Current Cost: ${st.session_state.audited_current_cost}\n"
                                f"Estimated Savings: ${st.session_state.audited_savings:,.2f}/yr\n\n"
                                f"--- Client Notes ---\n"
                                f"{user_notes}"
                            )
                            
                            with st.spinner("Dispatching email..."):
                                success = send_resend_email(email_subject, email_body)
                                if success:
                                    st.success("🎉 Success! Your enquiry has been sent straight to your living expense concierge.")
                        else:
                            st.warning("Please fill in your Name, Mobile, and Email address.")
            else:
                st.success(f"✅ **Great Job!** Your current rate is competitive and sitting at or below the regional benchmark.")
        else:
            st.warning("⚠️ Postcode not found within current QLD regional tracking ranges. Please double-check your postcode.")

# ==========================================
# PAGE 2: CONTACT CONCIERGE (GENERAL FORM)
# ==========================================
elif st.session_state.app_page == "Contact Concierge":
    render_top_logo()
    st.title("💬 Living Expense Concierge")
    st.subheader("Have multiple bills or custom items you want reviewed? Send a note directly.")
    
    with st.form("general_concierge_form"):
        client_name = st.text_input("Your Name")
        client_mobile = st.text_input("Mobile Number")
        client_email = st.text_input("Email Address")
        bill_types = st.multiselect("What bills do you want help with?", ["Electricity", "Internet / NBN", "Mobile Phone", "Insurance", "Streaming / Subscriptions", "Other"])
        notes = st.text_area("Notes / Details", placeholder="e.g., My energy and internet bills are too high, please help me review them.")
        
        submitted = st.form_submit_button("Send General Enquiry 🚀")
        
        if submitted:
            if client_name and client_mobile and notes:
                email_subject = f"General BillScope Inquiry from {client_name}"
                email_body = (
                    f"Name: {client_name}\n"
                    f"Mobile: {client_mobile}\n"
                    f"Email: {client_email}\n"
                    f"Target Bills: {', '.join(bill_types)}\n\n"
                    f"Notes:\n{notes}"
                )
                
                with st.spinner("Dispatching email..."):
                    success = send_resend_email(email_subject, email_body)
                    if success:
                        st.success("🎉 Success! Your enquiry has been sent straight to your living expense concierge.")
            else:
                st.warning("Please fill in your Name, Mobile, and Notes before submitting.")

# ==========================================
# PAGE 3: TERMS & CONDITIONS
# ==========================================
elif st.session_state.app_page == "Terms & Conditions":
    render_top_logo()
    st.title("⚖️ Terms of Service & Disclaimers")
    st.markdown("""
    ### 1. General Information Only
    BillScope is an independent software tool designed for general information, calculation, and benchmarking purposes only. It does not constitute personal financial, tax, or legal advice.
    
    ### 2. Concierge Services
    Our bill reduction concierge service assists with administrative guidance and comparison referrals. We do not provide credit assistance or mortgage products.
    
    ### 3. Limitation of Liability
    To the maximum extent permitted by law, BillScope accepts no liability for any financial loss or variation in utility contract pricing.
    """)
