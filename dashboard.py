import streamlit as st
from PIL import Image

def show_dashboard():
    # Create columns for layout
    col1, col2 = st.columns([1, 3])

    # Load and display the logo in the upper left corner
    with col1:
        img = Image.open("images/logo-hudson.png")
        st.image(img, width=100)

    # Center the title in the second column
    with col2:
        st.markdown("<h1 style='text-align: center;'>Hudson Dashboard</h1>", unsafe_allow_html=True)

    # Role selection
    role = st.selectbox("Select your role", ("Analyst", "Developer"))

    # Navigation button
    if st.button("Login"):
        if role == "Analyst":
            st.session_state.page = "analyst"
        elif role == "Developer":
            st.session_state.page = "developer"
