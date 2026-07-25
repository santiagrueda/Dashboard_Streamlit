"""Filtros de barra lateral reutilizables en todas las páginas."""

import pandas as pd
import streamlit as st


def render_filtros_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dibuja los filtros en la barra lateral (ciudad, zona, lluvia, hora)
    y devuelve el DataFrame filtrado. Usa claves fijas en session_state
    para que la selección se mantenga al cambiar de página.
    """
    st.sidebar.header("🔎 Filtros")

    ciudades = sorted(df["Ciudad"].unique().tolist())
    zonas = sorted(df["Tipo_Zona"].unique().tolist())

    ciudades_sel = st.sidebar.multiselect(
        "Ciudad", ciudades, default=ciudades, key="filtro_ciudad"
    )
    zonas_sel = st.sidebar.multiselect(
        "Tipo de zona", zonas, default=zonas, key="filtro_zona"
    )
    lluvia_sel = st.sidebar.radio(
        "Condición de lluvia", ["Todas", "Con lluvia", "Sin lluvia"],
        index=0, key="filtro_lluvia", horizontal=True,
    )
    rango_horas = st.sidebar.slider(
        "Rango de hora del día", 0, 23, (0, 23), key="filtro_horas",
        help="Filtra las lecturas según la hora en que fueron tomadas (0 a 23h)."
    )

    st.sidebar.caption(f"Registros disponibles: {len(df)}")

    df_filtrado = df[
        df["Ciudad"].isin(ciudades_sel) & df["Tipo_Zona"].isin(zonas_sel)
    ]
    if lluvia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Lluvia_Label"] == lluvia_sel]

    df_filtrado = df_filtrado[
        (df_filtrado["Hora_Entera"] >= rango_horas[0])
        & (df_filtrado["Hora_Entera"] <= rango_horas[1])
    ]

    st.sidebar.markdown(f"**Registros tras filtrar:** {len(df_filtrado)} / {len(df)}")

    if df_filtrado.empty:
        st.sidebar.warning("⚠️ Ningún registro cumple los filtros seleccionados.")

    return df_filtrado
