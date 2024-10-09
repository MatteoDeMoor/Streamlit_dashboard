import streamlit as st
import bcrypt
import json
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
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

# Functie om een nieuw account aan te maken
def create_user(username, password):
    users = load_users()
    if username in users:
        return False  # Gebruiker bestaat al
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password.decode('utf-8')
    
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
    
    return True

# Logging configureren
logging.basicConfig(filename="app_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Functie om grafieken naar PNG te converteren en te downloaden
def download_plot(fig, filename="plot.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Dashboard functie met grafieken
def show_dashboard():
    st.markdown("<h1 style='text-align:center;'>Dashboard</h1>", unsafe_allow_html=True)
    
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
            st.success("Succesvol ingelogd!")
            st.session_state.show_dashboard = True
            logging.info(f"Gebruiker '{username}' succesvol ingelogd.")
        else:
            st.error("Ongeldige inloggegevens.")
            logging.warning(f"Mislukte inlogpoging voor gebruiker '{username}'.")


# Streamlit registratie scherm
def register():
    st.title("Registreer")
    
    with st.form("register_form"):
        new_username = st.text_input("Nieuwe gebruikersnaam")
        new_password = st.text_input("Nieuw wachtwoord", type="password")
        submit_button = st.form_submit_button("Registreer")

    if submit_button:
        if create_user(new_username, new_password):
            st.success("Account succesvol aangemaakt!")
            logging.info(f"Nieuwe gebruiker '{new_username}' geregistreerd.")
        else:
            st.error("Gebruikersnaam bestaat al.")
            logging.warning(f"Registratie mislukt: gebruikersnaam '{new_username}' bestaat al.")


# Hoofdtoepassing
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False

    if st.session_state.logged_in and st.session_state.show_dashboard:
        show_dashboard()
    else:
        st.sidebar.title("Navigatie")
        optie = st.sidebar.radio("Selecteer een optie", ("Login", "Registreer"))

        if optie == "Login":
            login()
        elif optie == "Registreer":
            register()

if __name__ == "__main__":
    main()
