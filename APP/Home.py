import streamlit as st
import sqlite3
conn = sqlite3.connect("maintenance.db")
c = conn.cursor()

# Add a new user
username = st.text_input("New Username")
password = st.text_input("New Password", type="password")

if st.button("Add User"):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    st.success("User added!")

conn.close()
st.set_page_config(page_title="Preventive Maintenance App", layout="centered")

st.title("🛠️ Digital Maintenance Management System")
st.markdown("""
Use the sidebar to navigate to:
- 👨‍🔧 Master Machine List
- 📘 Preventive Maintenance

Each user page is login-protected.
""")
