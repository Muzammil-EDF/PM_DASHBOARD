import streamlit as st
import sqlite3
# Display all users after adding
conn = sqlite3.connect("maintenance.db")
c = conn.cursor()
c.execute("SELECT * FROM users")
rows = c.fetchall()
conn.close()

st.write("👤 Current Users in Database:")
for row in rows:
    st.write(f"ID: {row[0]}, Username: {row[1]}")

st.set_page_config(page_title="Preventive Maintenance App", layout="centered")

st.title("🛠️ Digital Maintenance Management System")
st.markdown("""
Use the sidebar to navigate to:
- 👨‍🔧 Master Machine List
- 📘 Preventive Maintenance

Each user page is login-protected.
""")
