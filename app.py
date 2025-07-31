import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────
# 🔧 CONFIGURATION GLOBALE
# ─────────────────────────────
st.set_page_config(
    page_title="Résine DIY - trhacknon",
    layout="wide",
    page_icon="🧪"
)

# CSS hacker style
st.markdown("""
    <style>
        body {
            background-color: #0d1117;
            color: #39ff14;
        }
        .stApp {
            background-color: #0d1117;
        }
        h1, h2, h3 {
            color: #39ff14;
            text-shadow: 0 0 5px #39ff14;
        }
        .stDataFrame {
            border: 1px solid #00ffe0;
            border-radius: 8px;
        }
        .block-container {
            padding: 2rem;
        }
        .css-1d391kg, .css-18e3th9 {
            background-color: #0d1117 !important;
        }
        @keyframes glow {
            0% { text-shadow: 0 0 5px #39ff14; }
            50% { text-shadow: 0 0 15px #00ffe0; }
            100% { text-shadow: 0 0 5px #39ff14; }
        }
        h1 {
            animation: glow 2s infinite;
        }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# 📋 MENU
# ─────────────────────────────
menu = st.sidebar.selectbox("🔽 Choisir une section", ["Pyramide Résine", "Effet Galaxie"])

# ─────────────────────────────
# PYRAMIDE
# ─────────────────────────────
if menu == "Pyramide Résine":
    st.title("🔺 Calcul Pyramide Résine - trhacknon")

    base = st.number_input("📐 Base de la pyramide (cm)", value=15.0)

    hauteurs = []
    cols = st.columns(5)
    default_hauteurs = [3.0, 2.0, 4.0, 3.0, 3.0]
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

    density = 1.1  # g/cm³
    resin_weights = [v * density for v in layer_volumes]

    st.subheader("📊 Détails par couche")
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
        title="⚗️ Poids total de résine par couche",
        xaxis_title="Couche",
        yaxis_title="Grams",
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#00ffe0"),
    )
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────
# GALAXY EFFECT
# ─────────────────────────────
if menu == "Effet Galaxie":
    st.title("🌌 Création Effet Galaxie - Résine DIY")

    nb_couches = st.slider("Nombre de couches effet galaxie", min_value=1, max_value=10, value=4)
    encre_choices = st.multiselect("🎨 Couleurs d'encres à alcool", [
        "Violet", "Bleu galaxie", "Rose magenta", "Noir", "Or métallisé", "Argent"
    ], default=["Violet", "Bleu galaxie"])

    mica_choices = st.multiselect("✨ Poudre de mica à utiliser", [
        "Blanc nacré", "Bleu nuit", "Violet profond", "Or antique", "Noir scintillant"
    ], default=["Blanc nacré", "Violet profond"])

    st.subheader("🧪 Recette Estimée")
    resine_totale = nb_couches * 60  # 60ml par couche estimée
    st.markdown(f"""
    - Résine epoxy totale : **{resine_totale} ml**  
    - Durcisseur (50%) : **{resine_totale / 2:.1f} ml**  
    - Encre à alcool : **2 à 3 gouttes par couleur/couche**  
    - Mica : **1/4 cuillère par couche**  
    """, unsafe_allow_html=True)

    st.subheader("📋 Étapes recommandées")
    st.markdown("""
    1. Préparer la résine et diviser en couches  
    2. Ajouter l’encre à alcool + mica dans chaque couche  
    3. Couler lentement chaque couche en conservant l'effet tourbillon  
    4. Ajouter des gouttes d’encre directement dans la résine pour effet nébuleuse  
    5. Laisser durcir 12-24h entre les couches  
    6. 🔥 Astuce trhacknon : jouer avec une aiguille pour tirer les formes galactiques
    """)

    st.success("🧬 Effet galaxie prêt à fusionner dans votre création !")
