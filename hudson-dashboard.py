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
        
        fig = plt.figure()
        plt.plot(x, np.sin(x), color=color_mapping[sin_color_option], linestyle=sin_line_style, label='sin(x)')
        plt.plot(x, np.cos(x), color=color_mapping[cos_color_option], linestyle=cos_line_style, label='cos(x)')
        plt.legend()
        st.pyplot(fig)

    # Staafdiagram
    elif graph_options == "Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Staafdiagram</h2>", unsafe_allow_html=True)
        fig = plt.figure()
        plt.bar(bar_x, bar_x * 10)
        plt.xlabel('Categorieën')
        plt.ylabel('Waarden')
        st.pyplot(fig)

    # Horizontale Staafdiagram
    elif graph_options == "Horizontale Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Horizontale Staafdiagram</h2>", unsafe_allow_html=True)
        fig = plt.figure()
        plt.barh(bar_x, bar_x * 10)
        plt.xlabel('Waarden')
        plt.ylabel('Categorieën')
        st.pyplot(fig)

    # 5. Scatterplot zonder filter, maar met Statistieken
    elif graph_options == "Scatterplot":
        st.markdown("<h2 style='text-align:center;'>Scatterplot</h2>", unsafe_allow_html=True)
        
        fig = plt.figure()
        plt.scatter(scatter_x, scatter_y, c='blue', alpha=0.5)
        plt.xlabel('X-as')
        plt.ylabel('Y-as')
        st.pyplot(fig)

        # Statistieken
        st.write(f"Gemiddelde X: {np.mean(scatter_x):.2f}")
        st.write(f"Gemiddelde Y: {np.mean(scatter_y):.2f}")
        st.write(f"Standaarddeviatie X: {np.std(scatter_x):.2f}")
        st.write(f"Standaarddeviatie Y: {np.std(scatter_y):.2f}")

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

