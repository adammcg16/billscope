import streamlit as st
import pandas as pd

# App Config & Branding
st.set_page_config(page_title="BillScope", page_icon="🔍", layout="centered")

# --- LOAD DATA FROM EXCEL ---
@st.cache_data
def load_data():
    file_path = "billscope_tabs.xlsx"
    electricity = pd.read_excel(file_path, sheet_name="Electricity")
    internet = pd.read_excel(file_path, sheet_name="Internet")
    mortgage = pd.read_excel(file_path, sheet_name="Mortgage")
    return electricity, internet, mortgage

try:
    elec_df, net_df, mort_df = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}. Please ensure 'billscope_tabs.xlsx' is uploaded to your GitHub repository.")
    st.stop()

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("🔍 BillScope Menu")
app_page = st.sidebar.radio("Go to", ["Auditor Dashboard", "Terms & Conditions"])

st.sidebar.divider()

# ==========================================
# PAGE 1: AUDITOR DASHBOARD
# ==========================================
if app_page == "Auditor Dashboard":
    st.title("🔍 BillScope")
    st.subheader("Living Expense & Savings Auditor")
    st.write("Track your household bills, factor in your postcode ranges, and identify potential savings.")

    st.sidebar.header("Enter Your Bill Details")
    category = st.sidebar.selectbox("Expense Category", ["Electricity", "Internet", "Mortgage"])

    # --- CATEGORY-SPECIFIC LOGIC ---
    if category in ["Electricity", "Internet"]:
        df = elec_df if category == "Electricity" else net_df
        
        user_postcode = st.sidebar.number_input("Enter Your Postcode", min_value=1000, max_value=9999, value=4557, step=1)
        provider_name = st.sidebar.text_input("Current Provider Name", "e.g., Origin")
        
        if category == "Electricity":
            billing_cycle = st.sidebar.selectbox("Billing Cycle", ["Monthly", "Quarterly"])
        
        current_cost = st.sidebar.number_input("Current Cost ($)", min_value=0.0, value=100.0, step=5.0)
        
        # Auto-detect region range logic
        match = df[(df["postcode_start"] <= user_postcode) & (df["postcode_end"] >= user_postcode)]
        
        if not match.empty:
            region_name = match.iloc[0]["region"]
            benchmark = match.iloc[0]["benchmark_cost"]
            suggested_provider = match.iloc[0]["provider_example"]
            
            monthly_user = current_cost / 3 if (category == "Electricity" and billing_cycle == "Quarterly") else current_cost
            
            st.subheader(f"{category} Analysis for Postcode {user_postcode}")
            st.caption(f"Detected Region: **{region_name}**")
            
            col1, col2 = st.columns(2)
            col1.metric("Your Annual Cost", f"${(monthly_user * 12):,.2f}")
            col2.metric("Regional Benchmark", f"${(benchmark * 12):,.2f}")
            
            savings = (monthly_user * 12) - (benchmark * 12)
            
            st.divider()
            if savings > 0:
                st.error(f"⚠️ **Potential Savings Found!** You are paying approximately **${savings:,.2f} more per year** than the regional benchmark. Consider checking **{suggested_provider}**.")
            else:
                st.success(f"✅ **Looking Good!** Your current rate with {provider_name} is at or below the regional benchmark.")
        else:
            st.warning("⚠️ Postcode not found within current QLD regional ranges. Please check your entered postcode.")

    elif category == "Mortgage":
        df = mort_df
        
        st.sidebar.subheader("Mortgage Details")
        prop_val = st.sidebar.number_input("Property Value ($)", min_value=0.0, value=800000.0, step=10000.0)
        loan_amt = st.sidebar.number_input("Loan Amount ($)", min_value=0.0, value=600000.0, step=10000.0)
        rate_type = st.sidebar.selectbox("Rate Type", ["Variable", "Fixed", "Investment"])
        current_rate = st.sidebar.number_input("Your Current Interest Rate (%)", min_value=0.0, max_value=20.0, value=6.5, step=0.05)
        
        if prop_val > 0:
            lvr = (loan_amt / prop_val) * 100
            lvr_tier = "<80% LVR" if lvr < 80 else ">80% LVR"
            
            if rate_type == "Investment":
                sub_cat = "Investment"
            else:
                sub_cat = f"{rate_type} ({lvr_tier})"
                
            match = df[df["sub_category"] == sub_cat]
            
            st.subheader("Mortgage Interest Rate Analysis")
            
            if not match.empty:
                benchmark_rate = match.iloc[0]["benchmark_value"]
                
                col1, col2 = st.columns(2)
                col1.metric("Your Calculated LVR", f"{lvr:.1f}%", lvr_tier)
                col2.metric("Market Benchmark Rate", f"{benchmark_rate:.2f}%")
                
                st.divider()
                if current_rate > benchmark_rate:
                    rate_diff = current_rate - benchmark_rate
                    st.error(f"⚠️ **Potential Savings Found!** Your interest rate ({current_rate:.2f}%) is **{rate_diff:.2f}% higher** than the market benchmark ({benchmark_rate:.2f}%). Consider shopping around.")
                else:
                    st.success(f"✅ **Competitive Rate!** Your current interest rate of {current_rate:.2f}% is at or below market benchmark levels.")
            else:
                st.warning("Could not match the mortgage criteria with the database spreadsheet.")

# ==========================================
# PAGE 2: TERMS & CONDITIONS
# ==========================================
elif app_page == "Terms & Conditions":
    st.title("⚖️ Terms of Service & Disclaimers")
    st.markdown("Please read these terms carefully before using BillScope.")
    
    st.markdown("""
    ### 1. Agreement to Terms
    By accessing or using BillScope ("the App"), you agree to be bound by these Terms of Service. If you disagree with any part of these terms, you must not use the App.

    ### 2. Nature of Service
    BillScope is a software-as-a-service (SaaS) tool intended to help users track ongoing household expenses, calculate Loan-to-Value Ratios (LVR), and compare user-inputted costs against generalized regional and market benchmarks.

    ### 3. Not Financial or Credit Advice
    The App provides automated calculations and generalized data comparisons only. 
    * The App does **NOT** provide personal financial advice.
    * The App does **NOT** provide credit assistance, financial product recommendations, or brokerage services.
    * Nothing contained within the App should be construed as an inducement, recommendation, or offer to buy or switch any financial product, utility plan, or mortgage.

    ### 4. Accuracy of Benchmarks and Calculations
    While we strive to keep benchmarks accurate, market rates fluctuate frequently. Regional estimates and interest rate benchmarks are generalized and may not apply directly to your individual credit profile, property valuation, or specific utility contract terms. You should read the relevant Product Disclosure Statement (PDS) or speak with a licensed professional before altering or entering into any financial contract.

    ### 5. Subscription and Fees
    Access to BillScope features may require a paid subscription fee. Fees are billed on a recurring basis as selected at checkout. All subscription fees cover the license to use the tracking and calculation software only, and do not constitute payment for advisory services.

    ### 6. Limitation of Liability
    To the maximum extent permitted by Australian Consumer Law (ACL), BillScope, its developers, and operators shall not be held liable for any direct, indirect, incidental, or consequential loss or damage arising out of or in connection with your use of the App, reliance on benchmark calculations, or failure to achieve anticipated financial savings.

    ### 7. Governing Law
    These terms shall be governed by and construed in accordance with the laws of Queensland, Australia, and you submit to the non-exclusive jurisdiction of the courts located in Queensland for the resolution of any disputes.
    """)
