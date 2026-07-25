"""Página de Reporte Final: hallazgos consolidados y recomendaciones."""

from datetime import datetime

import plotly.express as px
import streamlit as st

from utils.carga_datos import cargar_datos, COLOR_ICA, ORDEN_ICA
from utils.estilos import aplicar_tema_global, inyectar_css, bloque_narrativo
from utils.filtros import render_filtros_sidebar

st.set_page_config(page_title="Reporte Final | Monitoreo Ambiental", page_icon="📋", layout="wide")
aplicar_tema_global()
inyectar_css()

df = cargar_datos()
df_f = render_filtros_sidebar(df)

st.title("📋 Reporte Final de Monitoreo Ambiental")
st.caption(f"Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')} · basado en los filtros activos")

if df_f.empty:
    st.warning("No hay datos con los filtros actuales. Ajusta la barra lateral.")
    st.stop()

# ---------------------------------------------------------------
# Semáforo de calidad del aire por ciudad
# ---------------------------------------------------------------
st.header("🚦 Semáforo de calidad del aire por ciudad")

resumen_ciudad = (
    df_f.groupby("Ciudad")
    .agg(
        PM25_prom=("PM2_5_Ug_m3", "mean"),
        Ruido_prom=("Nivel_Ruido_dB", "mean"),
        Registros=("ID_Sensor", "count"),
    )
    .reset_index()
    .sort_values("PM25_prom", ascending=False)
)


def semaforo(pm25):
    if pm25 < 50:
        return "🟢 Buena"
    elif pm25 < 80:
        return "🟡 Moderada"
    elif pm25 < 110:
        return "🟠 Dañina para sensibles"
    else:
        return "🔴 Alta / Peligrosa"


resumen_ciudad["Estado"] = resumen_ciudad["PM25_prom"].apply(semaforo)

cols = st.columns(len(resumen_ciudad))
for col, (_, fila) in zip(cols, resumen_ciudad.iterrows()):
    with col:
        st.markdown(
            f"""
            <div class="tarjeta-hallazgo" style="text-align:center;">
                <h4 style="margin-bottom:4px;">{fila['Ciudad']}</h4>
                <p style="font-size:1.6rem; margin:4px 0;">{fila['Estado'].split()[0]}</p>
                <p style="margin:0; color:#9aa4b2;">{fila['Estado'].split(' ', 1)[1]}</p>
                <hr style="margin:8px 0;">
                <p style="margin:2px 0;"><b>{fila['PM25_prom']:.1f}</b> µg/m³ PM2.5</p>
                <p style="margin:2px 0; color:#9aa4b2;">{fila['Ruido_prom']:.1f} dB ruido</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption(
    "Semáforo basado en el promedio de PM2.5 por ciudad "
    "(🟢 <50 · 🟡 50–80 · 🟠 80–110 · 🔴 >110 µg/m³). Umbrales de referencia, no normativos."
)

st.divider()

# ---------------------------------------------------------------
# Resumen ejecutivo narrativo
# ---------------------------------------------------------------
st.header("📝 Resumen ejecutivo")

ciudad_critica = resumen_ciudad.iloc[0]["Ciudad"]
ciudad_mejor = resumen_ciudad.iloc[-1]["Ciudad"]
zona_ruidosa = df_f.groupby("Tipo_Zona")["Nivel_Ruido_dB"].mean().idxmax()
pct_peligrosa = (df_f["Indice_Calidad_Aire_ICA"].isin(["Muy Dañina", "Peligrosa"])).mean() * 100
n_registros = len(df_f)

bloque_narrativo(
    "Hallazgos principales",
    f"""
    Sobre los <b>{n_registros}</b> registros analizados: <b>{ciudad_critica}</b> presenta
    el promedio de PM2.5 más alto y requiere atención prioritaria, mientras que
    <b>{ciudad_mejor}</b> muestra los mejores niveles. Las zonas de tipo
    <b>{zona_ruidosa}</b> concentran los niveles de ruido más altos. Un
    <b>{pct_peligrosa:.0f}%</b> de las lecturas cae en categorías ICA severas
    ("Muy Dañina" o "Peligrosa"). El análisis de correlación no encontró relaciones
    fuertes entre PM2.5, temperatura, humedad y ruido — cada variable se comporta
    de forma prácticamente independiente, por lo que ninguna puede usarse como
    predictor confiable de las demás dentro de este dataset.
    """,
)

st.divider()

# ---------------------------------------------------------------
# Composición ICA general + recomendaciones
# ---------------------------------------------------------------
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Composición general del ICA")
    conteo_ica = df_f["Indice_Calidad_Aire_ICA"].value_counts().reindex(ORDEN_ICA).fillna(0)
    fig = px.pie(
        names=conteo_ica.index, values=conteo_ica.values,
        color=conteo_ica.index, color_discrete_map=COLOR_ICA, hole=0.45,
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader("✅ Recomendaciones")
    st.markdown(
        f"""
        1. **Priorizar monitoreo en {ciudad_critica}**, donde el PM2.5 promedio es
           más alto — evaluar fuentes de emisión cercanas a los sensores.
        2. **Reforzar control de ruido en zonas de tipo {zona_ruidosa}**, dado que
           superan con frecuencia el umbral de 85 dB.
        3. **No usar el ICA como único indicador**: complementarlo siempre con el
           valor numérico de PM2.5, dada la baja correlación observada entre ambos.
        4. **Mantener el monitoreo activo en todas las franjas horarias**, ya que
           no se identificó una única "hora crítica" concentrada.
        5. **Ampliar la recolección de datos** (más sensores o periodo temporal más
           largo) para poder detectar tendencias estacionales u horarias con mayor
           certeza estadística.
        """
    )

st.divider()

# ---------------------------------------------------------------
# Descarga del resumen
# ---------------------------------------------------------------
resumen_txt = f"""REPORTE DE MONITOREO AMBIENTAL
Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Registros analizados: {n_registros}

CIUDAD CON PM2.5 MAS ALTO: {ciudad_critica} ({resumen_ciudad.iloc[0]['PM25_prom']:.1f} ug/m3)
CIUDAD CON PM2.5 MAS BAJO: {ciudad_mejor} ({resumen_ciudad.iloc[-1]['PM25_prom']:.1f} ug/m3)
ZONA MAS RUIDOSA: {zona_ruidosa}
% LECTURAS EN CATEGORIA ICA SEVERA (Muy Dañina/Peligrosa): {pct_peligrosa:.1f}%

HALLAZGO CLAVE: No se hallaron correlaciones fuertes entre PM2.5, temperatura,
humedad y ruido. El ICA categorico no muestra relacion proporcional clara con
el valor numerico de PM2.5.

RECOMENDACIONES:
1. Priorizar monitoreo en {ciudad_critica}.
2. Reforzar control de ruido en zonas tipo {zona_ruidosa}.
3. Complementar el ICA con el valor numerico de PM2.5.
4. Mantener monitoreo activo en todas las franjas horarias.
5. Ampliar la recoleccion de datos para analisis de tendencias.
"""

st.download_button(
    "⬇️ Descargar resumen ejecutivo (.txt)",
    data=resumen_txt,
    file_name="reporte_monitoreo_ambiental.txt",
    mime="text/plain",
)
