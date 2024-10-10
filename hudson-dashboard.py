import streamlit as st

# Set the page title and layout
st.set_page_config(page_title="Hudson Dashboard", layout="centered")

# Title
st.title("Hudson Dashboard")

# Role selection
role = st.selectbox("Select your role", ("Analyst", "Developer"))

# Navigation button
if st.button("Login"):
    if role == "Analyst":
        st.session_state.page = "analyst"
    elif role == "Developer":
        st.session_state.page = "developer"

# Show the selected page
if 'page' in st.session_state:
    if st.session_state.page == "analyst":
        from analyst import show_analyst_dashboard
        show_analyst_dashboard()
    elif st.session_state.page == "developer":
        from developer import show_developer_dashboard  # Assuming you have this file
        show_developer_dashboard()
