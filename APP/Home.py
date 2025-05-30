import streamlit as st
import sqlite3
import os

# ========================================
# 🛠️ Page Setup
# ========================================
st.set_page_config(page_title="Preventive Maintenance App", layout="centered")
st.title("🛠️ Digital Maintenance Management System")
st.markdown("""
Use the sidebar to navigate to:
- 👨‍🔧 Master Machine List
- 📘 Preventive Maintenance

Each user page is login-protected.
""")

# ========================================
# 🔌 Setup SQLite Database
# ========================================
DB_FILENAME = "maintenance.db"

# Get full path to save DB in the same folder as this script
db_path = os.path.join(os.path.dirname(__file__), DB_FILENAME)

# Connect to SQLite database (will auto-create file if it doesn't exist)
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# ========================================
# 🧱 Create Table (if not exists)
# ========================================
def create_table():
    """Create the registration table if it does not already exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            STATUS TEXT(50),
            TYPE TEXT(50),
            CATEGORY TEXT(50)
        )
    """)
    conn.commit()

# ========================================
# ➕ Insert Data into Table
# ========================================
def add_info(status, machine_type, category):
    """Insert user input into the database."""
    cursor.execute("INSERT INTO registrations (STATUS, TYPE, CATEGORY) VALUES (?, ?, ?)",
                   (status, machine_type, category))
    conn.commit()
    st.success("✅ Entry added to the database!")

# ========================================
# 📋 Main Streamlit Form
# ========================================
def form_creation():
    """Display the registration form and handle submission."""
    st.title("🧵 Sewing Machine Registration")

    st.write("Please fill out the fields below to register a machine:")

    with st.form("Sewing Machine Registration Form"):
        status = st.text_input('Enter Machine Status (Active, Maintenance, Dead, Ready)')
        machine_type = st.text_input('Enter Machine Type')
        category = st.text_input('Enter Machine Category')
        submit = st.form_submit_button(label='Register')

    if submit:
        if status and machine_type and category:
            add_info(status, machine_type, category)
        else:
            st.warning("⚠️ Please fill in all fields before submitting.")

# ========================================
# 📄 View Entries
# ========================================
def view_entries():
    st.subheader("📄 View Registered Machines")

    cursor.execute("SELECT * FROM registrations")
    records = cursor.fetchall()

    if records:
        st.dataframe(records, use_container_width=True)
    else:
        st.info("No entries found in the database.")


# ========================================
# 🚀 Main App Execution
# ========================================
create_table()       # Ensure table exists
form_creation()      # Display the form
view_entries()       # Show all entries
