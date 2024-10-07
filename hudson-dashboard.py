import streamlit as st
import bcrypt
import json
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
import logging
from fpdf import FPDF

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

# Functie om een PDF te genereren
def generate_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Lijngrafiek
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Lijngrafiek: sin(x) en cos(x)", ln=True)
    pdf.image("line_chart.png", x=10, y=20, w=180)

    # Staafdiagram
    pdf.add_page()
    pdf.cell(200, 10, txt="Staafdiagram", ln=True)
    pdf.image("bar_chart.png", x=10, y=20, w=180)

    # Horizontale staafdiagram
    pdf.add_page()
    pdf.cell(200, 10, txt="Horizontale Staafdiagram", ln=True)
    pdf.image("horizontal_bar_chart.png", x=10, y=20, w=180)

    # Scatterplot
    pdf.add_page()
    pdf.cell(200, 10, txt="Scatterplot", ln=True)
    pdf.image("scatter_plot.png", x=10, y=20, w=180)

    # PDF terugsturen als buffer
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Dashboard functie met grafieken en downloadknoppen
def show_dashboard():
    st.markdown("<h1 style='text-align:center;'>Dashboard</h1>", unsafe_allow_html=True)

    # Data voor de grafieken
    x = np.linspace(0, 10, 100)
    bar_x = np.array([1, 2, 3, 4, 5])
    scatter_x = np.random.rand(100)
    scatter_y = np.random.rand(100)

    graph_options = st.sidebar.radio(
        "Kies een grafiek",
        options=("Lijngrafiek", "Staafdiagram", "Horizontale Staafdiagram", "Scatterplot")
    )

    if graph_options == "Lijngrafiek":
        st.markdown("<h2 style='text-align:center;'>Lijngrafiek</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.plot(x, np.sin(x), label="sin(x)")
        ax.plot(x, np.cos(x), label="cos(x)")
        ax.legend()
        st.pyplot(fig)
        buf = download_plot(fig)
        st.download_button("Download Lijngrafiek als PNG", buf, file_name="line_chart.png", mime="image/png")
        logging.info("Lijngrafiek bekeken en gedownload.")

    elif graph_options == "Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Staafdiagram</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.bar(bar_x, bar_x * 10)
        st.pyplot(fig)
        buf = download_plot(fig)
        st.download_button("Download Staafdiagram als PNG", buf, file_name="bar_chart.png", mime="image/png")
        logging.info("Staafdiagram bekeken en gedownload.")

    elif graph_options == "Horizontale Staafdiagram":
        st.markdown("<h2 style='text-align:center;'>Horizontale Staafdiagram</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.barh(bar_x, bar_x * 10)
        st.pyplot(fig)
        buf = download_plot(fig)
        st.download_button("Download Horizontale Staafdiagram als PNG", buf, file_name="horizontal_bar_chart.png", mime="image/png")
        logging.info("Horizontale Staafdiagram bekeken en gedownload.")

    elif graph_options == "Scatterplot":
        st.markdown("<h2 style='text-align:center;'>Scatterplot</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.scatter(scatter_x, scatter_y)
        st.pyplot(fig)
        buf = download_plot(fig)
        st.download_button("Download Scatterplot als PNG", buf, file_name="scatter_plot.png", mime="image/png")
        logging.info("Scatterplot bekeken en gedownload.")

# Streamlit login scherm
def login():
    st.title("Login")

    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password")

    if st.button("Login"):
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

    new_username = st.text_input("Nieuwe gebruikersnaam")
    new_password = st.text_input("Nieuw wachtwoord", type="password")

    if st.button("Registreer"):
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
        if st.sidebar.button("Download alle grafieken als PDF"):
            pdf_buf = generate_pdf()
            st.download_button("Download PDF", pdf_buf, file_name="alle_grafieken.pdf", mime="application/pdf")
            logging.info("PDF met alle grafieken gedownload.")
    else:
        st.sidebar.title("Navigatie")
        optie = st.sidebar.radio("Selecteer een optie", ("Login", "Registreer"))

        if optie == "Login":
            login()
        elif optie == "Registreer":
            register()

if __name__ == "__main__":
    main()
