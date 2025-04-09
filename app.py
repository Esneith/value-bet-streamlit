import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson

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

# Emparejar con cuotas simuladas
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

# 🔢 MÉTRICAS RÁPIDAS
st.metric("📈 Total analizados", len(df_resultado))
st.metric("🎯 Apuestas con valor", df_resultado[df_resultado["¿Apostar?"] == "✅ Sí"].shape[0])

# 📊 GRAFICO DE BARRAS - Value Bet
st.subheader("🔍 Gráfico de Value Bets por partido")
fig, ax = plt.subplots()
ax.barh(
    df_resultado["Local"] + " vs " + df_resultado["Visitante"],
    df_resultado["Value Bet Real"],
    color="green"
)
ax.set_xlabel("Value Bet")
ax.set_title("Valor estimado por apuesta")
st.pyplot(fig)

# 📉 GRAFICO DE DISPERSIÓN - Prob. vs Cuota
st.subheader("📌 Relación entre Probabilidad y Cuota")
fig2, ax2 = plt.subplots()
ax2.scatter(df_resultado["Prob. Local"], df_resultado["Cuota Real"], color="blue")
ax2.set_xlabel("Probabilidad Estimada")
ax2.set_ylabel("Cuota Real")
ax2.set_title("Probabilidad vs Cuota (Identificar value bets)")
st.pyplot(fig2)

# 📋 TABLA DE RESULTADOS
st.subheader("📋 Resultados del análisis")
st.dataframe(df_resultado.style.highlight_max(axis=0, subset=["Value Bet Real"], color="lightgreen"))

# 🎯 Apuestas recomendadas
st.subheader("🎯 Apuestas recomendadas")
st.dataframe(df_resultado[df_resultado["¿Apostar?"] == "✅ Sí"])

st.dataframe(df_resultado.style.highlight_max(axis=0, subset=["Value Bet Real"], color="lightgreen"))

# Filtro apuestas recomendadas
st.subheader("🎯 Apuestas recomendadas")
st.dataframe(df_resultado[df_resultado["¿Apostar?"] == "✅ Sí"])
