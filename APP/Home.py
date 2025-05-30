import streamlit as st
import sqlite3

# Connect to the SQLite DB
conn = sqlite3.connect("maintenance.db")
c = conn.cursor()

# Example query
c.execute("SELECT * FROM users")
rows = c.fetchall()

# Display data
st.write("Users in DB:", rows)

conn.close()


st.set_page_config(page_title="Preventive Maintenance App", layout="centered")

st.title("🛠️ Digital Maintenance Management System")
st.markdown("""
Use the sidebar to navigate to:
- 👨‍🔧 Master Machine List
- 📘 Preventive Maintenance

Each user page is login-protected.
""")
