# 🌎 Dashboard de Monitoreo Ambiental

Dashboard interactivo en **Streamlit** para el análisis de calidad del aire, ruido,
temperatura y humedad captados por una red de sensores urbanos en cinco ciudades
de Colombia (Bogotá, Medellín, Cali, Barranquilla, Bucaramanga).

## 🗂️ Estructura del proyecto

```
monitoreo-ambiental-dashboard/
├── Inicio.py                              # Página principal (KPIs generales)
├── pages/
│   ├── 1_📊_Analisis_Exploratorio.py      # EDA completo
│   ├── 2_📖_Storytelling.py               # Historia narrativa por variable
│   └── 3_📋_Reporte_Final.py              # Hallazgos, semáforo y recomendaciones
├── utils/
│   ├── carga_datos.py                     # Carga y limpieza de datos (cacheada)
│   ├── estilos.py                         # Tema oscuro para Plotly/Seaborn/Matplotlib
│   └── filtros.py                         # Filtros de barra lateral compartidos
├── data/
│   └── monitoreo_ambiental.csv            # Dataset (500 registros)
├── .streamlit/
│   └── config.toml                        # Tema oscuro nativo de Streamlit
├── requirements.txt
└── README.md
```

## ✅ Qué incluye

- **EDA completo**: estructura del dataset, calidad de datos (nulos/duplicados),
  estadísticas descriptivas, distribuciones, boxplots, matriz de correlación y
  análisis categórico.
- **Storytelling por variable**: una narrativa en lenguaje simple y accesible para
  PM2.5, temperatura, humedad/lluvia, ruido, hora del día e ICA, con conclusiones
  calculadas dinámicamente (no texto fijo).
- **Reporte final**: semáforo de calidad del aire por ciudad, resumen ejecutivo y
  recomendaciones, con botón de descarga en `.txt`.
- **Gráficas con Plotly (interactivas), Seaborn y Matplotlib/pyplot**, todas con
  un tema oscuro consistente.
- **Filtros globales** (ciudad, zona, lluvia, rango de hora) que persisten al
  navegar entre páginas.

## 🖥️ Cómo ejecutarlo en tu computador (opcional, antes de subirlo)

```bash
# 1. Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run Inicio.py
```

Se abrirá en `http://localhost:8501`.

---

## 🚀 Guía paso a paso: subir a GitHub y desplegar en Streamlit Community Cloud

### Paso 1 — Crear el repositorio en GitHub

1. Entra a [github.com](https://github.com) → botón **New repository**.
2. Nombre sugerido: `monitoreo-ambiental-dashboard`.
3. Visibilidad: **Public** (Streamlit Community Cloud gratuito requiere repos
   públicos, salvo que tengas plan con repos privados habilitados).
4. **No** marques "Add a README" (ya tienes uno) — crea el repo vacío.

### Paso 2 — Subir el proyecto desde tu computador

Descomprime el `.zip` que te entrego, entra a la carpeta del proyecto en tu
terminal y ejecuta:

```bash
cd monitoreo-ambiental-dashboard

git init
git add .
git commit -m "Dashboard de monitoreo ambiental - versión inicial"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/monitoreo-ambiental-dashboard.git
git push -u origin main
```

> Reemplaza `TU_USUARIO` por tu usuario real de GitHub. Si te pide autenticación,
> usa un **Personal Access Token** (GitHub ya no acepta contraseña normal por
> HTTPS): Settings → Developer settings → Personal access tokens.

### Paso 3 — Desplegar en Streamlit Community Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con tu
   cuenta de GitHub.
2. Clic en **New app**.
3. Selecciona:
   - **Repository:** `TU_USUARIO/monitoreo-ambiental-dashboard`
   - **Branch:** `main`
   - **Main file path:** `Inicio.py`
4. Clic en **Deploy**. El primer despliegue tarda 1-3 minutos mientras instala
   `requirements.txt`.
5. Tu dashboard quedará disponible en una URL pública tipo:
   `https://TU_USUARIO-monitoreo-ambiental-dashboard.streamlit.app`

### Paso 4 — Actualizaciones futuras

Cada vez que quieras actualizar el dashboard, solo necesitas hacer push a
`main`; Streamlit Community Cloud vuelve a desplegar automáticamente:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

### 🛠️ Solución de problemas comunes

| Problema | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError` al desplegar | Falta una librería en `requirements.txt` | Agrégala y vuelve a hacer push |
| El tema no se ve oscuro | El archivo `.streamlit/config.toml` no se subió | Verifica que la carpeta `.streamlit/` esté en el repo (a veces los `.` se ocultan; usa `git add -A`) |
| "File does not exist: data/monitoreo_ambiental.csv" | La carpeta `data/` no se subió o el CSV no se incluyó en el commit | Verifica con `git status` antes de subir |
| La app se "duerme" tras inactividad | Comportamiento normal del plan gratuito | Solo debes volver a abrir la URL; despierta automáticamente |

---

## 🔎 Nota metodológica sobre el dataset

El EDA identificó que este dataset **no presenta valores nulos ni duplicados**, y
que las variables numéricas (PM2.5, temperatura, humedad, ruido) **no muestran
correlaciones fuertes entre sí**, ni la categoría ICA se relaciona de forma
proporcional con el valor numérico de PM2.5. Esto se documenta de forma
transparente en el dashboard (secciones de EDA y Storytelling) en lugar de forzar
una narrativa de causalidad que los datos no respaldan.
