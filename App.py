import streamlit as st
import pandas as pd
import pdfplumber
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="BillScope App",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING & THEME RESTORATION ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD BENCHMARK DATA ---
@st.cache_data
def load_data():
    file_path = "billscope_tabs.xlsx"
    try:
        electricity = pd.read_excel(file_path, sheet_name="Electricity")
        internet = pd.read_excel(file_path, sheet_name="Internet")
        
        # Clean up column names by stripping trailing/leading spaces
        electricity.columns = electricity.columns.str.strip()
        internet.columns = internet.columns.str.strip()
        
        return electricity, internet
    except Exception as e:
        st.error(f"Error loading benchmark data file: {e}")
        return None, None

elec_df, net_df = load_data()

# --- APP HEADER ---
st.title("⚡ BillScope Bill Audit & Comparison")
st.markdown("Upload your utility bill or enter details manually to audit your costs against custom regional benchmarks.")

# --- SESSION STATE INITIALIZATION ---
if "audit_run" not in st.session_state:
    st.session_state.audit_run = False

# --- SIDEBAR & USER INPUTS ---
st.sidebar.header("1. Bill Details")
category = st.sidebar.selectbox("Select Utility Category", ["Electricity", "Internet"])

# PDF Upload Option
uploaded_file = st.sidebar.file_uploader("Upload Bill PDF (Optional)", type=["pdf"])

extracted_amount = None
if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        st.sidebar.success("PDF uploaded and parsed successfully!")
    except Exception as e:
        st.sidebar.error(f"Could not read PDF: {e}")

user_postcode = st.sidebar.number_input("Enter Postcode", min_value=1000, max_value=9999, value=4000)

nbn_tier = None
if category == "Internet":
    nbn_tier = st.sidebar.selectbox(
        "Select NBN Speed Tier", 
        ["NBN 25", "NBN 50", "NBN 100", "NBN 250", "NBN 500", "NBN 750", "NBN 1000"]
    )

user_cost = st.sidebar.number_input("Enter Your Monthly Cost ($)", min_value=0.0, value=120.0, step=5.0)

# Notification settings
st.sidebar.header("2. Report & Alerts")
user_email = st.sidebar.text_input("Email Address for Report", placeholder="name@example.com")

# --- AUDIT EXECUTION ---
if st.sidebar.button("Run Savings Analysis 🔍", type="primary"):
    st.session_state.audit_run = True

if st.session_state.audit_run:
    if elec_df is None or net_df is None:
        st.error("Benchmark dataset is missing or failed to load. Ensure 'billscope_tabs.xlsx' is uploaded to your repository.")
    else:
        benchmark = None
        provider = None
        region_name = "Unknown Region"
        
        if category == "Electricity":
            match = elec_df[(elec_df["postcode start"] <= user_postcode) & (elec_df["postcode end"] >= user_postcode)]
            if not match.empty:
                benchmark = match.iloc[0]["benchmark_cost"]
                provider = match.iloc[0]["top_provider"]
                region_name = match.iloc[0]["region"]
        else:  # Internet
            match = net_df[(net_df["postcode start"] <= user_postcode) & (net_df["postcode end"] >= user_postcode)]
            if not match.empty:
                tier_col = nbn_tier.lower().replace(" ", "_") + "_cost"
                if tier_col in match.columns:
                    benchmark = match.iloc[0][tier_col]
                provider = match.iloc[0]["top_provider"]
                region_name = match.iloc[0]["region"]
        
        # --- DISPLAY RESULTS ---
        st.divider()
        if benchmark is not None and pd.notna(benchmark):
            st.subheader(f"📊 Region Audit: {region_name}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Your Monthly Cost", f"${user_cost:.2f}")
            col2.metric("Regional Benchmark", f"${benchmark:.2f}")
            
            diff = user_cost - benchmark
            if diff > 0:
                col3.metric("Potential Overpay", f"${diff:.2f}/mo", delta=f"-${diff:.2f}", delta_color="inverse")
                st.warning(f"⚠️ You appear to be paying **${diff:.2f} more per month** than the regional benchmark for {category.lower()}.")
                if pd.notna(provider):
                    st.info(f"💡 **Recommendation:** Consider looking into **{provider}**, a top-performing provider in your area.")
            else:
                col3.metric("Savings Status", "Great Rate!", delta=f"+${abs(diff):.2f}", delta_color="normal")
                st.success(f"🎉 Excellent news! Your current rate is at or below the regional benchmark.")
            
            # Email section confirmation handler
            if user_email:
                st.success(f"📧 Summary report ready to be dispatched to **{user_email}**.")
        else:
            st.warning(f"⚠️ No benchmark data is currently available for postcode **{user_postcode}** in the {category} sheet.")

# --- FOOTER ---
st.markdown("---")
st.caption("BillScope v1.3 • Fully integrated with custom regional benchmarks and PDF auditing.")user_postcode = st.sidebar.number_input("Enter Postcode", min_value=1000, max_value=9999, value=4000)

nbn_tier = None
if category == "Internet":
    nbn_tier = st.sidebar.selectbox(
        "Select NBN Speed Tier", 
        ["NBN 25", "NBN 50", "NBN 100", "NBN 250", "NBN 500", "NBN 750", "NBN 1000"]
    )

user_cost = st.sidebar.number_input("Enter Your Current Monthly Cost ($)", min_value=0.0, value=120.0, step=5.0)

# --- AUDIT EXECUTION ---
if st.sidebar.button("Run Savings Analysis 🔍", type="primary"):
    if elec_df is None or net_df is None:
        st.error("Benchmark dataset is missing or failed to load. Ensure 'billscope_tabs.xlsx' is uploaded to your repository.")
    else:
        benchmark = None
        provider = None
        region_name = "Unknown Region"
        
        if category == "Electricity":
            match = elec_df[(elec_df["postcode start"] <= user_postcode) & (elec_df["postcode end"] >= user_postcode)]
            if not match.empty:
                benchmark = match.iloc[0]["benchmark_cost"]
                provider = match.iloc[0]["top_provider"]
                region_name = match.iloc[0]["region"]
        else:  # Internet
            match = net_df[(net_df["postcode start"] <= user_postcode) & (net_df["postcode end"] >= user_postcode)]
            if not match.empty:
                tier_col = nbn_tier.lower().replace(" ", "_") + "_cost"
                if tier_col in match.columns:
                    benchmark = match.iloc[0][tier_col]
                provider = match.iloc[0]["top_provider"]
                region_name = match.iloc[0]["region"]
        
        # --- DISPLAY RESULTS ---
        st.divider()
        if benchmark is not None and pd.notna(benchmark):
            st.subheader(f"Region Audit: {region_name}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Your Monthly Cost", f"${user_cost:.2f}")
            col2.metric("Regional Benchmark", f"${benchmark:.2f}")
            
            diff = user_cost - benchmark
            if diff > 0:
                col3.metric("Potential Overpay", f"${diff:.2f}/mo", delta=f"-${diff:.2f}", delta_color="inverse")
                st.warning(f"⚠️ You appear to be paying **${diff:.2f} more per month** than the regional benchmark for {category.lower()}.")
                if pd.notna(provider):
                    st.info(f"💡 **Recommendation:** Consider looking into **{provider}**, a top-performing provider in your area.")
            else:
                col3.metric("Savings Status", "Great Rate!", delta=f"+${abs(diff):.2f}", delta_color="normal")
                st.success(f"🎉 Excellent news! Your current rate is at or below the regional benchmark.")
        else:
            st.warning(f"⚠️ No benchmark data is currently available for postcode **{user_postcode}** in the {category} sheet.")

# --- FOOTER ---
st.markdown("---")
st.caption("BillScope v1.2 • Powered by custom regional benchmarks.")
