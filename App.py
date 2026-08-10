import streamlit as st
import pandas as pd

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

st.title("🔍 BillScope")
st.subheader("Living Expense & Savings Auditor")
st.write("Track your ongoing household bills, factor in your postcode, and instantly identify potential savings against regional benchmarks.")

# --- LOAD BENCHMARKS FROM CSV ---
@st.cache_data
def load_benchmarks():
    # Reads the CSV file you created in the repository
    return pd.read_csv("benchmarks.csv")

df_benchmarks = load_benchmarks()

# --- SIDEBAR: USER INPUT FORM ---
st.sidebar.header("Enter Your Bill Details")

# Pull unique postcodes dynamically from the CSV file
available_postcodes = df_benchmarks["postcode"].astype(str).unique().tolist()
user_postcode = st.sidebar.selectbox("Your Postcode", available_postcodes)

# Filter categories available for that specific postcode
filtered_categories = df_benchmarks[df_benchmarks["postcode"].astype(str) == user_postcode]["category"].tolist()
category = st.sidebar.selectbox("Expense Category", filtered_categories)

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

# Lookup benchmark cost from the CSV data frame
match = df_benchmarks[(df_benchmarks["postcode"].astype(str) == user_postcode) & (df_benchmarks["category"] == category)]

if not match.empty:
    benchmark_monthly = float(match["benchmark_cost"].values[0])
    suggested_provider = match["provider_example"].values[0]
    
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
        st.error(f"⚠️ **Potential Savings Found!** You are paying approximately **${annual_savings:,.2f} more per year** than the average local rate. Consider checking providers like **{suggested_provider}**.")
    else:
        st.success(f"✅ **Looking Good!** Your current rate with {provider_name} is at or below the regional benchmark.")

else:
    st.info("No benchmark data found for this selection.")