import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve admin credentials from environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Function to authenticate admin login
def authenticate(username, password):
    """Check if the provided username and password match admin credentials."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def admin_login():
    """Display the admin login form and handle authentication."""
    st.title("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful!")
            st.session_state['admin_authenticated'] = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password. Please try again.")

# Function to restrict access to admin panel
def admin_protect():
    """Require authentication for accessing the admin panel."""
    if 'admin_authenticated' not in st.session_state:
        st.session_state['admin_authenticated'] = False

    if not st.session_state['admin_authenticated']:
        admin_login()
        st.stop() 
