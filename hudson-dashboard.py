import streamlit as st
import bcrypt
import json
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
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

# Function to convert graphs to PNG and download
def download_plot(fig, filename="plot.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Dashboard function with graphs
def show_dashboard():
    st.markdown("<h1 style='text-align:center;'>Dashboard</h1>", unsafe_allow_html=True)

    # Data for the graphs
    x = np.linspace(0, 10, 100)
    bar_x = np.array([1, 2, 3, 4, 5])
    scatter_x = np.random.rand(100)
    scatter_y = np.random.rand(100)

    # Sidebar graph options
    graph_options = st.sidebar.radio(
        "Choose a graph",
        options=("Line Chart", "Bar Chart", "Horizontal Bar Chart", "Scatter Plot")
    )

    # 2. Customizable Line Chart for sin(x) and cos(x)
    if graph_options == "Line Chart":
        st.markdown("<h2 style='text-align:center;'>Line Chart</h2>", unsafe_allow_html=True)

        # Color and line style options for sin(x)
        sin_color_option = st.sidebar.selectbox("Choose a color for sin(x)", ("blue", "green", "red"))
        sin_line_style = st.sidebar.selectbox("Choose a line style for sin(x)", ("-", "--", "-.", ":"))

        # Color and line style options for cos(x)
        cos_color_option = st.sidebar.selectbox("Choose a color for cos(x)", ("blue", "green", "red"))
        cos_line_style = st.sidebar.selectbox("Choose a line style for cos(x)", ("-", "--", "-.", ":"))
        
        # Map English color terms to matplotlib colors
        color_mapping = {"blue": "blue", "green": "green", "red": "red"}
        
        fig_line_chart = plt.figure()
        plt.plot(x, np.sin(x), color=color_mapping[sin_color_option], linestyle=sin_line_style, label='sin(x)')
        plt.plot(x, np.cos(x), color=color_mapping[cos_color_option], linestyle=cos_line_style, label='cos(x)')
        plt.legend()
        st.pyplot(fig_line_chart)

        # Save the figure in session_state
        st.session_state['fig_line_chart'] = fig_line_chart

        # Add a download button for the line chart
        buf_line_chart = download_plot(fig_line_chart)
        st.download_button("Download Line Chart as PNG", buf_line_chart, "line_chart.png", "image/png")

    # Bar Chart
    elif graph_options == "Bar Chart":
        st.markdown("<h2 style='text-align:center;'>Bar Chart</h2>", unsafe_allow_html=True)
        fig_bar_chart = plt.figure()
        plt.bar(bar_x, bar_x * 10)
        plt.xlabel('Categories')
        plt.ylabel('Values')
        st.pyplot(fig_bar_chart)

        # Save the figure in session_state
        st.session_state['fig_bar_chart'] = fig_bar_chart

        # Add a download button for the bar chart
        buf_bar_chart = download_plot(fig_bar_chart)
        st.download_button("Download Bar Chart as PNG", buf_bar_chart, "bar_chart.png", "image/png")

    # Horizontal Bar Chart
    elif graph_options == "Horizontal Bar Chart":
        st.markdown("<h2 style='text-align:center;'>Horizontal Bar Chart</h2>", unsafe_allow_html=True)
        fig_horizontal_bar_chart = plt.figure()
        plt.barh(bar_x, bar_x * 10)
        plt.xlabel('Values')
        plt.ylabel('Categories')
        st.pyplot(fig_horizontal_bar_chart)

        # Save the figure in session_state
        st.session_state['fig_horizontal_bar_chart'] = fig_horizontal_bar_chart

        # Add a download button for the horizontal bar chart
        buf_horizontal_bar_chart = download_plot(fig_horizontal_bar_chart)
        st.download_button("Download Horizontal Bar Chart as PNG", buf_horizontal_bar_chart, "horizontal_bar_chart.png", "image/png")

    # Scatter Plot
    elif graph_options == "Scatter Plot":
        st.markdown("<h2 style='text-align:center;'>Scatter Plot</h2>", unsafe_allow_html=True)
        fig_scatter_plot = plt.figure()
        plt.scatter(scatter_x, scatter_y, c='blue', alpha=0.5)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        st.pyplot(fig_scatter_plot)

        # Save the figure in session_state
        st.session_state['fig_scatter_plot'] = fig_scatter_plot

        # Add a download button for the scatter plot
        buf_scatter_plot = download_plot(fig_scatter_plot)
        st.download_button("Download Scatter Plot as PNG", buf_scatter_plot, "scatter_plot.png", "image/png")

        # Statistics
        st.write(f"Mean X: {np.mean(scatter_x):.2f}")
        st.write(f"Mean Y: {np.mean(scatter_y):.2f}")
        st.write(f"Standard Deviation X: {np.std(scatter_x):.2f}")
        st.write(f"Standard Deviation Y: {np.std(scatter_y):.2f}")

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

# Main application logic
if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_dashboard()
    else:
        page = st.sidebar.selectbox("Choose a page", ["Login", "Register"])
        
        if page == "Login":
            login()
        else:
            register()
