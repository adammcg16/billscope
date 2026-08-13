import streamlit as st
import pandas as pd
import resend
import base64

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

# --- RESEND API CONFIGURATION (Using Streamlit Secrets) ---
try:
    resend.api_key = st.secrets["resend_api_key"]
except Exception:
    resend.api_key = ""

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
    
    # Strip whitespace from column names to guarantee reliable matching
    electricity.columns = electricity.columns.str.strip()
    internet.columns = internet.columns.str.strip()
    
    return electricity, internet

try:
    elec_df, net_df = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}. Please ensure 'billscope_tabs.xlsx' is uploaded to your GitHub repository.")
    st.stop()

# --- NAVIGATION SESSION STATE MANAGEMENT ---
if "app_page" not in st.session_state:
    st.session_state.app_page = "Home"

# --- CUSTOM CSS FOR MATCHING LOGO BACKGROUND COLOUR ---
st.markdown("""
    <style>
    /* Main App Background matched to logo's soft grey tone */
    .stApp {
        background-color: #F1F3F4;
        color: #1F2937;
    }
    
    /* Clean Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #E8ECEE !important;
        border-right: 1px solid #D1D5DB;
    }
    [data-testid="stSidebar"] .stRadio label p {
        color: #1F2937 !important;
        font-weight: 500;
    }
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] caption {
        color: #4B5563 !important;
    }

    h1, h2, h3 {
        color: #0F172A !important;
    }
    p, label, span {
        color: #334155 !important;
    }
    .hero-container {
        padding: 2.5rem 1.5rem;
        background: linear-gradient(135deg, #E2E8F0 0%, #F1F3F4 100%);
        border: 1px solid #D1D5DB;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        height: 100%;
    }
    .brand-box {
        background-color: #FFFFFF;
        border-left: 4px solid #2563EB;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGO HELPER ---
def render_top_logo():
    try:
        with open("logo.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 1.5rem; max-width: 320px; margin-left: auto; margin-right: auto;">
                <img src="data:image/png;base64,{encoded_string}" style="max-width: 100%; height: auto;" />
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        st.markdown("<h2 style='text-align: center; color: #2563EB;'>🔍 BILLSCOPE</h2>", unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
try:
    with open("logo.png", "rb") as image_file:
        encoded_sidebar_logo = base64.b64encode(image_file.read()).decode()
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{encoded_sidebar_logo}" style="max-width: 100%; height: auto;" />
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
# PAGE 0: HOME / LANDING PAGE
# ==========================================
if st.session_state.app_page == "Home":
    render_top_logo()
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Immediate Problem & CTA First
    st.markdown(
        """
        <div class="hero-container">
            <h1 style='font-size: 2.2rem; font-weight: 800; letter-spacing: -0.025em; margin-bottom: 1rem;'>
                Are you paying too much for your <br><span style='color: #2563EB;'>household bills?</span>
            </h1>
            <p style='font-size: 1.1rem; color: #475569; max-width: 600px; margin: 0 auto 1.5rem auto;'>
                Find out in under 2 minutes. Enter what you're currently paying and we’ll compare your bills with households in your area.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("Check my bills →", type="primary", use_container_width=True):
            st.session_state.app_page = "Instant Bill Auditor"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Value Proposition / Trust Section ("Why use BillScope?")
    st.markdown("### Why use BillScope?")
    st.write(
        "Comparison sites make you do all the heavy lifting: entering tedious details, comparing dozens of confusing plans, "
        "working out pricing structures, and dealing with providers. **Tell us what you’re paying. We’ll do the research.**"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### How BillScope Works")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h4>1. Tell us what you’re paying</h4>
                <p style='font-size: 0.85rem; color: #475569;'>Enter your current bill and a few details about your household.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h4>2. We find the opportunity</h4>
                <p style='font-size: 0.85rem; color: #475569;'>BillScope compares your costs with relevant regional benchmarks.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h4>3. We do the legwork</h4>
                <p style='font-size: 0.85rem; color: #475569;'>If there’s a worthwhile saving, our concierge researches your options for you.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "💡 **If we identify a worthwhile saving, our Living Expense Concierge can research the best options for you.** "
        "If we can't find savings, our service is completely free."
    )

# ==========================================
# PAGE 1: INSTANT BILL AUDITOR
# ==========================================
elif st.session_state.app_page == "Instant Bill Auditor":
    render_top_logo()
    st.title("⚡ Household Bill Auditor")
    st.subheader("Enter what you're currently paying to identify potential savings in your area.")

    category = st.selectbox("Select Bill Type", ["Electricity", "Internet"])
    
    internet_providers = [
        "Telstra", "Optus", "TPG", "Aussie Broadband", "Superloop", 
        "Vodafone", "Dodo", "iPrimus", "Exetel", "Leaptel", "AGL Energy", "Other"
    ]
    nbn_tiers = ["NBN 25", "NBN 50", "NBN 100", "NBN 250", "NBN 500", "NBN 750", "NBN 1000"]
    
    st.markdown("#### Initial Bill Details")
    col1, col2 = st.columns(2)
    with col1:
        user_postcode = st.number_input("Your Postcode", min_value=1000, max_value=9999, value=4000, step=1)
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

    st.divider()

    if "audit_run" not in st.session_state:
        st.session_state.audit_run = False

    if st.button("Run Savings Analysis 🔍", type="primary"):
        st.session_state.audit_run = True
        st.session_state.audited_category = category
        st.session_state.audited_postcode = user_postcode
        st.session_state.audited_provider = provider_name
        st.session_state.audited_nbn_tier = nbn_tier if category == "Internet" else "N/A"
        st.session_state.audited_current_cost = current_cost
        
        monthly_user = current_cost / 3 if (category == "Electricity" and billing_cycle == "Quarterly") else current_cost
        
        if category == "Electricity":
            match = elec_df[(elec_df["postcode start"] <= user_postcode) & (elec_df["postcode end"] >= user_postcode)]
            if not match.empty:
                region_name = match.iloc[0]["region"]
                benchmark_monthly = match.iloc[0]["benchmark_cost"]
                rec_provider = match.iloc[0]["top_provider"]
                
                st.session_state.audited_savings = (monthly_user * 12) - (benchmark_monthly * 12)
                st.session_state.audited_user_cost = monthly_user * 12
                st.session_state.audited_benchmark_cost = benchmark_monthly * 12
                st.session_state.audited_region = region_name
                st.session_state.audited_top_provider = rec_provider if pd.notna(rec_provider) else None
            else:
                st.session_state.audited_savings = None
        else:  # Internet
            match = net_df[(net_df["postcode start"] <= user_postcode) & (net_df["postcode end"] >= user_postcode)]
            if not match.empty:
                region_name = match.iloc[0]["region"]
                rec_provider = match.iloc[0]["top_provider"]
                
                tier_col = nbn_tier.lower().replace(" ", "_") + "_cost"
                if tier_col in match.columns and pd.notna(match.iloc[0][tier_col]):
                    benchmark_monthly = match.iloc[0][tier_col]
                else:
                    benchmark_monthly = match.iloc[0]["nbn_50_cost"]
                
                st.session_state.audited_savings = (monthly_user * 12) - (benchmark_monthly * 12)
                st.session_state.audited_user_cost = monthly_user * 12
                st.session_state.audited_benchmark_cost = benchmark_monthly * 12
                st.session_state.audited_region = region_name
                st.session_state.audited_top_provider = rec_provider if pd.notna(rec_provider) else None
            else:
                st.session_state.audited_savings = None

    if st.session_state.audit_run:
        if st.session_state.audited_savings is not None:
            savings = st.session_state.audited_savings
            monthly_saving = savings / 12
            
            # Determine Opportunity Rating
            if savings >= 400:
                opp_rating = "🔴 High opportunity (Potential saving: $400+/year — Definitely worth investigating.)"
            elif savings >= 150:
                opp_rating = "🟠 Moderate opportunity (Potential saving: $150–$400/year — There may be worthwhile alternatives.)"
            else:
                opp_rating = "🟢 Low opportunity (Potential saving: <$150/year — You’re already relatively competitive.)"

            st.subheader(f"Audit Results for Postcode {st.session_state.audited_postcode}")
            
            if savings > 0:
                st.markdown(
                    f"""
                    <div style="background-color: #FEF2F2; border: 1px solid #FCA5A5; padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1.5rem;">
                        <h3 style="color: #991B1B; margin-bottom: 0.2rem;">You could be paying too much</h3>
                        <p style="font-size: 0.95rem; color: #7F1D1D; margin-bottom: 0.5rem;">Estimated potential saving</p>
                        <h1 style="color: #DC2626; font-size: 2.5rem; font-weight: 800; margin: 0;">${savings:,.0f}/year</h1>
                        <p style="color: #6B7280; font-size: 1.1rem; font-weight: 600; margin-top: 0.2rem;">(~${monthly_saving:,.0f}/month)</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="background-color: #F0FDF4; border: 1px solid #86EFAC; padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1.5rem;">
                        <h3 style="color: #166534; margin-bottom: 0.2rem;">You're on a competitive rate!</h3>
                        <p style="font-size: 0.95rem; color: #14532D;">Your current bill is sitting at or below similar households in your region.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Context comparison & Opportunity rating
            st.write(f"You’re currently spending approximately **${st.session_state.audited_user_cost:,.0f}/year**, compared with what similar households pay of **${st.session_state.audited_benchmark_cost:,.0f}/year**.")
            st.info(f"**Opportunity Rating:** {opp_rating}")
            
            st.caption("We’ll investigate whether that saving is actually available to you.")
            
            # Provider Insight (with fallback handled gracefully)
            if st.session_state.audited_top_provider:
                st.markdown(
                    f"""
                    <div class="brand-box">
                        <strong>💡 BillScope Insight</strong><br>
                        In your region, top households frequently review plans with providers like <strong>{st.session_state.audited_top_provider}</strong>.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="brand-box">
                        <strong>💡 BillScope Insight</strong><br>
                        There may be cheaper options available in your area. We’ll research the current market for you.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Lazy tax soft callout
            if savings > 0:
                st.warning("💰 **Potential Lazy Tax Detected:** The extra money households often spend simply because they haven’t had the time to review their current bills.")

            st.markdown("---")
            
            if savings > 0:
                st.markdown("### Let us do the research for you")
                st.write("Don’t spend your weekend comparing plans. Give us a few details and we’ll investigate your current arrangement and look for better options available to you.")
                
                with st.form("qualified_lead_form"):
                    st.markdown("#### Tell us a bit more about your setup")
                    
                    col_f1, col_f2 = st.columns(2)
                    with col_f1:
                        client_name = st.text_input("Your Full Name")
                        client_mobile = st.text_input("Mobile Number")
                        client_email = st.text_input("Email Address")
                    with col_f2:
                        contract_status = st.selectbox("Contract Status / End Date", ["Unknown", "Out of contract", "In contract (< 6 months left)", "In contract (> 6 months left)"])
                        if st.session_state.audited_category == "Electricity":
                            has_solar = st.selectbox("Solar Panels?", ["No", "Yes", "Not sure"])
                            has_ev = st.selectbox("Electric Vehicle (EV)?", ["No", "Yes"])
                            has_pool = st.selectbox("Swimming Pool?", ["No", "Yes"])
                            occupants = st.number_input("Number of People in Household", min_value=1, max_value=10, value=2)
                        else:
                            data_usage = st.selectbox("Data Allowance", ["Unlimited", "Limited"])
                            download_speed = st.text_input("Current Speed / Plan details", "e.g. NBN 50")
                    
                    user_notes = st.text_area("Additional Notes (Optional)", placeholder="Any other details about your current bill...")
                    
                    submitted = st.form_submit_button("Have BillScope investigate my bills 🚀")
                    
                    if submitted:
                        if client_name and client_mobile and client_email:
                            email_subject = f"New Qualified Lead: {client_name} (Postcode {st.session_state.audited_postcode})"
                            
                            extra_details = ""
                            if st.session_state.audited_category == "Electricity":
                                extra_details = f"Solar: {has_solar}\nEV: {has_ev}\nPool: {has_pool}\nOccupants: {occupants}\n"
                            else:
                                extra_details = f"Data Allowance: {data_usage}\nPlan/Speed: {download_speed}\n"

                            email_body = (
                                f"A qualified audit request has been submitted through BillScope:\n\n"
                                f"--- Client Details ---\n"
                                f"Name: {client_name}\n"
                                f"Mobile: {client_mobile}\n"
                                f"Email: {client_email}\n\n"
                                f"--- Audit & Household Info ---\n"
                                f"Bill Type: {st.session_state.audited_category}\n"
                                f"Postcode: {st.session_state.audited_postcode}\n"
                                f"Provider: {st.session_state.audited_provider}\n"
                                f"NBN Tier: {st.session_state.audited_nbn_tier}\n"
                                f"Current Cost: ${st.session_state.audited_current_cost}\n"
                                f"Estimated Potential Saving: ${savings:,.0f}/yr (~${monthly_saving:,.0f}/mo)\n"
                                f"Contract Status: {contract_status}\n"
                                f"{extra_details}\n"
                                f"--- Client Notes ---\n"
                                f"{user_notes}"
                            )
                            
                            with st.spinner("Dispatching request..."):
                                success = send_resend_email(email_subject, email_body)
                                if success:
                                    st.success("🎉 Success! Your concierge has received your details and will begin investigating your options.")
                        else:
                            st.warning("Please fill in your Name, Mobile, and Email address.")
        else:
            st.warning("⚠️ Postcode not found within current QLD regional tracking ranges. Please double-check your postcode.")

# ==========================================
# PAGE 2: CONTACT CONCIERGE (GENERAL FORM)
# ==========================================
elif st.session_state.app_page == "Contact Concierge":
    render_top_logo()
    st.title("💬 Living Expense Concierge")
    st.subheader("Don’t spend your weekend comparing plans. We’ll do the research for you.")
    
    with st.form("general_concierge_form"):
        client_name = st.text_input("Your Name")
        client_mobile = st.text_input("Mobile Number")
        client_email = st.text_input("Email Address")
        bill_types = st.multiselect("What bills do you want help with?", ["Electricity", "Internet / NBN", "Mobile Phone", "Insurance", "Streaming / Subscriptions", "Other"])
        notes = st.text_area("Notes / Details", placeholder="e.g., My energy and internet bills are too high, please help me review them.")
        
        submitted = st.form_submit_button("Have BillScope investigate my bills 🚀")
        
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
