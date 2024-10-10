import streamlit as st
from PIL import Image
from developer import show_developer_dashboard
from analyst import show_analyst_dashboard

# Set the page title and layout
st.set_page_config(page_title="Hudson Dashboard", layout="wide", page_icon="images/logo--light.png")

# Create columns for layout
col1, col2 = st.columns([1, 3])  # Adjust ratios if necessary

# Load and display the logo in the upper left corner
with col1:
    img = Image.open("images/logo-hudson.png")
    st.image(img, width=100)  # Set a fixed width for the logo (adjust as necessary)

# Center the title in the second column
with col2:
    st.markdown(
        "<h1 style='text-align: center;'>Hudson Dashboard</h1>",
        unsafe_allow_html=True
    )

# Role selection
role = st.selectbox("Select your role", ("Analyst", "Developer"))

# Navigation button
if st.button("Login"):
    if role == "Analyst":
        st.session_state.page = "analyst"
    elif role == "Developer":
        st.session_state.page = "developer"

# Show the selected page
if 'page' in st.session_state:
    if st.session_state.page == "analyst":
        show_analyst_dashboard()
    elif st.session_state.page == "developer":
        show_developer_dashboard()
