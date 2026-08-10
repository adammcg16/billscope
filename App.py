import streamlit as st
import pandas as pd

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

st.title("🔍 BillScope")
st.subheader("Living Expense & Savings Auditor")
st.write("Track your household bills, factor in your postcode, and identify potential savings.")

# --- LOAD DATA FROM EXCEL ---
@st.cache_data
def load_data():
    # Ensure billscope_tabs.xlsx is in your GitHub repo
    file_path = "billscope_tabs.xlsx"
    electricity = pd.read_excel(file_path, sheet_name="Electricity")
    internet = pd.read_excel(file_path, sheet_name="Internet")
    mortgage = pd.read_excel(file_path, sheet_name="Mortgage")
    return electricity, internet, mortgage

try:
    elec_df, net_df, mort_df = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}. Please ensure 'billscope_tabs.xlsx' is uploaded.")
    st.stop()

# --- SIDEBAR: USER INPUT FORM ---
st.sidebar.header("Enter Your Bill Details")
category = st.sidebar.selectbox("Expense Category", ["Electricity", "Internet", "Mortgage"])

# --- CATEGORY-SPECIFIC LOGIC ---
if category == "Electricity":
    df = elec_df
    postcode = st.sidebar.selectbox("Your Postcode", df["postcode"].astype(str).unique())
    provider_name = st.sidebar.text_input("Current Provider Name", "e.g., Origin")
    billing_cycle = st.sidebar.selectbox("Billing Cycle", ["Monthly", "Quarterly"])
    current_cost = st.sidebar.number_input("Current Cost ($)", min_value=0.0, value=100.0)
    
    match = df[(df["postcode"].astype(str) == postcode)]
    
    if not match.empty:
        benchmark = match.iloc[0]["benchmark_cost"]
        monthly_user = current_cost / 3 if billing_cycle == "Quarterly" else current_cost
        
        st.subheader(f"Electricity Analysis (Postcode {postcode})")
        col1, col2 = st.columns(2)
        col1.metric("Your Annual Cost", f"${(monthly_user * 12):,.2f}")
        col2.metric("Local Benchmark", f"${(benchmark * 12):,.2f}")
        
        savings = (monthly_user * 12) - (benchmark * 12)
        if savings > 0:
            st.error(f"⚠️ Potential savings of ${savings:,.2f} per year.")
        else:
            st.success("✅ Your rate is competitive.")

elif category == "Internet":
    df = net_df
    postcode = st.sidebar.selectbox("Your Postcode", df["postcode"].astype(str).unique())
    provider_name = st.sidebar.text_input("Current Provider Name", "e.g., Aussie Broadband")
    current_cost = st.sidebar.number_input("Monthly Cost ($)", min_value=0.0, value=80.0)
    
    match = df[(df["postcode"].astype(str) == postcode)]
    
    if not match.empty:
        benchmark = match.iloc[0]["benchmark_cost"]
        st.subheader(f"Internet Analysis (Postcode {postcode})")
        col1, col2 = st.columns(2)
        col1.metric("Your Annual Cost", f"${(current_cost * 12):,.2f}")
        col2.metric("Local Benchmark", f"${(benchmark * 12):,.2f}")
        
        savings = (current_cost * 12) - (benchmark * 12)
        if savings > 0:
            st.error(f"⚠️ Potential savings of ${savings:,.2f} per year.")
        else:
            st.success("✅ Your rate is competitive.")

elif category == "Mortgage":
    df = mort_df
    prop_val = st.sidebar.number_input("Property Value ($)", min_value=0.0, value=800000.0)
    loan_amt = st.sidebar.number_input("Loan Amount ($)", min_value=0.0, value=600000.0)
    rate_type = st.sidebar.selectbox("Rate Type", ["Variable", "Fixed", "Investment"])
    current_rate = st.sidebar.number_input("Your Current Interest Rate (%)", min_value=0.0, value=6.5)
    
    if prop_val > 0:
        lvr = (loan_amt / prop_val) * 100
        lvr_tier = "<80% LVR" if lvr < 80 else ">80% LVR"
        
        if rate_type == "Investment":
            sub_cat = "Investment"
        else:
            sub_cat = f"{rate_type} ({lvr_tier})"
            
        match = df[df["sub_category"] == sub_cat]
        
        if not match.empty:
            benchmark_rate = match.iloc[0]["benchmark_value"]
            st.subheader("Mortgage Analysis")
            st.write(f"Your LVR: {lvr:.1f}% ({lvr_tier})")
            
            if current_rate > benchmark_rate:
                st.error(f"⚠️ Your rate ({current_rate}%) is higher than the benchmark ({benchmark_rate}%).")
            else:
                st.success(f"✅ Your rate ({current_rate}%) is competitive (Benchmark: {benchmark_rate}%).")