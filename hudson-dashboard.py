import streamlit as st
import bcrypt
import json
import os
from matplotlib import pyplot as plt
import numpy as np

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

# Dashboard functie met grafieken
def show_dashboard():
    st.markdown("<h1 style='text-align:center;'>Dashboard</h1>", unsafe_allow_html=True)
    
    # Keuzemenu voor grafieken aan de linkerzijde
    graph_options = st.sidebar.radio(
        "Kies een grafiek",
        options=("Ingevoerde Gegevens Lijngrafiek", "Staafdiagram", "Horizontale Staafdiagram", "Scatterplot")
    )

    # 1. Gegevensinvoer voor een Lijngrafiek
    if graph_options == "Ingevoerde Gegevens Lijngrafiek":
        st.markdown("<h2 style='text-align:center;'>Ingevoerde Gegevens Lijngrafiek</h2>", unsafe_allow_html=True)

        # Invoervelden voor X- en Y-waarden
        x_values = st.text_input("Voer X-waarden in (gescheiden door komma's)", "1, 2, 3, 4, 5")
        y_values = st.text_input("Voer Y-waarden in (gescheiden door komma's)", "10, 20, 30, 40, 50")

        if st.button("Genereer Grafiek"):
            try:
                x = [float(i) for i in x_values.split(",")]
                y = [float(i) for i in y_values.split(",")]
                
                if len(x) != len(y):
                    st.error("X- en Y-waarden moeten dezelfde lengte hebben!")
                else:
                    fig = plt.figure()
                    plt.plot(x, y, marker='o', linestyle='-', color='blue', label='Ingevoerde Gegevens')
                    plt.xlabel('X-waarden')
                    plt.ylabel('Y-waarden')
                    plt.title('Lijngrafiek van Ingevoerde Gegevens')
                    plt.legend()
                    st.pyplot(fig)

            except ValueError:
                st.error("Voer geldige numerieke waarden in.")

    # Staafdiagram
    elif graph_options == "Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Staafdiagram</h2>", unsafe_allow_html=True)
        fig = plt.figure()
        plt.bar([1, 2, 3], [10, 20, 15])
        plt.xlabel('Categorieën')
        plt.ylabel('Waarden')
        st.pyplot(fig)

    # Horizontale Staafdiagram
    elif graph_options == "Horizontale Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Horizontale Staafdiagram</h2>", unsafe_allow_html=True)
        fig = plt.figure()
        plt.barh([1, 2, 3], [10, 20, 15])
        plt.xlabel('Waarden')
        plt.ylabel('Categorieën')
        st.pyplot(fig)

    # Scatterplot
    elif graph_options == "Scatterplot":
        st.markdown("<h2 style='text-align:center;'>Scatterplot</h2>", unsafe_allow_html=True)
        
        scatter_x = np.random.rand(100)
        scatter_y = np.random.rand(100)
        
        fig = plt.figure()
        plt.scatter(scatter_x, scatter_y, c='blue', alpha=0.5)
        plt.xlabel('X-as')
        plt.ylabel('Y-as')
        st.pyplot(fig)

# Streamlit login scherm
def login():
    st.title("Login")
    
    # Invoervelden voor gebruikersnaam en wachtwoord
    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password")
    
    # Als de gebruiker op de 'Login' knop klikt
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.logged_in = True  # Zet de status in de sessie naar ingelogd
            st.success("Succesvol ingelogd!")
            st.session_state.show_dashboard = True  # Toon het dashboard na inloggen
        else:
            st.error("Ongeldige inloggegevens. Probeer opnieuw.")

# Streamlit registratie scherm
def register():
    st.title("Registreer")
    
    # Invoervelden voor nieuwe gebruikersnaam en wachtwoord
    new_username = st.text_input("Nieuwe gebruikersnaam")
    new_password = st.text_input("Nieuw wachtwoord", type="password")
    
    # Als de gebruiker op de 'Registreer' knop klikt
    if st.button("Registreer"):
        if create_user(new_username, new_password):
            st.success("Account succesvol aangemaakt!")
        else:
            st.error("Gebruikersnaam bestaat al, kies een andere.")

# Hoofdtoepassing
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # Initialiseer de ingelogde status
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False  # Initialiseer de dashboard status

    if st.session_state.logged_in and st.session_state.show_dashboard:
        show_dashboard()  # Toon het dashboard na succesvolle login
    else:
        st.sidebar.title("Navigatie")
        optie = st.sidebar.radio("Selecteer optie", ("Login", "Registreer"))
        
        if optie == "Login":
            login()
        elif optie == "Registreer":
            register()

if __name__ == "__main__":
    main()
