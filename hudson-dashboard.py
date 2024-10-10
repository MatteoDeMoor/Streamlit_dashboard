import streamlit as st
from analyst import show_analyst_dashboard  # Import the function from analyst.py
from developer import show_developer_dashboard  # Import the function from developer.py

# Main application logic
if __name__ == "__main__":
    st.markdown("<h1 style='text-align:center;'>Hudson Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Choose Your Role</h2>", unsafe_allow_html=True)

    # Role selection
    role = st.selectbox(
        "Select your role:",
        options=["Select a Role", "Analyst", "Developer"],
        index=0
    )

    if role != "Select a Role":
        st.session_state.selected_role = role  # Store the selected role

        # Display a login button
        if st.button("Login"):
            if role == "Analyst":
                show_analyst_dashboard()
            elif role == "Developer":
                show_developer_dashboard()
    else:
        st.info("Please select a role to proceed.")
