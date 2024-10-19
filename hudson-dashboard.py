import streamlit as st
from role_selection import show_role_selection
from analyst import show_analyst_dashboard
from developer import show_developer_dashboard
from layout import load_custom_css, add_footer, load_custom_font_graphs

# Set the page title and layout
st.set_page_config(page_title="Hudson Dashboard", layout="wide", page_icon="assets/images/logo--light.png")

# Load custom CSS
load_custom_css()

# Load custom fonts for graphs
load_custom_font_graphs()

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'role_selection'

# Navigation logic
if st.session_state.page == 'role_selection':
    show_role_selection()
    add_footer()  # Add footer
elif st.session_state.page == 'analyst':
    show_analyst_dashboard()
elif st.session_state.page == 'developer':
    show_developer_dashboard()
