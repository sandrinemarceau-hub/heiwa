import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Heiwa", page_icon="🌸")

# Connexion avec ta clé (Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🌸 Heiwa")

# --- FORMULAIRE ---
with st.form("form_final", clear_on_submit=True):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Ton message")
    envoyer = st.form_submit_button("Partager")

    if envoyer and nom and message:
        try:
            # On lit la première feuille disponible
            df = conn.read()
            
            # On ajoute le message
            nouveau = pd.DataFrame([{"Auteur": nom, "Message": message}])
            df_final = pd.concat([df, nouveau], ignore_index=True)
            
            # On sauvegarde
            conn.update(data=df_final)
            st.success("C'est en ligne ! Merci pour ta bienveillance.")
            st.balloons()
        except Exception as e:
            st.error(f"Erreur d'envoi : {e}")

st.divider()

# --- AFFICHAGE ---
st.subheader("💬 Mur de bienveillance")
try:
    # On lit la première feuille disponible avec rafraîchissement (ttl=0)
    data = conn.read(ttl=0)
    if not data.empty:
        for i, row in data.iloc[::-1].iterrows():
            st.info(f"**{row['Auteur']}** : {row['Message']}")
except Exception as e:
    st.error(f"Erreur d'affichage : {e}")
