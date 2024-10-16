import streamlit as st

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
