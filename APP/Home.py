import streamlit as st
import streamlit as st
import sqlite3

# ========================================
# 🔌 Connect to SQLite Database
# ========================================
# `check_same_thread=False` allows using the connection across multiple Streamlit reruns
conn = sqlite3.connect("maintenance.db", check_same_thread=False)
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

    # Use Streamlit form for grouped input + submission
    with st.form("Sewing Machine Registration Form"):
        status = st.text_input('Enter Machine Status (Active, Maintenance, Dead, Ready)')
        machine_type = st.text_input('Enter Machine Type')
        category = st.text_input('Enter Machine Category')
        submit = st.form_submit_button(label='Register')

    # Form submission logic
    if submit:
        if status and machine_type and category:
            add_info(status, machine_type, category)
        else:
            st.warning("⚠️ Please fill in all fields before submitting.")


create_table()       # Ensure table exists
form_creation()      # Display form


st.set_page_config(page_title="Preventive Maintenance App", layout="centered")
st.title("🛠️ Digital Maintenance Management System")
st.markdown("""
Use the sidebar to navigate to:
- 👨‍🔧 Master Machine List
- 📘 Preventive Maintenance

Each user page is login-protected.
""")
