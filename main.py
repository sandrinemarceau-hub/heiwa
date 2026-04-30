import streamlit as st
import gspread
import pandas as pd
import json
import time
import random

# --- 1. DESIGN AVANCÉ (CSS) ---
st.set_page_config(page_title="Heiwa", page_icon="🌸", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Quicksand', sans-serif;
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }

    /* Cartes Glassmorphism */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        margin-bottom: 15px !important;
    }

    /* Style du menu latéral */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
    }

    /* Boutons personnalisés */
    .stButton>button {
        width: 100%;
        border-radius: 30px !important;
        border: none !important;
        background: linear-gradient(90deg, #FFDEE9 0%, #B5FFFC 100%) !important;
        color: #4A4A4A !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONNEXION ---
@st.cache_resource
def connect_to_sheet():
    info = json.loads(st.secrets["connections"]["gsheets"]["service_account"])
    gc = gspread.service_account_from_dict(info)
    sh = gc.open_by_key("1kqgDes1pF13T5VrM7P-Qcd69UaxG5I3E-n0Lq_6J6Vw")
    return sh.get_worksheet(0)

worksheet = connect_to_sheet()

# --- 3. NAVIGATION ---
st.sidebar.markdown("# 🌸 Heiwa")
menu = st.sidebar.selection_state = st.sidebar.radio(
    "Navigation", 
    ["💬 Le Mur", "🌬️ Respiration", "📖 Journal d'Or"]
)

# --- PAGE 1 : LE MUR ---
if menu == "💬 Le Mur":
    st.title("Le Mur de Bienveillance")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        nom = st.text_input("Ton prénom", placeholder="Ex: Amélie")
    with col2:
        humeur = st.selectbox("Ton énergie", ["✨ Joie", "🌿 Calme", "💖 Amour", "☁️ Besoin d'écoute"])

    message = st.text_area("Ton message", placeholder="Écris quelque chose de doux...")
    
    if st.button("Diffuser cette énergie"):
        if nom and message:
            worksheet.append_row([nom, message, humeur])
            st.balloons()
            st.rerun()

    st.divider()

    # Affichage des messages
    data = pd.DataFrame(worksheet.get_all_records())
    if not data.empty:
        # On s'assure que la colonne 'Energie' existe pour les anciens messages
        if 'Energie' not in data.columns: data['Energie'] = "✨ Douceur"
        
        for i, row in data.iloc[::-1].iterrows():
            with st.chat_message("user", avatar="🌸"):
                st.write(f"**{row['Auteur']}** • {row.get('Energie', '✨')}")
                st.write(row['Message'])

# --- PAGE 2 : RESPIRATION (VERSION AMÉLIORÉE) ---
elif menu == "🌬️ Respiration":
    st.title("La Bulle de Paix")
    st.write("Ferme les yeux, ou fixe simplement la barre.")
    
    if st.button("Commencer le cycle"):
        placeholder = st.empty()
        for _ in range(3):
            # Phase d'inspiration
            for i in range(101):
                placeholder.markdown(f"""
                <div style="text-align:center;">
                    <div style="height:20px; width:{i}%; background:linear-gradient(90deg, #B5FFFC, #FFDEE9); border-radius:10px;"></div>
                    <p style="font-size:24px; margin-top:20px;">🌿 Inspire...</p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.04)
            time.sleep(1) # Rétention
            # Phase d'expiration
            for i in range(100, -1, -1):
                placeholder.markdown(f"""
                <div style="text-align:center;">
                    <div style="height:20px; width:{i}%; background:linear-gradient(90deg, #B5FFFC, #FFDEE9); border-radius:10px;"></div>
                    <p style="font-size:24px; margin-top:20px;">✨ Expire...</p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.06)
        st.success("Ton esprit est plus léger.")

# --- PAGE 3 : JOURNAL D'OR ---
elif menu == "📖 Journal d'Or":
    st.title("Le Journal d'Inspiration")
    st.write("Une pensée choisie pour toi, ici et maintenant.")
    
    citations = [
        {"texte": "Rien n'est permanent, sauf le changement. Souris-lui.", "auteur": "Héraclite"},
        {"texte": "Le bonheur est la seule chose qui se double quand on le partage.", "auteur": "Albert Schweitzer"},
        {"texte": "Tu es le ciel. Tout le reste, c'est juste le temps qu'il fait.", "auteur": "Pema Chödrön"}
    ]
    cit = random.choice(citations)
    
    st.markdown(f"""
    <div style="background: white; padding: 40px; border-radius: 30px; border-left: 10px solid #FFDEE9; box-shadow: 10px 10px 30px rgba(0,0,0,0.05);">
        <h2 style="font-style: italic; color: #5D4037;">"{cit['texte']}"</h2>
        <p style="text-align: right; font-weight: bold;">— {cit['auteur']}</p>
    </div>
    """, unsafe_allow_html=True)
