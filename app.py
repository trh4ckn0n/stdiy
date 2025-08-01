import streamlit as st
import plotly.graph_objects as go
import openai
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="trhacknon Galaxy Resin DIY",
    layout="wide",
    page_icon="🌌"
)

st.markdown("""
<style>
    body {
        background-color: #0d1117;
        color: #39ff14;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #39ff14;
        text-shadow: 0 0 5px #39ff14;
    }
    .stApp {
        background-color: #0d1117;
    }
    .stDataFrame {
        border: 1px solid #00ffe0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("trhacknon 🌌 Galaxy Resin DIY Generator")

menu = st.sidebar.selectbox("Menu", ["Création Galaxie", "Historique"])

if menu == "Création Galaxie":
    st.subheader("🔮 Choix des Paramètres")

    moules = {
        "Pyramide": "https://i.etsystatic.com/34814506/r/il/40b456/3917186865/il_570xN.3917186865_s5sv.jpg",
        "Boite Tête de mort": "https://m.media-amazon.com/images/I/513vg6lD4GL.jpg",
        "Grinder": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSinrnqVnjtwIBqyWnq2MZW-6p_URLYg6F0ymo7cSQZtA&s",
        "Sous-verre": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTa5RAhlRYEUqQFrpG2pXvZRaiepR8IpujgkUoTnrWyTQ&s",
        "Pendentif Treelife": "https://m.media-amazon.com/images/I/71GxpyDaklL.jpg",
        "Cendrier Carré": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT61lD4K_0t9SU3S2IezfFyon3TzD8nhwoSm0roc4CEHw&s"
    }

    choix_moule = st.selectbox("🔍 Choisis ton moule", list(moules.keys()))
    st.image(moules[choix_moule], width=250)

    poudres_mica = [
        "Bleu Galaxy", "Violet Iridescent", "Rose Fuchsia", "Or Scintillant", 
        "Vert Néon", "Noir Profond", "Blanc Nacré", "Turquoise Mystique"
    ]
    encres = ["Encre Alcool Bleue", "Encre Violette", "Encre Rose", "Encre Blanche"]

    couleurs_mica = st.multiselect("🖊️ Choisis les couleurs de mica", poudres_mica)
    encres_choisies = st.multiselect("🎨 Encres à alcool", encres)

    base = st.number_input("Base du moule (cm)", value=10.0)
    hauteurs = []
    cols = st.columns(5)
    default_hauteurs = [2.0, 2.5, 3.0, 1.5, 1.0]
    for i in range(5):
        with cols[i]:
            h = st.number_input(f"Hauteur couche {i+1} (cm)", min_value=0.0, value=default_hauteurs[i])
            hauteurs.append(h)

    def pyramide_volume(b, h):
        return (1/3) * (b ** 2) * h

    def base_at_height(total_h, current_h, base):
        return (base * current_h) / total_h

    full_height = sum(hauteurs)
    cumulative_heights = [sum(hauteurs[:i+1]) for i in range(len(hauteurs))]

    layer_volumes = []
    last_vol = 0
    for h in cumulative_heights:
        b = base_at_height(full_height, h, base)
        vol = pyramide_volume(b, h)
        layer_volumes.append(vol - last_vol)
        last_vol = vol

    density = 1.1
    resin_weights = [v * density for v in layer_volumes]

    st.subheader("📊 Détails des couches")
    data = {
        "Couche": [f"Couche {i+1}" for i in range(5)],
        "Hauteur (cm)": hauteurs,
        "Volume (cm³)": [round(v, 2) for v in layer_volumes],
        "Poids total (g)": [round(w, 2) for w in resin_weights],
        "Résine (g)": [round(w / 2, 2) for w in resin_weights],
        "Durcisseur (g)": [round(w / 2, 2) for w in resin_weights],
    }
    st.dataframe(data, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"C{i+1}" for i in range(5)],
        y=resin_weights,
        text=[f"{round(w)} g" for w in resin_weights],
        textposition="outside",
        marker_color="#39ff14"
    ))
    fig.update_layout(
        title="🔮 Poids résine par couche",
        xaxis_title="Couche",
        yaxis_title="Grammes",
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#00ffe0"),
    )
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🌌 Générer fiche Galaxie"):
        prompt = f"""
        Crée une fiche technique en français pour réaliser un effet galaxie en résine à partir de ces choix:
        Moule: {choix_moule},
        Couleurs mica: {', '.join(couleurs_mica)},
        Encres à alcool: {', '.join(encres_choisies)}.
        Donne une procédure étape par étape avec précautions, durées de séchage, et conseils créatifs.
        """
        with st.spinner("✍️ Rédaction de la fiche..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            fiche = response.choices[0].message.content
            st.markdown(f"### 📄 Fiche Galaxie\n{fiche}")

        dalle_prompt = f"galaxy effect in epoxy resin with {', '.join(couleurs_mica)} pigments in {choix_moule} mold"
        with st.spinner("🎨 Génération image DALL·3..."):
            dalle_response = openai.Image.create(prompt=dalle_prompt, n=1, size="512x512")
            image_url = dalle_response['data'][0]['url']
            st.image(image_url, caption="Prévisualisation de l'effet galaxie")

        historique = {
            "date": datetime.now().isoformat(),
            "moule": choix_moule,
            "couleurs_mica": couleurs_mica,
            "encres": encres_choisies,
            "fiche": fiche,
            "image_url": image_url
        }
        with open("historique_galaxie.json", "a") as f:
            f.write(json.dumps(historique) + "\n")

elif menu == "Historique":
    st.subheader("🔍 Historique des fiches Galaxie")
    if os.path.exists("historique_galaxie.json"):
        with open("historique_galaxie.json", "r") as f:
            lines = f.readlines()
        for line in lines[::-1]:
            h = json.loads(line)
            st.markdown(f"#### 📅 {h['date']}")
            st.markdown(f"**Moule**: {h['moule']}  ")
            st.markdown(f"**Mica**: {', '.join(h['couleurs_mica'])}  ")
            st.markdown(f"**Encres**: {', '.join(h['encres'])}  ")
            st.image(h["image_url"], width=200)
            with st.expander("📄 Fiche Technique"):
                st.markdown(h["fiche"])
