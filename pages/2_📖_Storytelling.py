"""Página de Storytelling: una historia clara y accesible por cada variable."""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

from utils.carga_datos import cargar_datos, COLOR_CIUDADES, COLOR_ICA, ORDEN_ICA
from utils.estilos import aplicar_tema_global, inyectar_css, bloque_narrativo
from utils.filtros import render_filtros_sidebar

st.set_page_config(page_title="Storytelling | Monitoreo Ambiental", page_icon="📖", layout="wide")
aplicar_tema_global()
inyectar_css()

df = cargar_datos()
df_f = render_filtros_sidebar(df)

st.title("📖 Storytelling: lo que dicen los datos, variable por variable")
st.markdown(
    "Cada sección cuenta una historia breve, en lenguaje simple, sobre una variable "
    "del monitoreo ambiental — pensada para que cualquier persona, sin importar su "
    "formación técnica, entienda qué está pasando."
)

if df_f.empty:
    st.warning("No hay datos con los filtros actuales. Ajusta la barra lateral.")
    st.stop()

st.divider()

# =================================================================
# PM2.5
# =================================================================
st.header("🫁 PM2.5 — el contaminante que más afecta la salud")

ciudad_top_pm25 = df_f.groupby("Ciudad")["PM2_5_Ug_m3"].mean().idxmax()
valor_top_pm25 = df_f.groupby("Ciudad")["PM2_5_Ug_m3"].mean().max()
pct_alto = (df_f["PM2_5_Ug_m3"] > 100).mean() * 100

col1, col2 = st.columns([3, 2])
with col1:
    fig = px.box(
        df_f, x="Ciudad", y="PM2_5_Ug_m3", color="Ciudad",
        color_discrete_map=COLOR_CIUDADES,
        labels={"PM2_5_Ug_m3": "PM2.5 (µg/m³)"},
    )
    fig.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig, width='stretch')
with col2:
    bloque_narrativo(
        "¿Qué nos dice esta variable?",
        f"""
        El <b>PM2.5</b> son partículas tan pequeñas que pueden llegar hasta los pulmones
        y el torrente sanguíneo. En los datos filtrados, <b>{ciudad_top_pm25}</b> registra
        el promedio más alto ({valor_top_pm25:.1f} µg/m³). Además, un
        <b>{pct_alto:.0f}%</b> de las lecturas supera los 100 µg/m³, un nivel considerado
        alto según estándares internacionales de calidad del aire.
        """,
    )

st.divider()

# =================================================================
# Temperatura
# =================================================================
st.header("🌡️ Temperatura — el clima detrás de cada lectura")

temp_prom = df_f["Temperatura_C"].mean()
ciudad_calida = df_f.groupby("Ciudad")["Temperatura_C"].mean().idxmax()
ciudad_fresca = df_f.groupby("Ciudad")["Temperatura_C"].mean().idxmin()

col1, col2 = st.columns([3, 2])
with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.violinplot(
        data=df_f, x="Ciudad", y="Temperatura_C", hue="Ciudad",
        palette=COLOR_CIUDADES, legend=False, ax=ax,
    )
    ax.set_ylabel("Temperatura (°C)")
    ax.set_xlabel("")
    plt.xticks(rotation=15)
    st.pyplot(fig, width='stretch')
with col2:
    bloque_narrativo(
        "¿Qué nos dice esta variable?",
        f"""
        La temperatura promedio registrada es de <b>{temp_prom:.1f} °C</b>.
        <b>{ciudad_calida}</b> aparece como la ciudad con temperaturas más altas
        en promedio, mientras que <b>{ciudad_fresca}</b> presenta las más bajas.
        La forma de "violín" de cada ciudad muestra qué tan dispersas son sus
        lecturas: entre más ancha la figura en un punto, más lecturas hay
        alrededor de esa temperatura.
        """,
    )

st.divider()

# =================================================================
# Humedad y lluvia
# =================================================================
st.header("💧 Humedad y lluvia — ¿van siempre de la mano?")

hum_lluvia = df_f.groupby("Lluvia_Label")["Humedad_Relativa_Pct"].mean()
diff_hum = hum_lluvia.get("Con lluvia", 0) - hum_lluvia.get("Sin lluvia", 0)

col1, col2 = st.columns([3, 2])
with col1:
    fig = px.histogram(
        df_f, x="Humedad_Relativa_Pct", color="Lluvia_Label", barmode="overlay",
        opacity=0.65, nbins=25,
        color_discrete_map={"Con lluvia": "#4c9be8", "Sin lluvia": "#f2b134"},
        labels={"Humedad_Relativa_Pct": "Humedad relativa (%)", "Lluvia_Label": "Condición"},
    )
    fig.update_layout(height=380)
    st.plotly_chart(fig, width='stretch')
with col2:
    if abs(diff_hum) < 3:
        interpretacion = (
            "la diferencia es mínima, lo cual indica que en este dataset la humedad "
            "<b>no depende fuertemente</b> de si llueve o no en el momento de la lectura "
            "(puede deberse a que la humedad ambiental cambia más lento que la lluvia puntual)."
        )
    else:
        interpretacion = (
            f"los días con lluvia muestran en promedio "
            f"{'más' if diff_hum > 0 else 'menos'} humedad, una relación esperable físicamente."
        )
    bloque_narrativo(
        "¿Qué nos dice esta variable?",
        f"""
        Humedad promedio <b>con lluvia:</b> {hum_lluvia.get('Con lluvia', 0):.1f}% ·
        <b>sin lluvia:</b> {hum_lluvia.get('Sin lluvia', 0):.1f}%.
        En términos simples, {interpretacion}
        """,
    )

st.divider()

# =================================================================
# Ruido
# =================================================================
st.header("🔊 Ruido — el impacto silencioso en la calidad de vida")

zona_ruidosa = df_f.groupby("Tipo_Zona")["Nivel_Ruido_dB"].mean().idxmax()
zona_tranquila = df_f.groupby("Tipo_Zona")["Nivel_Ruido_dB"].mean().idxmin()
pct_riesgo = (df_f["Nivel_Ruido_dB"] > 85).mean() * 100

col1, col2 = st.columns([3, 2])
with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=df_f.groupby("Tipo_Zona", as_index=False)["Nivel_Ruido_dB"].mean(),
        x="Tipo_Zona", y="Nivel_Ruido_dB", hue="Tipo_Zona",
        palette="flare", legend=False, ax=ax,
    )
    ax.axhline(85, color="#e74c3c", linestyle="--", linewidth=1.2)
    ax.text(0, 86.5, "Umbral de riesgo auditivo (85 dB)", color="#e74c3c", fontsize=8)
    ax.set_ylabel("Ruido promedio (dB)")
    ax.set_xlabel("")
    plt.xticks(rotation=15)
    st.pyplot(fig, width='stretch')
with col2:
    bloque_narrativo(
        "¿Qué nos dice esta variable?",
        f"""
        <b>{zona_ruidosa}</b> es, en promedio, el tipo de zona más ruidosa, mientras
        que <b>{zona_tranquila}</b> es la más tranquila. La Organización Mundial de la
        Salud señala que la exposición prolongada por encima de 85 dB puede afectar
        la audición; en este conjunto de datos, un <b>{pct_riesgo:.0f}%</b> de las
        lecturas supera ese umbral.
        """,
    )

st.divider()

# =================================================================
# Hora del día
# =================================================================
st.header("🕒 Hora del día — ¿cuándo se respira peor?")

pm25_hora = df_f.groupby("Franja_Horaria")["PM2_5_Ug_m3"].mean().reindex(
    ["Madrugada (22:00–4:59)", "Mañana (5:00–11:59)", "Tarde (12:00–17:59)", "Noche (18:00–21:59)"]
)
franja_peor = pm25_hora.idxmax()

col1, col2 = st.columns([3, 2])
with col1:
    fig = px.line(
        x=pm25_hora.index, y=pm25_hora.values, markers=True,
        labels={"x": "Franja horaria", "y": "PM2.5 promedio (µg/m³)"},
    )
    fig.update_traces(line_color="#4c9be8", marker_size=10)
    fig.update_layout(height=380)
    st.plotly_chart(fig, width='stretch')
with col2:
    bloque_narrativo(
        "¿Qué nos dice esta variable?",
        f"""
        Agrupando las lecturas por franja horaria, la peor calidad de aire promedio
        (PM2.5 más alto) se observa en la franja de <b>{franja_peor}</b>. Aun así, las
        diferencias entre franjas en este dataset son moderadas — no hay un patrón
        horario extremo, lo que sugiere que el monitoreo debe mantenerse activo
        durante todo el día y no solo en "horas pico" tradicionales.
        """,
    )

st.divider()

# =================================================================
# ICA (transparencia sobre el hallazgo de independencia)
# =================================================================
st.header("🚦 Índice de Calidad del Aire (ICA) — la etiqueta oficial")

conteo_ica = df_f["Indice_Calidad_Aire_ICA"].value_counts().reindex(ORDEN_ICA).fillna(0)

col1, col2 = st.columns([3, 2])
with col1:
    fig = px.bar(
        x=conteo_ica.index, y=conteo_ica.values,
        color=conteo_ica.index, color_discrete_map=COLOR_ICA,
        labels={"x": "Categoría ICA", "y": "Nº de registros"},
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, width='stretch')
with col2:
    bloque_narrativo(
        "¿Qué nos dice esta variable?",
        """
        El ICA clasifica cada lectura en una categoría de severidad, de "Buena" a
        "Peligrosa". Es importante ser transparentes: al comparar esta etiqueta con
        el valor numérico de PM2.5 (ver sección de EDA), <b>no encontramos una
        relación proporcional clara</b> entre ambas en este dataset — lecturas con
        PM2.5 similar aparecen en categorías ICA distintas. Por eso, para decisiones
        críticas recomendamos apoyarse en el <b>valor numérico de PM2.5</b> además
        de la etiqueta ICA.
        """,
    )

st.divider()
st.caption(
    "Storytelling elaborado con datos reales y calculados dinámicamente según los "
    "filtros activos — ningún número de esta página está escrito a mano."
)
