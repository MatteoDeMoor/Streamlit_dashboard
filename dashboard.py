import streamlit as st
from PIL import Image
    
# Function to show the first screen (role selection)
def show_dashboard():
    # Create columns for layout to center content
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust these ratios to control the layout

    # Load and display the logo in the upper left corner (still in col1 for symmetry)
    with col1:
        img = Image.open("assets/images/logo-hudson.png")
        st.image(img, width=200)

    # Center the title in the middle column
    with col2:
        st.markdown("<h1 style='text-align: center;'>Hudson Dashboard</h1>", unsafe_allow_html=True)

        # Add some space above the selectbox
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Smaller selectbox and center it
        st.markdown("<h3 style='text-align: center;'>Select Your Role</h3>", unsafe_allow_html=True)
        
        # Center and control the width of the selectbox using columns
        select_col1, select_col2, select_col3 = st.columns([1, 2, 1])  # Centering the selectbox

        with select_col2:
            role = st.selectbox("", ("Analyst", "Developer"), key="role_selection", label_visibility="collapsed")  # Remove label and center

        # Add space before the login button
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Add the login button also in the middle
        with select_col2:
            if st.button("Login", use_container_width=True):
                if role == "Analyst":
                    st.session_state.page = "analyst"
                    st.rerun()

                elif role == "Developer":
                    st.session_state.page = "developer"
                    st.rerun()

    # Right column remains empty to keep symmetry
    with col3:
        st.empty()

# Ensure this function runs only when needed
if __name__ == "__main__":
    show_dashboard()
