import streamlit as st
import gspread
import pandas as pd
import json
import time
import random

# --- 1. DESIGN & STYLE (Inchangé pour la cohérence) ---
st.set_page_config(page_title="Heiwa", page_icon="🌸", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Quicksand', sans-serif;
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 30px !important;
        background: linear-gradient(90deg, #FFDEE9 0%, #B5FFFC 100%) !important;
        color: #4A4A4A !important;
        font-weight: 600 !important;
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
menu = st.sidebar.radio("Où veux-tu aller ?", ["💬 Le Mur", "🧘 Timer Zen", "📖 Inspiration"])

# --- PAGE 1 : LE MUR (Inchangé) ---
if menu == "💬 Le Mur":
    st.title("Le Mur de Bienveillance")
    nom = st.text_input("Ton prénom", placeholder="Amélie")
    humeur = st.selectbox("Ton énergie", ["✨ Joie", "🌿 Calme", "💖 Amour", "☁️ Besoin d'écoute"])
    message = st.text_area("Ton message", placeholder="Écris quelque chose de doux...")
    
    if st.button("Diffuser cette énergie"):
        if nom and message:
            worksheet.append_row([nom, message, humeur])
            st.balloons()
            st.rerun()

    st.divider()
    data = pd.DataFrame(worksheet.get_all_records())
    if not data.empty:
        for i, row in data.iloc[::-1].iterrows():
            with st.chat_message("user", avatar="🌸"):
                st.write(f"**{row['Auteur']}** • {row.get('Energie', '✨')}")
                st.write(row['Message'])

# --- PAGE 2 : TIMER ZEN (NOUVEAU) ---
elif menu == "🧘 Timer Zen":
    st.title("Espace Méditation")
    st.write("Prends un instant pour te reconnecter à ton souffle.")
    
    col1, col2 = st.columns(2)
    with col1:
        duree = st.slider("Durée totale (minutes)", 2, 20, 10)
    with col2:
        mode = st.radio("Style", ["Recommandé (Mixte)", "Simple", "Carrée"])

    if st.button("Commencer la session"):
        st.write(f"C'est parti pour {duree} minutes de calme...")
        progress_bar = st.empty()
        instruction = st.empty()
        
        start_time = time.time()
        end_time = start_time + (duree * 60)
        half_time = start_time + (duree * 30) # Pour le mode recommandé

        while time.time() < end_time:
            current_time = time.time()
            elapsed_total = (current_time - start_time) / (duree * 60)
            progress_bar.progress(min(elapsed_total, 1.0))

            # Logique du Mode Recommandé (5 min simple + 5 min carrée)
            if mode == "Recommandé (Mixte)":
                if current_time < half_time:
                    # Respiration Simple (5s inspir / 5s expir)
                    instruction.markdown("### 🌬️ Respiration Simple : Inspire...")
                    time.sleep(5)
                    instruction.markdown("### 🌬️ Respiration Simple : Expire...")
                    time.sleep(5)
                else:
                    # Respiration Carrée (4s par phase)
                    instruction.markdown("### 🧊 Carrée : Inspire (4s)")
                    time.sleep(4)
                    instruction.markdown("### 🧊 Carrée : Bloque plein (4s)")
                    time.sleep(4)
                    instruction.markdown("### 🧊 Carrée : Expire (4s)")
                    time.sleep(4)
                    instruction.markdown("### 🧊 Carrée : Bloque vide (4s)")
                    time.sleep(4)
            
            # Logique Simple uniquement
            elif mode == "Simple":
                instruction.markdown("### 🌬️ Inspire...")
                time.sleep(5)
                instruction.markdown("### 🌬️ Expire...")
                time.sleep(5)
                
            # Logique Carrée uniquement
            elif mode == "Carrée":
                instruction.markdown("### 🧊 Inspire (4s)")
                time.sleep(4)
                instruction.markdown("### 🧊 Bloque plein (4s)")
                time.sleep(4)
                instruction.markdown("### 🧊 Expire (4s)")
                time.sleep(4)
                instruction.markdown("### 🧊 Bloque vide (4s)")
                time.sleep(4)

        st.success("Session terminée. Merci pour ce moment de paix.")
        st.balloons()

# --- PAGE 3 : INSPIRATION (Inchangé) ---
elif menu == "📖 Inspiration":
    st.title("Le Journal d'Inspiration")
    citations = [
        {"texte": "Rien n'est permanent, sauf le changement. Souris-lui.", "auteur": "Héraclite"},
        {"texte": "Le bonheur est la seule chose qui se double quand on le partage.", "auteur": "Albert Schweitzer"},
        {"texte": "Tu es le ciel. Tout le reste, c'est juste le temps qu'il fait.", "auteur": "Pema Chödrön"}
    ]
    cit = random.choice(citations)
    st.markdown(f"""
    <div style="background: white; padding: 40px; border-radius: 30px; border-left: 10px solid #FFDEE9;">
        <h2 style="font-style: italic;">"{cit['texte']}"</h2>
        <p style="text-align: right;">— {cit['auteur']}</p>
    </div>
    """, unsafe_allow_html=True)
