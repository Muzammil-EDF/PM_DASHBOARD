# ========================
# 📦 Import Dependencies
# ========================
import streamlit as st                      # For building the web app interface
import pandas as pd                        # For data manipulation
from datetime import datetime              # For working with dates
import gspread                             # To interact with Google Sheets
import json                                # For handling JSON data (Google credentials)
import os                                  # For reading environment variables
from oauth2client.service_account import ServiceAccountCredentials  # For Google Sheets API auth
from io import StringIO                    # Optional, for string-based I/O (not used here directly)

# ===========================
# 🔐 Define User Credentials
# ===========================
# Hardcoded credentials (for demonstration only)
USER1_CREDENTIALS = {
    "user1": "pass1"  # Replace or expand for production use with hashed passwords
}

# ============================================
# 🔑 Get Google Sheets API Client
# ============================================
def get_gspread_client():
    """
    Initialize and return an authenticated gspread client using a service account.
    Supports both environment variable-based secret (for deployment) and local file (for local dev).
    """
    if "GOOGLE_SERVICE_ACCOUNT_JSON" in os.environ:
        # Load from GitHub/Streamlit environment secret
        creds_dict = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    else:
        # Load from local JSON file
        with open("service_account.json") as f:
            creds_dict = json.load(f)

    # Define required OAuth scopes for reading and writing to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    return gspread.authorize(credentials)

# ===================================================
# 📄 Load a Worksheet as DataFrame + gspread object
# ===================================================
def load_sheet_as_df(sheet_title):
    """
    Load the specified Google Sheet into a Pandas DataFrame.
    
    Returns:
        - DataFrame of sheet data
        - gspread worksheet object (for writing later)
    """
    gc = get_gspread_client()
    sh = gc.open(sheet_title)
    worksheet = sh.sheet1  # Use the first sheet
    data = worksheet.get_all_records()  # Read all rows as list of dictionaries
    return pd.DataFrame(data), worksheet

# ================================
# 🔐 User Login Page
# ================================
def login():
    st.title("🔐 User 1 Login")

    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check login credentials
    if st.button("Login"):
        if username in USER1_CREDENTIALS and USER1_CREDENTIALS[username] == password:
            # Successful login: set session variables
            st.session_state.user1_logged_in = True
            st.session_state.user1_username = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# ================================================
# 🧑‍🔧 Main User Maintenance Page (after login)
# ================================================
def user1_page():
    st.title("🧑‍🔧 User 1 Maintenance Page")

    # Session state initialization
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = None
    if "show_operations" not in st.session_state:
        st.session_state.show_operations = False
    if "selected_asset" not in st.session_state:
        st.session_state.selected_asset = None
    if "selected_assets" not in st.session_state:
        st.session_state.selected_assets = []

    # ========================
    # Date Selection Interface
    # ========================
    col1, col2 = st.columns([2, 1])
    with col1:
        st.text_input("Date (auto-filled)", 
                      value=str(st.session_state.selected_date) if st.session_state.selected_date else "", 
                      disabled=True)

    with col2:
        if st.button("📅 Extract Today’s Date"):
            st.session_state.selected_date = datetime.today().date()
            st.session_state.show_operations = False  # Reset operation view when date changes

    # ==============================================
    # Asset Selection (based on selected date)
    # ==============================================
    if st.session_state.selected_date:
        try:
            df_assets, asset_sheet = load_sheet_as_df("Preventive Schedule YTML")  # Sheet name must match in Google Drive
            df_assets['Date'] = pd.to_datetime(df_assets['Date'], errors='coerce').dt.date

            # Filter assets scheduled for the selected date
            filtered_df = df_assets[df_assets['Date'] == st.session_state.selected_date]

            if not filtered_df.empty:
                # Get only the unselected assets for dropdown
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

    # ====================================================
    # Operations Checklist Section (for selected asset)
    # ====================================================
    if st.session_state.show_operations and st.session_state.selected_asset:
        st.markdown("---")
        st.subheader(f"🛠️ Operations for Asset: {st.session_state.selected_asset}")

        try:
            df_ops, _ = load_sheet_as_df("Operations")  # Must contain "Operation" column
            operations = df_ops["Operation"].dropna().tolist()

            # Display checklist for operations
            checked_ops = []
            for op in operations:
                if st.checkbox(op, key=op):  # Ensure unique key
                    checked_ops.append(op)

            # Submission button to update sheet
            if st.button("✅ Submit"):
                try:
                    for idx, row in df_assets.iterrows():
                        if (
                            row['Date'] == st.session_state.selected_date and
                            row['Asset Number'] == st.session_state.selected_asset
                        ):
                            # Write selected operations to sheet
                            asset_sheet.update_cell(idx + 2, df_assets.columns.get_loc("Operations") + 1, ', '.join(checked_ops))
                            asset_sheet.update_cell(idx + 2, df_assets.columns.get_loc("Remarks") + 1, "Done")

                    st.success(f"✅ Operations submitted for {st.session_state.selected_asset}.")
                except Exception as e:
                    st.error(f"Failed to write to sheet: {e}")

        except Exception as e:
            st.error(f"Error reading operations sheet: {e}")

# ===============================
# 🚪 Entry Point: Session Control
# ===============================
if "user1_logged_in" not in st.session_state:
    st.session_state.user1_logged_in = False
    st.session_state.user1_username = ""

# Routing logic based on session
if st.session_state.user1_logged_in:
    if st.button("🚪 Logout"):
        st.session_state.user1_logged_in = False
        st.experimental_rerun()
    else:
        user1_page()
else:
    login()
