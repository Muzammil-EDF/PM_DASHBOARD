import streamlit as st
import pandas as pd
from datetime import datetime

EXCEL_PATH = "APP/pm_backend.xlsx"
OPERATIONS_PATH = "APP/operations.xlsx"

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
            df_assets = pd.read_excel(EXCEL_PATH)
            df_assets['Date'] = pd.to_datetime(df_assets['Date']).dt.date
            filtered_df = df_assets[df_assets['Date'] == st.session_state.selected_date]

            # if not filtered_df.empty:
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
            # else:
            #     st.warning("No assets found for the selected date.")
        except Exception as e:
            st.error(f"Error reading asset file: {e}")
    else:
        st.info("Please extract today's date to continue.")

    if st.session_state.show_operations and st.session_state.selected_asset:
        st.markdown("---")
        st.subheader(f"🛠️ Operations for Asset: {st.session_state.selected_asset}")
        try:
            df_ops = pd.read_excel(OPERATIONS_PATH)
            operations = df_ops["Operation"].dropna().tolist()

            checked_ops = []
            for op in operations:
                if st.checkbox(op, key=op):
                    checked_ops.append(op)

            if st.button("✅ Submit"):
                if checked_ops:
                    try:
                        df_assets = pd.read_excel(EXCEL_PATH)
                        df_assets['Date'] = pd.to_datetime(df_assets['Date']).dt.date

                        mask = (
                            (df_assets['Date'] == st.session_state.selected_date) &
                            (df_assets['Asset Number'] == st.session_state.selected_asset)
                        )

                        df_assets.loc[mask, 'Operations'] = ', '.join(checked_ops)
                        df_assets.loc[mask, 'Remarks'] = "Done"

                        df_assets.to_excel(EXCEL_PATH, index=False)
                        st.success(f"✅ Operations submitted for {st.session_state.selected_asset}.")
                        st.write("Checked operations:", checked_ops)
                        st.session_state.show_operations = False

                    except Exception as e:
                        st.error(f"Error updating backend file: {e}")
                else:
                    st.warning("Please select at least one operation before submitting.")
        except Exception as e:
            st.error(f"Error reading operations file: {e}")

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

