import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Heiwa", page_icon="🌸")

# Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🌸 Heiwa")

# --- FORMULAIRE ---
with st.form("form_paix", clear_on_submit=True):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Ton message")
    envoyer = st.form_submit_button("Partager")

    if envoyer:
        if not nom or not message:
            st.warning("Merci de remplir tous les champs.")
        else:
            try:
                # 1. On lit les données existantes
                df = conn.read(worksheet="Feuille1")
                
                # 2. On prépare la nouvelle ligne
                # On s'assure que les noms "Auteur" et "Message" sont identiques à la feuille
                nouveau_message = pd.DataFrame([{"Auteur": nom, "Message": message}])
                
                # 3. On ajoute la ligne au tableau
                df_final = pd.concat([df, nouveau_message], ignore_index=True)
                
                # 4. On renvoie tout à Google
                conn.update(worksheet="Feuille1", data=df_final)
                
                st.success("Message diffusé avec succès !")
                st.balloons()
            except Exception as e:
                st.error(f"Détail de l'erreur : {e}")

st.divider()

# --- AFFICHAGE ---
st.subheader("💬 Mur de bienveillance")
try:
    # On force le rafraîchissement des données (ttl=0)
    data = conn.read(worksheet="Feuille1", ttl=0)
    if not data.empty:
        # On affiche du plus récent au plus ancien
        for i, row in data.iloc[::-1].iterrows():
            st.info(f"**{row['Auteur']}** : {row['Message']}")
except Exception as e:
    st.write("Le mur se prépare... actualisez dans quelques instants.")
