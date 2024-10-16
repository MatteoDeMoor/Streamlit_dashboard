import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
from role_selection import show_role_selection
from analyst import show_analyst_dashboard
from developer import show_developer_dashboard

# Set the page title and layout
st.set_page_config(page_title="Hudson Dashboard", layout="wide", page_icon="assets/images/logo--light.png")

# Set the CSS
try:
    with open("style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("CSS file not found. Please check the path.")
    
# Set the font
font_path = './assets/fonts/Moneta-Bold.ttf'
try:
    font_manager.fontManager.addfont(font_path)
except FileNotFoundError:
    st.warning("Font file not found. Please check the path.")

# Set the font family for Matplotlib
plt.rcParams['font.family'] = 'Moneta-Bold'

# Manage session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'role_selection'

# Navigation logic
if st.session_state.page == 'role_selection':
    show_role_selection()
elif st.session_state.page == 'analyst':
    show_analyst_dashboard()
elif st.session_state.page == 'developer':
    show_developer_dashboard()
