import streamlit as st
import random

# Configuration de la page (Le titre dans l'onglet du navigateur)
st.set_page_config(page_title="Heiwa", page_icon="🌸")

# --- LE COIN CITATION ---
citations = [
    "La bienveillance est le langage qu'un sourd peut entendre et qu'un aveugle peut voir. — Mark Twain",
    "Soyez le changement que vous voulez voir dans le monde. — Gandhi",
    "Chaque pensée positive est une prière silencieuse qui changera votre vie. — Sivananda",
    "La paix commence par un sourire. — Mère Teresa",
    "La douceur surpasse la force. — Proverbe japonais"
]

# On choisit une citation au hasard
pensee_du_jour = random.choice(citations)

# Affichage esthétique
st.title("🌸 Heiwa")
st.markdown(f"> **La pensée du moment :**\n> *{pensee_du_jour}*")

st.divider() # Une petite ligne de séparation élégante

st.write("Bienvenue dans cet espace de calme. Prenez une grande inspiration...")
