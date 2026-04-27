import streamlit as st
import random
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuration
st.set_page_config(page_title="Heiwa", page_icon="🌸")

# Connexion à Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌸 Heiwa")
st.write("Un espace pour respirer et partager.")

# --- INSPIRATION ---
citations = ["La paix commence par un sourire.", "La douceur surpasse la force.", "Ecouter est un cadeau."]
st.info(random.choice(citations))

st.divider()

# --- FORMULAIRE D'ENVOI ---
with st.form("paix_form", clear_on_submit=True):
    nom = st.text_input("Ton prénom")
    texte = st.text_area("Ton message de bienveillance")
    submit = st.form_submit_button("Diffuser")

    if submit and nom and texte:
        # Lire les données actuelles
        existing_data = conn.read(worksheet="Feuille 1", usecols=[0,1])
        # Créer une nouvelle ligne
        new_entry = pd.DataFrame([{"Auteur": nom, "Message": texte}])
        # Fusionner et sauvegarder (on utilise ici une version simplifiée pour le test)
        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        conn.update(worksheet="Feuille 1", data=updated_df)
        st.success("Merci pour ce partage !")
        st.balloons()

# --- AFFICHAGE DES MESSAGES ---
st.subheader("💬 Le mur de la bienveillance")
# Recharger les données pour voir le dernier message
data = conn.read(worksheet="Feuille 1")

for index, row in data.iloc[::-1].iterrows(): # Affiche du plus récent au plus ancien
    with st.chat_message("user", avatar="✨"):
        st.write(f"**{row['Auteur']}**")
        st.write(row['Message'])
