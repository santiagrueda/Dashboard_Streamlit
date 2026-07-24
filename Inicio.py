"""
Dashboard de Monitoreo Ambiental — Página de inicio.
Punto de entrada de la app multipágina de Streamlit.
"""

import plotly.express as px
import streamlit as st

from utils.carga_datos import cargar_datos, resumen_calidad_datos, COLOR_CIUDADES
from utils.estilos import aplicar_tema_global, inyectar_css
from utils.filtros import render_filtros_sidebar

st.set_page_config(
    page_title="Monitoreo Ambiental | Inicio",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_tema_global()
inyectar_css()

# ---------- Carga de datos ----------
df = cargar_datos()
df_f = render_filtros_sidebar(df)
resumen = resumen_calidad_datos(df)

# ---------- Encabezado ----------
st.title("🌎 Dashboard de Monitoreo Ambiental")
st.markdown(
    "Análisis de calidad del aire, ruido, temperatura y humedad captados por una "
    "red de sensores urbanos en cinco ciudades de Colombia."
)
st.divider()

# ---------- Sobre el proyecto ----------
col_texto, col_img = st.columns([2, 1])
with col_texto:
    st.subheader("📌 ¿Qué encontrarás en este dashboard?")
    st.markdown(
        """
- **📊 Análisis Exploratorio (EDA):** estructura del dataset, calidad de los datos,
  distribuciones y relaciones entre variables.
- **📖 Storytelling por variable:** una historia clara y en lenguaje simple sobre
  qué dice cada variable (PM2.5, temperatura, humedad, ruido, lluvia, hora e ICA).
- **📋 Reporte Final:** hallazgos consolidados, semáforo de calidad del aire por
  ciudad y recomendaciones prácticas.

Usa los **filtros de la barra lateral** (ciudad, zona, lluvia, hora) — se aplican
automáticamente en todas las páginas.
        """
    )
with col_img:
    st.markdown("#### 🗺️ Ciudades monitoreadas")
    for c in resumen["ciudades"]:
        st.markdown(f"- {c}")
    st.markdown("#### 🏭 Tipos de zona")
    for z in resumen["zonas"]:
        st.markdown(f"- {z}")

st.divider()

# ---------- KPIs generales ----------
st.subheader("📈 Panorama general (según filtros activos)")

if df_f.empty:
    st.info("Ajusta los filtros de la barra lateral para ver datos.")
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Sensores (registros)", f"{len(df_f):,}")
    c2.metric("PM2.5 promedio", f"{df_f['PM2_5_Ug_m3'].mean():.1f} µg/m³")
    c3.metric("Temperatura promedio", f"{df_f['Temperatura_C'].mean():.1f} °C")
    c4.metric("Humedad promedio", f"{df_f['Humedad_Relativa_Pct'].mean():.0f} %")
    c5.metric("Ruido promedio", f"{df_f['Nivel_Ruido_dB'].mean():.1f} dB")

    st.markdown("##### PM2.5 promedio por ciudad")
    prom_ciudad = (
        df_f.groupby("Ciudad", as_index=False)["PM2_5_Ug_m3"]
        .mean()
        .sort_values("PM2_5_Ug_m3", ascending=False)
    )
    fig = px.bar(
        prom_ciudad, x="Ciudad", y="PM2_5_Ug_m3", color="Ciudad",
        color_discrete_map=COLOR_CIUDADES, text_auto=".1f",
        labels={"PM2_5_Ug_m3": "PM2.5 promedio (µg/m³)"},
    )
    fig.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig, width='stretch')

st.divider()
st.caption(
    "Dataset: monitoreo_ambiental.csv · 500 registros de sensores · "
    "Navega usando el menú de la izquierda ⬅️"
)
