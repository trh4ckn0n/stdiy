import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Pyramide Résine DIY - trhacknon",
    layout="wide",
    page_icon="🛠"
)

# Style hacker personnalisé injecté
st.markdown("""
    <style>
        body {
            background-color: #0d1117;
            color: #39ff14;
        }
        .css-18e3th9 {
            background-color: #0d1117;
        }
        .css-1d391kg {
            background-color: #0d1117;
        }
        h1 {
            color: #39ff14;
            text-shadow: 0 0 5px #39ff14;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { text-shadow: 0 0 5px #39ff14; }
            50% { text-shadow: 0 0 15px #00ffe0; }
            100% { text-shadow: 0 0 5px #39ff14; }
        }
        .stDataFrame {
            border: 1px solid #00ffe0;
            border-radius: 8px;
        }
        .stApp {
            background-color: #0d1117;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌪️ WebApp Hacker DIY - Calcul Pyramide Résine")

# Entrée des dimensions
base = st.number_input("📐 Base de la pyramide (cm)", value=15.0)

hauteurs = []
cols = st.columns(5)
default_hauteurs = [3.0, 2.0, 4.0, 3.0, 3.0]
for i in range(5):
    with cols[i]:
        h = st.number_input(f"Hauteur couche {i+1} (cm)", min_value=0.0, value=default_hauteurs[i])
        hauteurs.append(h)

# Fonctions
def pyramide_volume(b, h):
    return (1/3) * (b ** 2) * h

def base_at_height(total_h, current_h, base):
    return (base * current_h) / total_h

# Calculs
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

# Affichage tableau
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

# Graphique
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
