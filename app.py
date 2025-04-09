
import streamlit as st
import pandas as pd
from scipy.stats import poisson
from datetime import date

st.set_page_config(page_title="Value Bet Fútbol", layout="wide")
st.title("⚽ Sistema de Value Bets - Modelo Poisson")

# Cuotas simuladas
df_cuotas_mock = pd.DataFrame([
    {"Fecha": "2025-04-09", "Equipo 1": "Barcelona", "Equipo 2": "Real Madrid", "Cuota Real 1": 2.3},
    {"Fecha": "2025-04-09", "Equipo 1": "River Plate", "Equipo 2": "Boca Juniors", "Cuota Real 1": 2.0},
    {"Fecha": "2025-04-09", "Equipo 1": "Manchester City", "Equipo 2": "Arsenal", "Cuota Real 1": 1.9},
    {"Fecha": "2025-04-09", "Equipo 1": "América de Cali", "Equipo 2": "Millonarios", "Cuota Real 1": 2.1},
    {"Fecha": "2025-04-09", "Equipo 1": "Flamengo", "Equipo 2": "Palmeiras", "Cuota Real 1": 2.2}
])

# Simulación de partidos analizados
df_poisson = pd.DataFrame([
    {"Fecha": "2025-04-09", "Local": "Barcelona", "Visitante": "Real Madrid", "Prob. Local": 0.58},
    {"Fecha": "2025-04-09", "Local": "River Plate", "Visitante": "Boca Juniors", "Prob. Local": 0.62},
    {"Fecha": "2025-04-09", "Local": "Manchester City", "Visitante": "Arsenal", "Prob. Local": 0.55},
    {"Fecha": "2025-04-09", "Local": "América de Cali", "Visitante": "Millonarios", "Prob. Local": 0.51},
    {"Fecha": "2025-04-09", "Local": "Flamengo", "Visitante": "Palmeiras", "Prob. Local": 0.57}
])

# Emparejamos y calculamos value bet real
def emparejar_con_cuotas(df_partidos, df_cuotas):
    df = df_partidos.copy()
    df["Cuota Real"] = 2.1
    for i, row in df.iterrows():
        for _, cuota in df_cuotas.iterrows():
            if (
                row["Local"].lower() in cuota["Equipo 1"].lower()
                and row["Visitante"].lower() in cuota["Equipo 2"].lower()
                and row["Fecha"] == cuota["Fecha"]
            ):
                df.at[i, "Cuota Real"] = cuota["Cuota Real 1"]
    df["Value Bet Real"] = (df["Prob. Local"] * df["Cuota Real"]) - 1
    df["¿Apostar?"] = df["Value Bet Real"].apply(lambda x: "✅ Sí" if x > 0 else "❌ No")
    return df

df_resultado = emparejar_con_cuotas(df_poisson, df_cuotas_mock)

# Mostrar tabla
st.subheader("📋 Resultados del análisis")
st.dataframe(df_resultado.style.highlight_max(axis=0, subset=["Value Bet Real"], color="lightgreen"))

# Filtro apuestas recomendadas
st.subheader("🎯 Apuestas recomendadas")
st.dataframe(df_resultado[df_resultado["¿Apostar?"] == "✅ Sí"])
