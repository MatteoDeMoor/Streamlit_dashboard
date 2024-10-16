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
    import streamlit as st

    # Custom CSS to style the links and center them

    st.write("##")
    st.markdown("<h3>Contacteer Hudson</h3>", unsafe_allow_html=True)

    # Centered links in a single row
    st.markdown("""
        <div class="centered-links">
            <a href="https://www.hudsonsolutions.com/be-nl/contacteer-ons" class="centered-link">Stel ons uw Vraag</a>
            <a href="https://www.hudsonsolutions.com/be-nl/spontaan-solliciteren" class="centered-link">Solliciteer spontaan</a>
            <a href="https://www.hudsonsolutions.com/be-nl/onze-kantoren" class="centered-link">Vind een Kantoor</a>
            <a href="https://www.hudsonsolutions.com/be-nl/over-hudson/werken-bij-hudson" class="centered-link">Werken bij Hudson</a>
            <a href="https://www.hudsonsolutions.com/media/boddrpko/cookiepolicy_nl_2024.pdf" class="centered-link">Cookiebeleid</a>
            <a href="https://www.hudsonsolutions.com/media/o1oah3en/privacybeleid_hudson_nl.pdf" class="centered-link">Privacyverklaring</a>
        </div>
        """, unsafe_allow_html=True)

    # Footer logic remains in Python, as positioning can't be handled in TOML
    footer = f"""
    <div class='footer'>
        <p>© 2024 Hudson Dashboard. All rights reserved.</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
elif st.session_state.page == 'analyst':
    show_analyst_dashboard()
elif st.session_state.page == 'developer':
    show_developer_dashboard()
