import streamlit as st
import random

# Configuration de la page
st.set_page_config(page_title="Heiwa", page_icon="🌸")

# --- STYLE ---
# Correction ici : "unsafe_allow_html" au lieu de "unsafe_allow_status"
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { border-radius: 20px; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- INSPIRATION ---
citations = [
    "La bienveillance est le langage qu'un sourd peut entendre. — Mark Twain",
    "La paix commence par un sourire. — Mère Teresa",
    "La douceur surpasse la force. — Proverbe japonais"
]

st.title("🌸 Heiwa")
st.subheader("Ton sanctuaire de bienveillance")

# Affichage de la pensée du jour
st.info(random.choice(citations))

st.divider()

# --- ESPACE DE PARTAGE ---
st.write("### ✍️ Partager une pensée ou un merci")

with st.form("formulaire_message", clear_on_submit=True):
    nom = st.text_input("Ton prénom / Pseudo")
    message = st.text_area("Ton message de paix")
    envoyer = st.form_submit_button("Diffuser la lumière")

    if envoyer:
        if nom and message:
            st.success(f"Merci {nom} ! Ton message a été entendu.")
            st.balloons() 
        else:
            st.warning("Pense à remplir les deux champs pour partager ta douceur.")

st.write("---")
st.write("*Note : La mémoire persistante du forum est en cours de construction...*")
