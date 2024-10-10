import streamlit as st
from analyst import show_analyst_dashboard  # Import the function from analyst.py
from developer import show_developer_dashboard  # Import the function from developer.py

# Main application logic
if __name__ == "__main__":
    # Role selection
    role = st.sidebar.selectbox("Choose your role", ["Analyst", "Developer"])

    if role == "Analyst":
        show_analyst_dashboard()
    elif role == "Developer":
        show_developer_dashboard()
