import streamlit as st
import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

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

# Definieer de add_navbar functie
def add_navbar():
    # Maak een horizontale navigatiebalk met alleen de dashboardknoppen
    st.markdown("""<style>
                            @font-face {
                                font-family: "Moneta";
                                src: url("https://corsproxy.io/?https://www.hudsonsolutions.com/assets/corporate/fonts/moneta-black.ttf")
                                    format("truetype");
                            }
                            .stMainBlockContainer {
                                padding-top: 0;
                                margin-top: 0;
                            }
                            .stVerticalBlock {
                                display: flex;
                                flex: 1 1 0%;
                                flex-direction: column;
                                gap: 0;
                            }
                            .stElementContainer:nth-of-type(2) {
                                margin-top: 0rem;
                            }
                            .stElementContainer:nth-of-type(3) {
                                margin-top: 0rem;
                            }
                            .stElementContainer {
                                margin-top: 1rem;
                            }
                            .stElementContainer:nth-of-type(1) {
                                margin-top: 0rem;
                            }
                            .container-xxl {
                                font-family: "Moneta", sans-serif !important;
                            }
                    </style>""", unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Analyst Dashboard", "Developer Dashboard"],
        icons=["bar-chart", "bar-chart"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#111f2a"},
            "icon": {"color": "white"},
            "nav-link": {"font-size": "16px", "color": "white", "font-family": "Moneta"},
            "nav-link-selected": {"background-color": "transparent", "color": "white", "font-family": "Moneta"},
        }
    )

    # Update de sessietoestand op basis van de geselecteerde optie
    if selected == "Analyst Dashboard" and st.session_state.page != 'analyst':
        st.session_state.page = 'analyst'
        st.rerun()

    elif selected == "Developer Dashboard" and st.session_state.page != 'developer':
        st.session_state.page = 'developer'
        st.rerun()
