import streamlit as st
import pandas as pd

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

st.title("🔍 BillScope")
st.subheader("Living Expense & Savings Auditor")
st.write("Track your ongoing household bills, factor in your postcode, and instantly identify potential savings against regional benchmarks.")

# --- MOCK REGIONAL BENCHMARK DATABASE ---
benchmark_data = {
    "4557": {"Electricity": 350.0, "Internet": 85.0, "Phone": 55.0},
    "2000": {"Electricity": 400.0, "Internet": 90.0, "Phone": 60.0},
    "3000": {"Electricity": 380.0, "Internet": 85.0, "Phone": 55.0}
}

# --- SIDEBAR: USER INPUT FORM ---
st.sidebar.header("Enter Your Bill Details")

user_postcode = st.sidebar.selectbox("Your Postcode", ["4557", "2000", "3000"])
category = st.sidebar.selectbox("Expense Category", ["Electricity", "Internet", "Phone"])
provider_name = st.sidebar.text_input("Current Provider Name", "e.g., Origin or Telstra")
billing_cycle = st.sidebar.selectbox("Billing Cycle", ["Monthly", "Quarterly"])
current_cost = st.sidebar.number_input("Current Cost ($)", min_value=0.0, value=100.0, step=5.0)

# Normalize cost to a monthly figure for comparison
if billing_cycle == "Quarterly":
    monthly_user_cost = current_cost / 3.0
else:
    monthly_user_cost = current_cost

# --- MAIN DASHBOARD COMPARISON LOGIC ---
st.divider()
st.subheader(f"Analysis for Postcode: {user_postcode}")

if user_postcode in benchmark_data and category in benchmark_data[user_postcode]:
    benchmark_monthly = benchmark_data[user_postcode][category]
    
    # Calculate annual figures
    user_annual = monthly_user_cost * 12
    benchmark_annual = benchmark_monthly * 12
    
    # Display Metrics Side-by-Side
    col1, col2 = st.columns(2)
    col1.metric("Your Estimated Annual Cost", f"${user_annual:,.2f}")
    col2.metric(f"Local Benchmark ({category})", f"${benchmark_annual:,.2f}")
    
    # Savings Calculation
    annual_savings = user_annual - benchmark_annual
    
    st.write("")
    if annual_savings > 0:
        st.error(f"⚠️ **Potential Savings Found!** You are paying approximately **${annual_savings:,.2f} more per year** than the average local rate for {category} with {provider_name}.")
    else:
        st.success(f"✅ **Looking Good!** Your current rate with {provider_name} is at or below the regional benchmark.")

else:
    st.info("Select a category and postcode to view local benchmark comparisons.")

