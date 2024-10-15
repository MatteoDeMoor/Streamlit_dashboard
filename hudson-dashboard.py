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
    
# Set the font of the plots to Moneta-Bold
font_path = './assets/fonts/Moneta-Bold.ttf'  # Ensure the font file is correctly placed

try:
    font_manager.fontManager.addfont(font_path)
except FileNotFoundError:
    st.warning("Font file not found. Please check the path.")

# Set the font family for Matplotlib
plt.rcParams['font.family'] = 'Moneta-Bold'  # Use the font name directly

# Manage session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'role_selection'

# Navigation logic
if st.session_state.page == 'role_selection':
    show_dashboard()
    # Add a footer that is fixed at the bottom only for the role selection page
    footer = f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #608099;
        text-align: center;
        padding: 10px;
    }}
    .footer p {{
        color: #bbbdbd;
        margin: 0;
    }}
    </style>
    <div class='footer'>
        <p>© 2024 Hudson Dashboard. All rights reserved.</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
elif st.session_state.page == 'analyst':
    show_analyst_dashboard()
elif st.session_state.page == 'developer':
    show_developer_dashboard()
