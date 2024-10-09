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

# Function to verify the user
def verify_user(username, password):
    users = load_users()
    if username in users:
        hashed_password = users[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    else:
        return False

# Function to validate password strength
def is_strong_password(password):
    # Minimum 8 characters, 1 uppercase, 1 lowercase, 1 digit, and 1 special character
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
    
    # Validate password strength
    is_valid, message = is_strong_password(password)
    if not is_valid:
        return False, message
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password.decode('utf-8')
    
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Streamlit login screen
def login():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password")

# User registration
def register():
    st.title("Register")
    
    with st.form("register_form"):
        username = st.text_input("Choose a username")
        password = st.text_input("Choose a password", type="password")
        submit_button = st.form_submit_button("Create Account")

    if submit_button:
        success, message = create_user(username, password)
        if success:
            st.success(message)
        else:
            st.error(message)
