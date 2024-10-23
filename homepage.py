import streamlit as st
from PIL import Image

# Function to show the first screen
def show_homepage():
    # Create columns for layout to center content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        # Load and display the logo
        try:
            img = Image.open("assets/images/logo-hudson-white.png")
            st.image(img, width=200)
        except FileNotFoundError:
            st.error("De logo-afbeelding kan niet worden gevonden. Controleer het pad en probeer het opnieuw.")
        except Exception as e:
            st.error(f"Er is een fout opgetreden bij het laden van de afbeelding: {e}")

    with col2:
        st.markdown("<h1 style='text-align: center;'>Hudson Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True) 
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Go to dashboard</h3>", unsafe_allow_html=True)
        
        select_col1, select_col2, select_col3 = st.columns([1, 2, 1])

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Add the login button
        with select_col2:
            if st.button("Login", use_container_width=True):
                st.session_state.page = "analyst"
                st.rerun()

    # Add white space
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h3>Contacteer Hudson</h3>", unsafe_allow_html=True)
    st.write("##")
    st.write("##")
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
