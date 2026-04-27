import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import random

# 1. CONFIGURATION ET NETTOYAGE
st.set_page_config(page_title="Heiwa", page_icon="🌸")

# On récupère le lien des secrets et on force la suppression des caractères invisibles
try:
    url_brute = st.secrets["connections"]["gsheets"]["spreadsheet"]
    url_propre = url_brute.strip().replace("\n", "").replace("\r", "")
except Exception:
    st.error("Le lien Google Sheets est introuvable dans les Secrets.")
    st.stop()

# Création de la connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# --- STYLE ---
st.markdown("<style>.main { background-color: #f8f9fa; }</style>", unsafe_allow_html=True)

st.title("🌸 Heiwa")

# --- INSPIRATION ---
citations = ["La paix commence par un sourire.", "La douceur surpasse la force.", "Ecouter est un cadeau."]
st.info(random.choice(citations))

st.divider()

# --- FORMULAIRE ---
with st.form("paix_form", clear_on_submit=True):
    nom = st.text_input("Ton prénom")
    texte = st.text_area("Ton message de bienveillance")
    submit = st.form_submit_button("Diffuser")

    if submit and nom and texte:
        try:
            # On utilise le lien PROPRE ici pour éviter l'erreur InvalidURL
            existing_data = conn.read(spreadsheet=url_propre)
            new_entry = pd.DataFrame([{"Auteur": nom, "Message": texte}])
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
            conn.update(spreadsheet=url_propre, data=updated_df)
            st.success("Merci pour ce partage !")
            st.balloons()
        except Exception as e:
            st.error(f"Erreur lors de l'envoi : {e}")

# --- AFFICHAGE ---
st.subheader("💬 Le mur de la bienveillance")
try:
    # On lit avec le lien PROPRE
    data = conn.read(spreadsheet=url_propre)
    if not data.empty:
        for index, row in data.iloc[::-1].iterrows():
            with st.chat_message("user", avatar="✨"):
                st.write(f"**{row['Auteur']}**")
                st.write(row['Message'])
    else:
        st.write("Le mur est encore vide, sois le premier à écrire !")
except Exception as e:
    st.error("Impossible d'afficher les messages pour le moment.")
