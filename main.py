import streamlit as st
import pandas as pd
from gspread_pandas import Spread, Client

st.title("🌸 Heiwa - Mode Secours")

# On essaie une lecture ultra-directe
try:
    # On récupère l'ID directement
    sheet_id = "1kqgDes1pF13T5VrM7P-Qcd69UaxG5I3E-n0Lq_6J6Vw"
    
    # On affiche un message de patience
    with st.spinner("Connexion au mur de bienveillance..."):
        # On utilise une méthode de lecture différente
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
        data = pd.read_csv(url)
        
    st.success("Connexion établie !")
    
    for i, row in data.iloc[::-1].iterrows():
        st.info(f"**{row['Auteur']}** : {row['Message']}")

except Exception as e:
    st.error(f"Désolé, le mur est encore timide. Erreur : {e}")
    st.info("Vérifie bien que ton Google Sheet est en 'Tous les utilisateurs disposant du lien : LECTEUR' pour ce test.")
