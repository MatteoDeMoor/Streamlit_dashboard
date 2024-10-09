import streamlit as st
from auth import login, register  # Import the functions from auth.py
from dashboard import show_dashboard  # Import the dashboard function from dashboard.py

# Main application logic
if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_dashboard()
    else:
        page = st.sidebar.selectbox("Choose a page", ["Login", "Register"])
        
        if page == "Login":
            login()
        else:
            register()
