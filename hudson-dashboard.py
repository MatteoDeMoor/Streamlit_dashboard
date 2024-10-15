import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
from dashboard import show_dashboard
from analyst import show_analyst_dashboard
from developer import show_developer_dashboard

# Set the page title and layout
st.set_page_config(page_title="Hudson Dashboard", layout="wide", page_icon="assets/images/logo--light.png")

try:
    with open("style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("CSS file not found. Please check the path.")
    
#Set the font of the plots
try:
    font_path = './assets/fonts/Moneta-Bold.ttf'
    font_manager.fontManager.addfont(font_path)
except FileNotFoundError:
    st.warning("Font file not found. Please check the path.")

prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

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

# Add a footer
st.markdown("---")  # Adds a horizontal line
footer = """
<div style='text-align: center; padding: 10px;'>
    <p>© 2024 Hudson Dashboard. All rights reserved.</p>
    <p>Contact: info@hudsondashboard.com | Privacy Policy | Terms of Service</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)