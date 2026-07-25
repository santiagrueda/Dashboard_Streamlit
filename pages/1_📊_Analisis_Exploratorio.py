"""Página de Análisis Exploratorio de Datos (EDA)."""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

from utils.carga_datos import cargar_datos, resumen_calidad_datos, COLOR_CIUDADES
from utils.estilos import aplicar_tema_global, inyectar_css
from utils.filtros import render_filtros_sidebar

st.set_page_config(page_title="EDA | Monitoreo Ambiental", page_icon="📊", layout="wide")
aplicar_tema_global()
inyectar_css()

df = cargar_datos()
df_f = render_filtros_sidebar(df)

st.title("📊 Análisis Exploratorio de Datos (EDA)")
st.markdown(
    "Antes de contar la historia de los datos, verificamos su estructura, "
    "calidad y comportamiento estadístico."
)

if df_f.empty:
    st.warning("No hay datos con los filtros actuales. Ajusta la barra lateral.")
    st.stop()

# ---------------------------------------------------------------
# 1. Vista general y calidad de datos
# ---------------------------------------------------------------
st.header("1️⃣ Vista general y calidad del dataset")
resumen = resumen_calidad_datos(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Filas totales", resumen["filas"])
c2.metric("Columnas", resumen["columnas"])
c3.metric("Valores nulos", resumen["nulos_totales"])
c4.metric("Filas duplicadas", resumen["duplicados"])

st.markdown(
    """
<div class="tarjeta-hallazgo">
✅ <b>El dataset no presenta valores nulos ni filas duplicadas</b>, y cada sensor
(<code>ID_Sensor</code>) es único. Esto significa que no fue necesario aplicar
imputación ni limpieza de duplicados antes del análisis.
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("Ver tipos de datos por columna"):
    tipos = df.dtypes.astype(str).rename("Tipo de dato")
    st.dataframe(tipos, width='stretch')

# ---------------------------------------------------------------
# 2. Estadísticas descriptivas
# ---------------------------------------------------------------
st.header("2️⃣ Estadísticas descriptivas")
st.dataframe(
    df_f[["PM2_5_Ug_m3", "Temperatura_C", "Humedad_Relativa_Pct", "Nivel_Ruido_dB"]]
    .describe()
    .T.style.format("{:.2f}"),
    width='stretch',
)

# ---------------------------------------------------------------
# 3. Distribuciones numéricas (Plotly)
# ---------------------------------------------------------------
st.header("3️⃣ Distribuciones de variables numéricas")
st.caption("Histogramas interactivos (Plotly) — pasa el cursor para ver el detalle.")

variables_num = {
    "PM2_5_Ug_m3": "Material particulado PM2.5 (µg/m³)",
    "Temperatura_C": "Temperatura (°C)",
    "Humedad_Relativa_Pct": "Humedad relativa (%)",
    "Nivel_Ruido_dB": "Nivel de ruido (dB)",
}

tabs = st.tabs(list(variables_num.values()))
for tab, (col, etiqueta) in zip(tabs, variables_num.items()):
    with tab:
        fig = px.histogram(
            df_f, x=col, nbins=30, marginal="box",
            color_discrete_sequence=["#4c9be8"],
            labels={col: etiqueta},
        )
        fig.update_layout(height=420, bargap=0.03)
        st.plotly_chart(fig, width='stretch')

# ---------------------------------------------------------------
# 4. Comparaciones por ciudad / zona (Seaborn)
# ---------------------------------------------------------------
st.header("4️⃣ Comparaciones por ciudad y tipo de zona")
st.caption("Boxplots (Seaborn) — la caja muestra la mediana y el rango intercuartílico; los puntos son valores atípicos.")

col_a, col_b = st.columns(2)

with col_a:
    fig, ax = plt.subplots(figsize=(6, 4.2))
    sns.boxplot(
        data=df_f, x="Ciudad", y="PM2_5_Ug_m3", hue="Ciudad",
        palette=COLOR_CIUDADES, legend=False, ax=ax,
    )
    ax.set_title("PM2.5 por ciudad")
    ax.set_xlabel("")
    ax.set_ylabel("PM2.5 (µg/m³)")
    plt.xticks(rotation=20)
    st.pyplot(fig, width='stretch')

with col_b:
    fig2, ax2 = plt.subplots(figsize=(6, 4.2))
    sns.boxplot(
        data=df_f, x="Tipo_Zona", y="Nivel_Ruido_dB", hue="Tipo_Zona",
        palette="crest", legend=False, ax=ax2,
    )
    ax2.set_title("Nivel de ruido por tipo de zona")
    ax2.set_xlabel("")
    ax2.set_ylabel("Ruido (dB)")
    plt.xticks(rotation=20)
    st.pyplot(fig2, width='stretch')

# ---------------------------------------------------------------
# 5. Matriz de correlación (Seaborn heatmap)
# ---------------------------------------------------------------
st.header("5️⃣ Matriz de correlación entre variables numéricas")
corr = df_f[["PM2_5_Ug_m3", "Temperatura_C", "Humedad_Relativa_Pct", "Nivel_Ruido_dB"]].corr()

fig3, ax3 = plt.subplots(figsize=(5.5, 4.2))
sns.heatmap(
    corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
    linewidths=0.5, linecolor="#0e1117", ax=ax3, cbar_kws={"shrink": 0.8},
)
ax3.set_title("Correlación de Pearson")
st.pyplot(fig3, width='content')

corr_max = corr.where(~corr.isna()).abs().where(~(corr.abs() == 1)).max().max()
st.markdown(
    f"""
<div class="tarjeta-hallazgo">
🔎 <b>Hallazgo clave:</b> ninguna pareja de variables numéricas muestra una
correlación relevante (la más alta en valor absoluto es de apenas
<b>{corr_max:.2f}</b>). Esto sugiere que, dentro de este dataset, PM2.5,
temperatura, humedad y ruido se comportan de forma <b>prácticamente
independiente</b> entre sí — ninguna predice a la otra de forma directa.
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# 6. Variables categóricas (Matplotlib puro + Plotly)
# ---------------------------------------------------------------
st.header("6️⃣ Distribución de variables categóricas")

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("**Distribución del Índice de Calidad del Aire (ICA)**")
    conteo_ica = df_f["Indice_Calidad_Aire_ICA"].value_counts().reindex(
        df_f["Indice_Calidad_Aire_ICA"].cat.categories
    ).fillna(0)
    fig4, ax4 = plt.subplots(figsize=(5.5, 5.5))
    colores = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c", "#9b59b6", "#7f1d1d"]
    ax4.pie(
        conteo_ica.values, labels=conteo_ica.index, autopct="%1.0f%%",
        colors=colores, textprops={"color": "#fafafa", "fontsize": 8},
        wedgeprops={"edgecolor": "#0e1117", "linewidth": 1},
    )
    ax4.set_title("Categorías ICA (Matplotlib)")
    st.pyplot(fig4, width='stretch')

with col_d:
    st.markdown("**Registros por ciudad y presencia de lluvia**")
    fig5 = px.histogram(
        df_f, x="Ciudad", color="Lluvia_Label", barmode="group",
        color_discrete_map={"Con lluvia": "#4c9be8", "Sin lluvia": "#f2b134"},
        labels={"Lluvia_Label": "Condición"},
    )
    fig5.update_layout(height=460, xaxis_title="", yaxis_title="Nº de registros")
    st.plotly_chart(fig5, width='stretch')

st.divider()
st.caption(
    "Herramientas usadas en esta página → Plotly (histogramas interactivos y barras), "
    "Seaborn (boxplots y heatmap) y Matplotlib/pyplot (gráfico de pastel)."
)
