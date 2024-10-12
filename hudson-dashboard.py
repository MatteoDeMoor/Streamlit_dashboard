import streamlit as st
from dashboard import show_dashboard
from analyst import show_analyst_dashboard
from developer import show_developer_dashboard

# Set the page title and layout (this must be the first Streamlit command)
st.set_page_config(page_title="Hudson Dashboard", layout="wide", page_icon="assets/images/logo--light.png")

# Print the current theme's primary color (optional)
print(st.get_option("theme.primaryColor"))

# Apply custom CSS from style.css
with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Manage session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'role_selection'

# Navigation logic
if st.session_state.page == 'role_selection':
    show_dashboard()
elif st.session_state.page == 'analyst':
    show_analyst_dashboard()
elif st.session_state.page == 'developer':
    show_developer_dashboard()
