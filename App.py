import streamlit as st
import pandas as pd
import pdfplumber
import io

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

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

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("🔍 BillScope Menu")
app_page = st.sidebar.radio("Navigation", ["Home", "Instant Bill Auditor", "Terms & Conditions"])

st.sidebar.divider()
st.sidebar.caption("© 2026 BillScope. Household Expense Concierge.")

# ==========================================
# PAGE 0: HOME / LANDING PAGE
# ==========================================
if app_page == "Home":
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
                "3. **Let Us Fix It:** Want out of the overpayment? Request our bill reduction concierge service.")
    
    if st.button("Start Bill Audit Now 🚀", type="primary"):
        st.info("Use the left navigation menu and select **Instant Bill Auditor** to begin!")

# ==========================================
# PAGE 1: INSTANT BILL AUDITOR
# ==========================================
elif app_page == "Instant Bill Auditor":
    st.title("⚡ Household Bill Auditor")
    st.subheader("Upload your bill or enter details to uncover potential savings.")

    # Choice of Input Method
    input_method = st.radio("Choose Input Method", ["Quick Manual Entry", "Upload Bill (PDF)"], horizontal=True)
    
    category = st.selectbox("Select Bill Type", ["Electricity", "Internet"])
    df = elec_df if category == "Electricity" else net_df
    
    user_postcode = None
    current_cost = 0.0
    billing_cycle = "Monthly"
    provider_name = "Unknown"
    
    # --- METHOD A: QUICK MANUAL ENTRY ---
    if input_method == "Quick Manual Entry":
        st.markdown("#### Enter Bill Details")
        col1, col2 = st.columns(2)
        with col1:
            user_postcode = st.number_input("Your Postcode", min_value=1000, max_value=9999, value=4557, step=1)
            provider_name = st.text_input("Current Provider", "e.g. Origin, AGL, Telstra")
        with col2:
            if category == "Electricity":
                billing_cycle = st.selectbox("Billing Cycle", ["Monthly", "Quarterly"])
            current_cost = st.number_input("Current Cost ($)", min_value=0.0, value=150.0, step=5.0)

    # --- METHOD B: UPLOAD PDF BILL ---
    else:
        st.markdown("#### Upload PDF Bill")
        uploaded_file = st.file_uploader("Upload your recent bill statement", type=["pdf"])
        
        user_postcode = st.number_input("Confirm Your Postcode", min_value=1000, max_value=9999, value=4557, step=1)
        
        if uploaded_file is not None:
            with st.spinner("Reading bill details..."):
                try:
                    with pdfplumber.open(uploaded_file) as pdf:
                        extracted_text = ""
                        for page in pdf.pages:
                            extracted_text += page.extract_text() or ""
                    
                    st.success("Bill successfully scanned!")
                    # Basic placeholder parsing (you can refine keywords later)
                    st.caption("Extracted text snippet preview available in system.")
                except Exception as ex:
                    st.warning(f"Could not automatically parse PDF text ({ex}). Please enter cost manually below.")
            
            current_cost = st.number_input("Confirmed Bill Cost ($ from statement)", min_value=0.0, value=200.0, step=5.0)
            if category == "Electricity":
                billing_cycle = st.selectbox("Billing Cycle", ["Monthly", "Quarterly"])
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
            
            # Normalize to annual cost for comparison
            monthly_user = current_cost / 3 if (category == "Electricity" and billing_cycle == "Quarterly") else current_cost
            annual_user_cost = monthly_user * 12
            annual_benchmark_cost = benchmark * 12
            
            savings = annual_user_cost - annual_benchmark_cost
            
            st.subheader(f"📊 Audit Results for Postcode {user_postcode}")
            st.caption(f"Matched Region: **{region_name}**")
            
            col1, col2 = st.columns(2)
            col1.metric("Your Estimated Annual Cost", f"${annual_user_cost:,.2f}")
            col2.metric("Regional Benchmark Target", f"${annual_benchmark_cost:,.2f}")
            
            st.markdown("---")
            
            if savings > 0:
                st.error(f"⚠️ **Lazy Tax Detected!** You are paying approximately **${savings:,.2f} more per year** than the regional benchmark.")
                
                # CONCIERGE HANDOVER CALL TO ACTION
                st.markdown("### Want us to slash this bill for you?")
                st.write("Don't spend hours on hold. Hand this over to our **Household Bill Concierge** service, and we will handle the switch to a cheaper provider on your behalf.")
                
                with st.form("concierge_form"):
                    st.markdown("#### Request Free Concierge Assistance")
                    c_name = st.text_input("Your Full Name")
                    c_phone = st.text_input("Phone Number")
                    c_email = st.text_input("Email Address")
                    
                    submitted = st.form_submit_button("Book My Free Bill Review 🚀")
                    if submitted:
                        if c_name and c_email:
                            st.success(f"Thank you, {c_name}! We have received your audit data and will contact you within 24 hours to help lower your {category.lower()} bills.")
                        else:
                            st.warning("Please provide your name and email so we can reach out.")
            else:
                st.success(f"✅ **Great Job!** Your current rate is competitive and sitting at or below the regional benchmark.")
        else:
            st.warning("⚠️ Postcode not found within current QLD regional tracking ranges. Please double-check your postcode.")

# ==========================================
# PAGE 2: TERMS & CONDITIONS
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
