import streamlit as st
import bcrypt
import json
import os
import re

# Function to load the user file
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    else:
        return {}

# Function to validate password strength
def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least 1 uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least 1 lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least 1 digit."
    if not re.search(r"[!@#\$%\^&\*]", password):
        return False, "Password must contain at least 1 special character (!@#$%^&*)."
    return True, "Password is strong."

# Function to create a new account
def create_user(username, password):
    users = load_users()
    if username in users:
        return False, "User already exists"

    is_valid, message = is_strong_password(password)
    if not is_valid:
        return False, message

    # Hash the password and store the user
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password.decode('utf-8')

    # Save the updated user list to the file
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

    return True, "User created successfully."

# User registration
def register():
    st.title("Register")
    
    with st.form("register_form"):
        username = st.text_input("Choose a username")
        password = st.text_input("Choose a password", type="password")
        submit_button = st.form_submit_button("Create Account")

    if submit_button:
        # Check for empty fields
        if not username or not password:
            st.error("Username and password cannot be empty.")
            return
        
        # Call create_user and check the return value
        result = create_user(username, password)
        
        if result is not None:
            success, message = result
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("An unexpected error occurred.")


# Start the application
if __name__ == "__main__":
    register()
