import streamlit as st
import gspread
import pandas as pd
import json
import time

# --- 1. CONFIGURATION & DESIGN "DOUX" ---
st.set_page_config(page_title="Heiwa", page_icon="🌸", layout="centered")

# CSS pour injecter de la douceur
st.markdown("""
    <style>
    /* Fond de page crème doux */
    .stApp {
        background-color: #FFFDF5;
    }
    /* Style des titres */
    h1, h2, h3 {
        color: #5D4037;
        font-family: 'Lexend', sans-serif;
    }
    /* Bulles de messages arrondies */
    div[data-testimonial="true"], .stChatMessage {
        background-color: #FFFFFF !important;
        border-radius: 25px !important;
        border: 1px solid #FFE0B2 !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    /* Boutons joyeux */
    .stButton>button {
        border-radius: 20px;
        background-color: #FFECB3;
        border: none;
        color: #5D4037;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFE082;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONNEXION GOOGLE SHEETS ---
@st.cache_resource
def connect_to_sheet():
    service_account_info = json.loads(st.secrets["connections"]["gsheets"]["service_account"])
    gc = gspread.service_account_from_dict(service_account_info)
    sh = gc.open_by_key("1kqgDes1pF13T5VrM7P-Qcd69UaxG5I3E-n0Lq_6J6Vw")
    return sh.get_worksheet(0)

try:
    worksheet = connect_to_sheet()
except Exception as e:
    st.error("Connexion en cours...")
    st.stop()

# --- 3. ARCHITECTURE (MENU LATÉRAL) ---
st.sidebar.title("🌸 Heiwa")
st.sidebar.markdown("Ton refuge de poche.")
page = st.sidebar.radio("Où veux-tu aller ?", ["Le Mur", "La Bulle", "Inspiration"])

# --- PAGE 1 : LE MUR (TON CODE ACTUEL) ---
if page == "Le Mur":
    st.title("💬 Le Mur de Bienveillance")
    st.write("Dépose une pensée, repars avec un sourire.")

    with st.form("form_paix", clear_on_submit=True):
        nom = st.text_input("Ton prénom")
        message = st.text_area("Ton message de douceur")
        submit = st.form_submit_button("Diffuser la joie")

        if submit and nom and message:
            worksheet.append_row([nom, message])
            st.success("C'est envoyé !")
            st.balloons()

    st.divider()
    data = pd.DataFrame(worksheet.get_all_records())
    if not data.empty:
        for i, row in data.iloc[::-1].iterrows():
            with st.chat_message("user", avatar="✨"):
                st.write(f"**{row['Auteur']}**")
                st.write(row['Message'])

# --- PAGE 2 : LA BULLE (RESPIRATION) ---
elif page == "La Bulle":
    st.title("🌬️ La Bulle de Respiration")
    st.write("Suis le mouvement de la bulle pour apaiser ton esprit.")
    
    st.info("Inspire quand la barre monte, expire quand elle descend.")
    
    # Simulation d'une barre de respiration douce
    placeholder = st.empty()
    if st.button("Démarrer une session (1 min)"):
        for i in range(6):  # 6 cycles de 10 secondes
            # Inspir
            for progress in range(0, 101, 5):
                placeholder.progress(progress, text="🌿 Inspiration...")
                time.sleep(0.1)
            # Expir
            for progress in range(100, -1, -5):
                placeholder.progress(progress, text="✨ Expiration...")
                time.sleep(0.1)
        st.success("Bravo. Tu as pris un instant pour toi.")

# --- PAGE 3 : INSPIRATION ---
elif page == "Inspiration":
    st.title("✨ Jardin d'Inspiration")
    citations = [
        "Chaque petit pas compte.",
        "Tu es assez, tel(le) que tu es.",
        "La paix commence par un sourire.",
        "Sois doux avec toi-même aujourd'hui.",
        "Le ciel est toujours bleu derrière les nuages."
    ]
    
    st.subheader("Ton mantra du moment :")
    import random
    st.warning(f"### {random.choice(citations)}")
    
    if st.button("Une autre pensée ?"):
        st.rerun()
