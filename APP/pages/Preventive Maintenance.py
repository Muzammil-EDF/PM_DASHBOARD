import streamlit as st
import pandas as pd
from datetime import datetime

# 🔗 Google Sheet CSV links (replace these with your actual Google Sheet IDs)
ASSET_SHEET_ID = "1wAyHAy1XdqR0DgVUaWMjpWuj2dCX2JiVZK51OZAkhI0"
OPERATIONS_SHEET_ID = "1-x39S7oomlU4BSNZX9Q9g2MOQLCiRM5eox3QEPPs46s"

EXCEL_URL = f"https://docs.google.com/spreadsheets/d/{ASSET_SHEET_ID}/export?format=csv"
OPERATIONS_URL = f"https://docs.google.com/spreadsheets/d/{OPERATIONS_SHEET_ID}/export?format=csv"

USER1_CREDENTIALS = {
    "user1": "pass1"
}

def login():
    st.title("🔐 User 1 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER1_CREDENTIALS and USER1_CREDENTIALS[username] == password:
            st.session_state.user1_logged_in = True
            st.session_state.user1_username = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def user1_page():
    st.title("🧑‍🔧 User 1 Maintenance Page")

    if "selected_date" not in st.session_state:
        st.session_state.selected_date = None
    if "show_operations" not in st.session_state:
        st.session_state.show_operations = False
    if "selected_asset" not in st.session_state:
        st.session_state.selected_asset = None
    if "selected_assets" not in st.session_state:
        st.session_state.selected_assets = []

    col1, col2 = st.columns([2, 1])
    with col1:
        st.text_input("Date (auto-filled)", value=str(st.session_state.selected_date) if st.session_state.selected_date else "", disabled=True)
    with col2:
        if st.button("📅 Extract Today’s Date"):
            st.session_state.selected_date = datetime.today().date()
            st.session_state.show_operations = False

    if st.session_state.selected_date:
        try:
            df_assets = pd.read_csv(EXCEL_URL)
            df_assets['Date'] = pd.to_datetime(df_assets['Date'], errors='coerce').dt.date
            filtered_df = df_assets[df_assets['Date'] == st.session_state.selected_date]

            if not filtered_df.empty:
                asset_options = filtered_df['Asset Number'].dropna().unique()
                available_assets = [a for a in asset_options if a not in st.session_state.selected_assets]

                if available_assets:
                    selected_asset = st.selectbox("Select Asset", available_assets)
                    if st.button("➡️ Proceed"):
                        st.session_state.selected_asset = selected_asset
                        st.session_state.show_operations = True
                        st.session_state.selected_assets.append(selected_asset)
                else:
                    st.info("✅ All available assets for today have been selected.")
            else:
                st.warning("No assets found for the selected date.")
        except Exception as e:
            st.error(f"Error reading asset sheet: {e}")
    else:
        st.info("Please extract today's date to continue.")

    if st.session_state.show_operations and st.session_state.selected_asset:
        st.markdown("---")
        st.subheader(f"🛠️ Operations for Asset: {st.session_state.selected_asset}")
        try:
            df_ops = pd.read_csv(OPERATIONS_URL)
            operations = df_ops["Operation"].dropna().tolist()

            checked_ops = []
            for op in operations:
                if st.checkbox(op, key=op):
                    checked_ops.append(op)

            if st.button("✅ Submit"):
                st.warning("✋ This version uses Google Sheets in read-only mode. To update the sheet, you'll need Google Sheets API integration with credentials.")
                st.write("These operations would be submitted:", checked_ops)

        except Exception as e:
            st.error(f"Error reading operations sheet: {e}")

# Login state management
if "user1_logged_in" not in st.session_state:
    st.session_state.user1_logged_in = False
    st.session_state.user1_username = ""

if st.session_state.user1_logged_in:
    if st.button("🚪 Logout"):
        st.session_state.user1_logged_in = False
        st.experimental_rerun()
    else:
        user1_page()
else:
    login()
