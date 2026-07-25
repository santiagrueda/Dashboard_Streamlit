"""
Estilos y utilidades visuales compartidas: CSS para tema oscuro,
plantilla de Plotly y configuración de Seaborn/Matplotlib.
Se centraliza aquí para que las tres librerías de graficación
(Plotly, Seaborn, Matplotlib) luzcan consistentes entre páginas.
"""

import matplotlib.pyplot as plt
import plotly.io as pio
import seaborn as sns
import streamlit as st

FONDO = "#0e1117"
PANEL = "#1a1f2b"
TEXTO = "#fafafa"
GRID = "#2b3242"
ACENTO = "#4c9be8"


def aplicar_tema_global():
    """Configura Plotly, Seaborn y Matplotlib con una paleta oscura consistente."""
    # --- Plotly ---
    pio.templates["oscuro_custom"] = pio.templates["plotly_dark"]
    pio.templates["oscuro_custom"].layout.paper_bgcolor = FONDO
    pio.templates["oscuro_custom"].layout.plot_bgcolor = FONDO
    pio.templates["oscuro_custom"].layout.font.color = TEXTO
    pio.templates.default = "oscuro_custom"

    # --- Matplotlib / Seaborn ---
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": FONDO,
        "axes.facecolor": FONDO,
        "savefig.facecolor": FONDO,
        "axes.edgecolor": GRID,
        "grid.color": GRID,
        "text.color": TEXTO,
        "axes.labelcolor": TEXTO,
        "xtick.color": TEXTO,
        "ytick.color": TEXTO,
        "font.size": 10,
    })
    sns.set_style("darkgrid", {
        "axes.facecolor": FONDO,
        "figure.facecolor": FONDO,
        "grid.color": GRID,
    })


def inyectar_css():
    """Inyecta CSS adicional para pulir tarjetas de métricas, tabs y contenedores."""
    st.markdown(
        """
        <style>
        .stApp { background-color: #0e1117; }

        div[data-testid="stMetric"] {
            background-color: #1a1f2b;
            border: 1px solid #2b3242;
            border-radius: 10px;
            padding: 14px 16px;
        }
        div[data-testid="stMetricLabel"] { color: #9aa4b2; }

        .bloque-narrativa {
            background-color: #1a1f2b;
            border-left: 4px solid #4c9be8;
            border-radius: 6px;
            padding: 16px 20px;
            margin: 10px 0 18px 0;
            font-size: 0.98rem;
            line-height: 1.55;
        }
        .bloque-narrativa h4 { margin-top: 0; color: #4c9be8; }

        .tarjeta-hallazgo {
            background-color: #1a1f2b;
            border: 1px solid #2b3242;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 12px;
        }

        h1, h2, h3 { color: #fafafa; }
        hr { border-color: #2b3242; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def bloque_narrativo(titulo: str, texto_html: str):
    """Renderiza una caja de storytelling con estilo consistente."""
    st.markdown(
        f"""<div class="bloque-narrativa"><h4>{titulo}</h4>{texto_html}</div>""",
        unsafe_allow_html=True,
    )
