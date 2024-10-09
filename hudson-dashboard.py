import streamlit as st
import bcrypt
import json
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
import re  # Voor wachtwoordvalidatie
import logging

# Functie om het gebruikersbestand te laden
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    else:
        return {}

# Functie om de gebruiker te verifiëren
def verify_user(username, password):
    users = load_users()
    if username in users:
        hashed_password = users[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    else:
        return False

# Functie om de sterkte van het wachtwoord te valideren
def is_strong_password(password):
    # Minimaal 8 tekens, 1 hoofdletter, 1 kleine letter, 1 cijfer en 1 speciaal teken
    if len(password) < 8:
        return False, "Wachtwoord moet minimaal 8 tekens lang zijn."
    if not re.search(r"[A-Z]", password):
        return False, "Wachtwoord moet minimaal 1 hoofdletter bevatten."
    if not re.search(r"[a-z]", password):
        return False, "Wachtwoord moet minimaal 1 kleine letter bevatten."
    if not re.search(r"\d", password):
        return False, "Wachtwoord moet minimaal 1 cijfer bevatten."
    if not re.search(r"[!@#\$%\^&\*]", password):
        return False, "Wachtwoord moet minimaal 1 speciaal teken bevatten (!@#$%^&*)."
    return True, "Wachtwoord is sterk."

# Functie om een nieuw account aan te maken
def create_user(username, password):
    users = load_users()
    if username in users:
        return False, "Gebruiker bestaat al"
    
    # Controleer de sterkte van het wachtwoord
    is_valid, message = is_strong_password(password)
    if not is_valid:
        return False, message
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password.decode('utf-8')
    
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Functie om grafieken naar PNG te converteren en te downloaden
def download_plot(fig, filename="plot.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Dashboard functie met grafieken
def show_dashboard():
    st.markdown("<h1 style='text-align:center;'>Dashboard</h1>", unsafe_allow_html=True)

    # Thema en kleurkeuze instellen met 5 basisopties
    st.sidebar.markdown("### Dashboard Thema")
    
    background_color = st.sidebar.radio("Kies een achtergrondkleur", 
                                        options=["rood", "geel", "blauw", "groen", "oranje"])
    
    text_color = st.sidebar.radio("Kies een tekstkleur", 
                                  options=["rood", "geel", "blauw", "groen", "oranje"])
    
    # Mapping voor kleuren
    color_mapping = {
        "rood": "#ff0000",
        "geel": "#ffff00",
        "blauw": "#0000ff",
        "groen": "#00ff00",
        "oranje": "#ffa500"
    }

    # Toepassen van de gekozen kleuren
    st.markdown(f"<style>body {{ background-color: {color_mapping[background_color]}; color: {color_mapping[text_color]}; }}</style>", unsafe_allow_html=True)
    
    # Data voor de grafieken
    x = np.linspace(0, 10, 100)
    bar_x = np.array([1, 2, 3, 4, 5])
    scatter_x = np.random.rand(100)
    scatter_y = np.random.rand(100)

    # Keuzemenu voor grafieken aan de linkerzijde
    graph_options = st.sidebar.radio(
        "Kies een grafiek",
        options=("Lijngrafiek", "Staafdiagram", "Horizontale Staafdiagram", "Scatterplot")
    )

    # 2. Aanpasbare Lijngrafiek voor sin(x) en cos(x)
    if graph_options == "Lijngrafiek":
        st.markdown("<h2 style='text-align:center;'>Lijngrafiek</h2>", unsafe_allow_html=True)

        # Kleur- en lijnstijlopties voor sin(x)
        sin_color_option = st.sidebar.selectbox("Kies een kleur voor sin(x)", ("blauw", "groen", "rood"))
        sin_line_style = st.sidebar.selectbox("Kies een lijnstijl voor sin(x)", ("-", "--", "-.", ":"))

        # Kleur- en lijnstijlopties voor cos(x)
        cos_color_option = st.sidebar.selectbox("Kies een kleur voor cos(x)", ("blauw", "groen", "rood"))
        cos_line_style = st.sidebar.selectbox("Kies een lijnstijl voor cos(x)", ("-", "--", "-.", ":"))
        
        # Koppel de Nederlandse termen aan matplotlib kleuren
        color_mapping = {"blauw": "blue", "groen": "green", "rood": "red"}
        
        fig_line_chart = plt.figure()
        plt.plot(x, np.sin(x), color=color_mapping[sin_color_option], linestyle=sin_line_style, label='sin(x)')
        plt.plot(x, np.cos(x), color=color_mapping[cos_color_option], linestyle=cos_line_style, label='cos(x)')
        plt.legend()
        st.pyplot(fig_line_chart)

        # Sla de figuur op in de session_state
        st.session_state['fig_line_chart'] = fig_line_chart

        # Voeg een download knop toe voor de lijngrafiek
        buf_line_chart = download_plot(fig_line_chart)
        st.download_button("Download Lijngrafiek als PNG", buf_line_chart, "lijngrafiek.png", "image/png")

    # Staafdiagram
    elif graph_options == "Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Staafdiagram</h2>", unsafe_allow_html=True)
        fig_bar_chart = plt.figure()
        plt.bar(bar_x, bar_x * 10)
        plt.xlabel('Categorieën')
        plt.ylabel('Waarden')
        st.pyplot(fig_bar_chart)

        # Sla de figuur op in de session_state
        st.session_state['fig_bar_chart'] = fig_bar_chart

        # Voeg een download knop toe voor de staafdiagram
        buf_bar_chart = download_plot(fig_bar_chart)
        st.download_button("Download Staafdiagram als PNG", buf_bar_chart, "staafdiagram.png", "image/png")

    # Horizontale Staafdiagram
    elif graph_options == "Horizontale Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Horizontale Staafdiagram</h2>", unsafe_allow_html=True)
        fig_horizontal_bar_chart = plt.figure()
        plt.barh(bar_x, bar_x * 10)
        plt.xlabel('Waarden')
        plt.ylabel('Categorieën')
        st.pyplot(fig_horizontal_bar_chart)

        # Sla de figuur op in de session_state
        st.session_state['fig_horizontal_bar_chart'] = fig_horizontal_bar_chart

        # Voeg een download knop toe voor de horizontale staafdiagram
        buf_horizontal_bar_chart = download_plot(fig_horizontal_bar_chart)
        st.download_button("Download Horizontale Staafdiagram als PNG", buf_horizontal_bar_chart, "horizontale_staafdiagram.png", "image/png")

    # Scatterplot
    elif graph_options == "Scatterplot":
        st.markdown("<h2 style='text-align:center;'>Scatterplot</h2>", unsafe_allow_html=True)
        fig_scatter_plot = plt.figure()
        plt.scatter(scatter_x, scatter_y, c='blue', alpha=0.5)
        plt.xlabel('X-as')
        plt.ylabel('Y-as')
        st.pyplot(fig_scatter_plot)

        # Sla de figuur op in de session_state
        st.session_state['fig_scatter_plot'] = fig_scatter_plot

        # Voeg een download knop toe voor de scatterplot
        buf_scatter_plot = download_plot(fig_scatter_plot)
        st.download_button("Download Scatterplot als PNG", buf_scatter_plot, "scatterplot.png", "image/png")

        # Statistieken
        st.write(f"Gemiddelde X: {np.mean(scatter_x):.2f}")
        st.write(f"Gemiddelde Y: {np.mean(scatter_y):.2f}")
        st.write(f"Standaarddeviatie X: {np.std(scatter_x):.2f}")
        st.write(f"Standaarddeviatie Y: {np.std(scatter_y):.2f}")

# Streamlit login scherm
def login():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Gebruikersnaam")
        password = st.text_input("Wachtwoord", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.success(f"Welkom, {username}!")
        else:
            st.error("Ongeldige gebruikersnaam of wachtwoord")

# Gebruikersregistratie
def register():
    st.title("Registreren")
    
    with st.form("register_form"):
        username = st.text_input("Kies een gebruikersnaam")
        password = st.text_input("Kies een wachtwoord", type="password")
        submit_button = st.form_submit_button("Account aanmaken")

    if submit_button:
        success, message = create_user(username, password)
        if success:
            st.success(message)
        else:
            st.error(message)

# Main applicatie logica
if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_dashboard()
    else:
        page = st.sidebar.selectbox("Kies een pagina", ["Login", "Registreren"])
        
        if page == "Login":
            login()
        else:
            register()
