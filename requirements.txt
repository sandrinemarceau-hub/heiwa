import streamlit as st
import gspread
import pandas as pd
import json

# 1. CONFIGURATION
st.set_page_config(page_title="Heiwa", page_icon="🌸")

# 2. CONNEXION SÉCURISÉE (On déballe la clé JSON)
@st.cache_resource
def connect_to_sheet():
    # On récupère le JSON dans les secrets
    service_account_info = json.loads(st.secrets["connections"]["gsheets"]["service_account"])
    # On se connecte via gspread
    gc = gspread.service_account_from_dict(service_account_info)
    # On ouvre la feuille par son ID
    sh = gc.open_by_key("1kqgDes1pF13T5VrM7P-Qcd69UaxG5I3E-n0Lq_6J6Vw")
    return sh.get_worksheet(0) # On prend la première feuille

try:
    worksheet = connect_to_sheet()
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.info("💡 Vérifie bien que l'e-mail du bot est 'Éditeur' sur ta Google Sheet.")
    st.stop()

st.title("🌸 Heiwa")
st.write("Un espace de paix partagé.")

# --- FORMULAIRE D'ENVOI ---
with st.form("form_paix", clear_on_submit=True):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Ton message de bienveillance")
    submit = st.form_submit_button("Diffuser")

    if submit and nom and message:
        # On ajoute la ligne directement dans Google Sheets
        worksheet.append_row([nom, message])
        st.success("Message envoyé !")
        st.balloons()

st.divider()

# --- AFFICHAGE DU MUR ---
st.subheader("💬 Mur de la bienveillance")
# On récupère toutes les données
data = pd.DataFrame(worksheet.get_all_records())

if not data.empty:
    # On affiche du plus récent au plus ancien
    for i, row in data.iloc[::-1].iterrows():
        with st.chat_message("user", avatar="✨"):
            st.write(f"**{row['Auteur']}**")
            st.write(row['Message'])
else:
    st.write("Le mur est encore vide, sois le premier !")
