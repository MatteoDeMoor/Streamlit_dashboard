import streamlit as st
from homepage import show_homepage
from analyst import show_analyst_dashboard
from developer import show_developer_dashboard
from layout import load_custom_css, add_footer, load_custom_font_graphs

# Set the page title and layout
st.set_page_config(page_title="Hudson Dashboard", layout="wide", page_icon="assets/images/logo--light.png")

# Load custom CSS and fonts
load_custom_css()
load_custom_font_graphs()

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'homepage'

# Navigation logic
if st.session_state.page == 'homepage':
    show_homepage() # Show the homepage
    add_footer()  # Add footer
elif st.session_state.page == 'analyst':
    show_analyst_dashboard() # Show the analyst dashboard
elif st.session_state.page == 'developer':
    show_developer_dashboard() # Show the developer dashboard
