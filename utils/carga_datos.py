"""
Módulo de carga y preparación de datos para el Dashboard de Monitoreo Ambiental.
Centraliza la lectura del CSV y las transformaciones para que todas las
páginas del dashboard trabajen sobre el mismo dataset consistente.
"""

import pandas as pd
import streamlit as st

RUTA_DATOS = "data/monitoreo_ambiental.csv"

# Orden lógico del Índice de Calidad del Aire (de mejor a peor),
# usado para que gráficas y tablas respeten la severidad real y no el orden alfabético.
ORDEN_ICA = [
    "Buena",
    "Moderada",
    "Dañina para grupos sensibles",
    "Dañina",
    "Muy Dañina",
    "Peligrosa",
]

# Paleta de color asociada a cada categoría ICA (estilo semáforo de calidad del aire)
COLOR_ICA = {
    "Buena": "#2ecc71",
    "Moderada": "#f1c40f",
    "Dañina para grupos sensibles": "#e67e22",
    "Dañina": "#e74c3c",
    "Muy Dañina": "#9b59b6",
    "Peligrosa": "#7f1d1d",
}

# Paleta de color para ciudades (consistente en todo el dashboard)
COLOR_CIUDADES = {
    "Bogotá": "#4c9be8",
    "Medellín": "#5ad1a3",
    "Cali": "#f2b134",
    "Barranquilla": "#e8615c",
    "Bucaramanga": "#b088f0",
}


@st.cache_data
def cargar_datos(ruta: str = RUTA_DATOS) -> pd.DataFrame:
    """
    Carga el dataset de monitoreo ambiental y aplica transformaciones ligeras:
    - Conversión de Hora_Lectura a tipo datetime.time y a franja horaria.
    - Conversión de Indice_Calidad_Aire_ICA a categórica ordenada.
    - Traducción de Presencia_Lluvia a etiquetas legibles.
    """
    df = pd.read_csv(ruta)

    # Hora de lectura -> objeto datetime auxiliar y hora entera (para agrupar por franja)
    df["Hora_dt"] = pd.to_datetime(df["Hora_Lectura"], format="%H:%M", errors="coerce")
    df["Hora_Entera"] = df["Hora_dt"].dt.hour

    # Franja horaria en lenguaje natural
    def franja(h):
        if pd.isna(h):
            return "Desconocida"
        if 5 <= h < 12:
            return "Mañana (5:00–11:59)"
        elif 12 <= h < 18:
            return "Tarde (12:00–17:59)"
        elif 18 <= h < 22:
            return "Noche (18:00–21:59)"
        else:
            return "Madrugada (22:00–4:59)"

    df["Franja_Horaria"] = df["Hora_Entera"].apply(franja)

    # ICA como categórica ordenada por severidad real
    df["Indice_Calidad_Aire_ICA"] = pd.Categorical(
        df["Indice_Calidad_Aire_ICA"], categories=ORDEN_ICA, ordered=True
    )

    # Etiqueta legible para lluvia
    df["Lluvia_Label"] = df["Presencia_Lluvia"].map({True: "Con lluvia", False: "Sin lluvia"})

    return df


def resumen_calidad_datos(df: pd.DataFrame) -> dict:
    """Genera un resumen rápido de calidad de datos para la sección de EDA."""
    return {
        "filas": df.shape[0],
        "columnas": df.shape[1],
        "nulos_totales": int(df.isnull().sum().sum()),
        "duplicados": int(df.duplicated().sum()),
        "sensores_unicos": int(df["ID_Sensor"].nunique()),
        "ciudades": sorted(df["Ciudad"].unique().tolist()),
        "zonas": sorted(df["Tipo_Zona"].unique().tolist()),
    }
