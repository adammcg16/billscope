import streamlit as st

# Page Configuration
st.set_page_config(page_title="NBN Plan Selector", page_icon="🌐", layout="centered")

# Custom CSS styling with updated input background colors and nbn speeds
st.markdown(
    """
    <style>
        :root {
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --input-bg: #f4f6f8;        /* Lighter, eye-friendly color */
            --input-border: #cbd5e1;    /* Gentle gray border */
            --input-focus: #3b82f6;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
        }

        .stApp {
            background-color: var(--bg-color);
            color: var(--text-main);
        }

        .container {
            background-color: var(--card-bg);
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        /* Streamlit input field overrides */
        .stTextInput input, .stSelectbox select {
            background-color: var(--input-bg) !important;
            border: 1px solid var(--input-border) !important;
            border-radius: 8px !important;
            color: var(--text-main) !important;
        }

        .stTextInput input:focus, .stSelectbox select:focus {
            background-color: #ffffff !important;
            border-color: var(--input-focus) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# App UI
st.markdown("## Select Your nbn® Plan")

with st.form("nbn_form"):
  full_name = st.text_input("Full Name", placeholder="Enter your full name")
  email = st.text_input("Email Address", placeholder="Enter your email")

  nbn_speed = st.selectbox(
      "Choose nbn® Speed Tier",
      [
          "Select a speed tier",
          "nbn® 25 (Home Basic II)",
          "nbn® 50 (Home Standard)",
          "nbn® 100 (Home Fast)",
          "nbn® 250 (Home Superfast)",
          "nbn® 1000 (Home Ultrafast)",
      ],
  )

  submitted = st.form_submit_button("Check Availability")

  if submitted:
    if not full_name or not email or nbn_speed == "Select a speed tier":
      st.warning("Please fill out all fields and select a valid speed tier.")
    else:
      st.success(
          f"Thank you, {full_name}! Your request for {nbn_speed} has been"
          " received."
      )
