import streamlit as st
from analyst import show_analyst_dashboard  # Import the function from analyst.py
from developer import show_developer_dashboard  # Import the function from developer.py

# Set page config

st.set_page_config(
    page_title="Hudson Dashboard",
    page_icon="😃",
    layout="centered",
    initial_sidebar_state="expanded",
    # Theme settings
    theme={
        "primaryColor": "#F39C12",
        "backgroundColor": "#2C3E50",
        "secondaryBackgroundColor": "#34495E",
        "textColor": "#ECF0F1",
        "font": "sans serif",
    }
)

st.markdown("<h1 class='header'>Hudson Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='header'>Choose Your Role</h2>", unsafe_allow_html=True)

# Role selection
role = st.selectbox(
    "Select your role:",
    options=["Select a Role", "Analyst", "Developer"],
    index=0,
    key="role_selection"
)

if role != "Select a Role":
    st.session_state.selected_role = role  # Store the selected role

    # Display a login button with custom styling
    if st.button("Login", key="login_button", help="Click to login as selected role", css_class='button'):
        if role == "Analyst":
            show_analyst_dashboard()
        elif role == "Developer":
            show_developer_dashboard()
else:
    st.info("Please select a role to proceed.")
