import streamlit as st
import random

# Configuration
st.set_page_config(page_title="Heiwa", page_icon="🌸")

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { border-radius: 20px; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_status=True)

# --- INSPIRATION ---
citations = [
    "La bienveillance est le langage qu'un sourd peut entendre. — Mark Twain",
    "La paix commence par un sourire. — Mère Teresa",
    "La douceur surpasse la force. — Proverbe japonais"
]

st.title("🌸 Heiwa")
st.subheader("Ton sanctuaire de bienveillance")

# Affichage de la pensée du jour dans un encadré bleu
st.info(random.choice(citations))

st.divider()

# --- ESPACE DE PARTAGE ---
st.write("### ✍️ Partager une pensée ou un merci")

# Création du formulaire
with st.form("formulaire_message", clear_on_submit=True):
    nom = st.text_input("Ton prénom / Pseudo")
    message = st.text_area("Ton message de paix")
    envoyer = st.form_submit_button("Diffuser la lumière")

    if envoyer:
        if nom and message:
            st.success(f"Merci {nom} ! Ton message a été entendu par le cœur du forum.")
            # Pour l'instant, le message s'affiche juste ici. 
            # On connectera la "mémoire" (Google Sheet) juste après.
            st.balloons() 
        else:
            st.warning("Pense à remplir les deux champs pour partager ta douceur.")

# --- AFFICHAGE TEMPORAIRE ---
st.write("---")
st.write("*Note : La mémoire persistante du forum est en cours de construction...*")
