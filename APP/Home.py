import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Preventive Maintenance App", layout="centered")
st.title("🛠️ Digital Maintenance Management System")
st.markdown("""
Use the sidebar to navigate to:
- 👨‍🔧 Master Machine List
- 📘 Preventive Maintenance

Each user page is login-protected.
""")

# ========================================
# 🧱 Database Setup
# ========================================

DB_PATH = "maintenance.db"

# Check if DB file exists
if not os.path.exists(DB_PATH):
    st.info("🔧 Creating new database file...")
    
# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ========================================
# 🔨 Create Table
# ========================================
def create_table():
    """Create the registrations table if it doesn't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            STATUS TEXT(50),
            TYPE TEXT(50),
            CATEGORY TEXT(50)
        )
    """)
    conn.commit()

# ========================================
# ➕ Insert Entry
# ========================================
def add_info(status, machine_type, category):
    """Insert user input into the database."""
    cursor.execute("INSERT INTO registrations (STATUS, TYPE, CATEGORY) VALUES (?, ?, ?)",
                   (status, machine_type, category))
    conn.commit()
    st.success("✅ Entry added to the database!")

# ========================================
# 🧾 Show Entries
# ========================================
def view_entries():
    """Fetch and display all entries from the database."""
    st.subheader("📄 View Registered Machines")
    cursor.execute("SELECT * FROM registrations")
    records = cursor.fetchall()
    if records:
        st.dataframe(records, use_container_width=True)
    else:
        st.info("No entries found in the database.")

# ========================================
# 📝 Form UI
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
# 🚀 Run App Functions
# ========================================
create_table()       # Ensure table exists
form_creation()      # Display form
view_entries()       # Show existing data
