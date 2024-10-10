import streamlit as st
from analyst import show_analyst_dashboard  # Import the function from analyst.py
from developer import show_developer_dashboard  # Import the function from developer.py

# Set page config
st.set_page_config(page_title="Hudson Dashboard", layout="centered")

# Define colors
background_color = "#FFFFFF"  # White background
header_color = "#5E8199"  # Darker shade for the header
role_box_color = "#99B8BF"  # Light shade for the role selection box
button_color = "#58788C"  # Accent color for buttons
text_color = "#121F2C"  # Dark text color for contrast

# Function to display the role selection screen
def display_role_selection():
    st.markdown(
        f"""
        <style>
        .main {{
            background-color: {background_color};
            color: {text_color};
            text-align: center;
        }}
        .header {{
            background-color: {header_color};
            padding: 20px;
            border-radius: 10px;
        }}
        .role-selection {{
            background-color: {role_box_color};
            padding: 20px;
            border-radius: 10px;
            margin: 20px;
        }}
        .button {{
            background-color: {button_color};
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .button:hover {{
            background-color: #4A6C7D;  /* Slightly darker on hover */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 class='header'>Hudson Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='header'>Choose Your Role</h2>", unsafe_allow_html=True)

    # Role selection
    role = st.selectbox(
        "Select your role:",
        options=["Select a Role", "Analyst", "Developer"],
        index=0,
        key="role_selection"
    )

    if role != "Select a Role":
        st.session_state.selected_role = role  # Store the selected role

        # Display a login button with custom styling
        if st.button("Proceed", key="login_button", help="Click to proceed as selected role"):
            st.session_state.page = 'dashboard'  # Navigate to the dashboard page

# Check if the session state exists, if not initialize it
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

if 'page' not in st.session_state:
    st.session_state.page = 'role_selection'  # Default to role selection

# Main application logic
if st.session_state.page == 'role_selection':
    display_role_selection()
else:
    # Show the appropriate dashboard based on the selected role
    if st.session_state.selected_role == "Analyst":
        show_analyst_dashboard()
    elif st.session_state.selected_role == "Developer":
        show_developer_dashboard()
