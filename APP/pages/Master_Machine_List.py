import streamlit as st
import pandas as pd

GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/11WppySSOEDKbcAAtqJjvnfU8vxcuQJPh5ZcTv_9e2I4/export?format=csv"

USER2_CREDENTIALS = {
    "user2": "pass2"
}

def login():
    st.title("🔐 Master Machine List Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER2_CREDENTIALS and USER2_CREDENTIALS[username] == password:
            st.session_state.user2_logged_in = True
            st.session_state.user2_username = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def user2_page():
    st.title("📘 Master Machine List")
    try:
        df_master = pd.read_csv(GOOGLE_SHEET_CSV)

        with st.expander("🔍 Filter Machine List", expanded=False):
            search_values = {}
            for col in df_master.columns:
                search_values[col] = st.text_input(f"Search in '{col}'")

        filtered_df = df_master.copy()
        for col, val in search_values.items():
            if val:
                filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(val, case=False, na=False)]

        st.markdown("### 📋 Filtered Machine List")
        st.dataframe(filtered_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading machine list from Google Sheet: {e}")

# Login state management
if "user2_logged_in" not in st.session_state:
    st.session_state.user2_logged_in = False
    st.session_state.user2_username = ""

if st.session_state.user2_logged_in:
    if st.button("🚪 Logout"):
        st.session_state.user2_logged_in = False
        st.experimental_rerun()
    else:
        user2_page()
else:
    login()

