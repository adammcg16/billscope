import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="BillScope App",
    page_icon="⚡",
    layout="centered"
)

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
st.markdown("Check your household electricity or internet bills against regional benchmarks to uncover potential savings.")

# --- USER INPUT FORM ---
st.sidebar.header("Audit Parameters")
category = st.sidebar.selectbox("Select Utility Category", ["Electricity", "Internet"])
user_postcode = st.sidebar.number_input("Enter Postcode", min_value=1000, max_value=9999, value=4000)

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
                # Map selected tier string to match column names (e.g. 'NBN 50' -> 'nbn_50_cost')
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
