import streamlit as st
import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

def load_custom_font_graphs():
    font_path = './assets/fonts/Moneta-Bold.ttf'

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found at: {font_path}")

    font_prop = fm.FontProperties(fname=font_path)
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

def load_custom_css():
    """Load custom CSS from a file and apply it to the Streamlit app."""
    try:
        with open("style.css") as css:
            st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Please check the path.")

def add_footer():
    """Add a footer with custom styling to the Streamlit app."""
    footer = """
    <div class='footer'>
        <p>© 2024 Hudson Dashboard. All rights reserved.</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
