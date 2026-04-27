import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Heiwa", page_icon="🌸")

# Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🌸 Heiwa")

# --- FORMULAIRE ---
with st.form("form_paix"):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Ton message")
    envoyer = st.form_submit_button("Partager")

    if envoyer and nom and message:
        try:
            # ON UTILISE "Feuille1" SANS ESPACE
            df = conn.read(worksheet="Feuille1")
            nouveau = pd.DataFrame([{"Auteur": nom, "Message": message}])
            df_final = pd.concat([df, nouveau], ignore_index=True)
            conn.update(worksheet="Feuille1", data=df_final)
            st.success("Message envoyé !")
            st.balloons()
        except Exception as e:
            st.error(f"Erreur lors de l'envoi : {e}")

st.divider()

# --- AFFICHAGE ---
st.subheader("💬 Mur de bienveillance")
try:
    # ON UTILISE "Feuille1" SANS ESPACE
    data = conn.read(worksheet="Feuille1")
    if not data.empty:
        for i, row in data.iloc[::-1].iterrows():
            st.write(f"**{row['Auteur']}** : {row['Message']}")
    else:
        st.write("Le mur est vide pour l'instant.")
except Exception as e:
    st.write("Le mur est inaccessible. Vérifie le nom de l'onglet.")
