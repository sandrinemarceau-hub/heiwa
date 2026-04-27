import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Heiwa", page_icon="🌸")

# Connexion simplifiée
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🌸 Heiwa")

# --- FORMULAIRE ---
with st.form("form_paix"):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Ton message")
    envoyer = st.form_submit_button("Partager")

    if envoyer and nom and message:
        try:
            # On lit la feuille (Onglet "Feuille1")
            df = conn.read(worksheet="Feuille1")
            # On ajoute le message
            nouveau = pd.DataFrame([{"Auteur": nom, "Message": message}])
            df_final = pd.concat([df, nouveau], ignore_index=True)
            # On sauvegarde
            conn.update(worksheet="Feuille 1", data=df_final)
            st.success("Message envoyé !")
            st.balloons()
        except Exception as e:
            st.error(f"Erreur : {e}")

st.divider()

# --- AFFICHAGE ---
st.subheader("💬 Mur de bienveillance")
try:
    data = conn.read(worksheet="Feuille1")
    for i, row in data.iloc[::-1].iterrows():
        st.write(f"**{row['Auteur']}** : {row['Message']}")
except:
    st.write("Le mur est vide ou inaccessible.")
