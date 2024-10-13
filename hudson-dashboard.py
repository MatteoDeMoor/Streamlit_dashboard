import streamlit as st
from dashboard import show_dashboard
from analyst import show_analyst_dashboard
from developer import show_developer_dashboard
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Set the page title and layout
st.set_page_config(page_title="Hudson Dashboard", layout="wide", page_icon="assets/images/logo--light.png")
print(st.get_option("theme.primaryColor"))
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
#Set the font of the plots
font_path = './assets/fonts/Moneta-Bold.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
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
