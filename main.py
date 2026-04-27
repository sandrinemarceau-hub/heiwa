import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Heiwa", page_icon="🌸")

# Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🌸 Heiwa")

with st.form("form_paix", clear_on_submit=True):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Ton message")
    envoyer = st.form_submit_button("Partager")

    if envoyer and nom and message:
        try:
            # 1. On lit uniquement les colonnes A et B pour éviter les colonnes fantômes
            df = conn.read(worksheet="Feuille1", usecols=[0, 1])
            
            # 2. On s'assure que le tableau a les bons noms de colonnes
            df.columns = ["Auteur", "Message"]
            
            # 3. On crée la nouvelle ligne proprement
            nouveau = pd.DataFrame([{"Auteur": nom, "Message": message}])
            
            # 4. On fusionne
            df_final = pd.concat([df, nouveau], ignore_index=True)
            
            # 5. On renvoie tout à Google
            conn.update(worksheet="Feuille1", data=df_final)
            
            st.success("Message envoyé !")
            st.balloons()
        except Exception as e:
            st.error(f"Erreur technique : {e}")

st.divider()

# --- AFFICHAGE ---
st.subheader("💬 Mur de bienveillance")
try:
    # On affiche les messages en ignorant les lignes vides
    data = conn.read(worksheet="Feuille1", ttl=0).dropna(subset=["Auteur", "Message"])
    for i, row in data.iloc[::-1].iterrows():
        st.info(f"**{row['Auteur']}** : {row['Message']}")
except:
    st.write("Le mur est prêt à recevoir tes premiers mots.")
