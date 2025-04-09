mport streamlit as st
import pandas as pd
import requests
from scipy.stats import poisson
from datetime import date

# Configuración de la app
st.set_page_config(page_title="Value Bets Reales - API-Football", layout="wide")
st.title("📊 Sistema Value Bets con Partidos Reales (Poisson + API-Football)")

# API Key
api_key = "c6e72749d66c97b26c4a7e880e8b98ee"
headers = {"x-apisports-key": api_key}

# Obtener partidos del día
def obtener_partidos_hoy():
    hoy = date.today().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoy}"
    res = requests.get(url, headers=headers)
    return res.json().get("response", [])

# Promedio de goles en últimos 5 partidos
def goles_promedio(team_id, tipo="home"):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    res = requests.get(url, headers=headers)
    data = res.json()
    goles = []
    for match in data.get("response", []):
        if tipo == "home" and match["teams"]["home"]["id"] == team_id:
            goles.append(match["goals"]["home"])
        elif tipo == "away" and match["teams"]["away"]["id"] == team_id:
            goles.append(match["goals"]["away"])
    return sum(goles)/len(goles) if goles else 1.0

# Modelo Poisson
def calcular_poisson_prob(home_avg_goals, away_avg_goals, max_goals=5):
    home_win_prob = 0
    draw_prob = 0
    away_win_prob = 0
    for home_goals in range(0, max_goals + 1):
        for away_goals in range(0, max_goals + 1):
            p = poisson.pmf(home_goals, home_avg_goals) * poisson.pmf(away_goals, away_avg_goals)
            if home_goals > away_goals:
                home_win_prob += p
            elif home_goals == away_goals:
                draw_prob += p
            else:
                away_win_prob += p
    return round(home_win_prob, 3), round(draw_prob, 3), round(away_win_prob, 3)

# Análisis completo
def analizar_partidos():
    partidos = obtener_partidos_hoy()
    lista = []
    for match in partidos:
        fecha = match["fixture"]["date"][:10]
        equipo_local = match["teams"]["home"]["name"]
        equipo_visitante = match["teams"]["away"]["name"]
        id_local = match["teams"]["home"]["id"]
        id_visitante = match["teams"]["away"]["id"]

        # Calcular promedios
        avg_local = goles_promedio(id_local, "home")
        avg_visit = goles_promedio(id_visitante, "away")

        # Probabilidades
        prob_local, prob_empate, prob_visit = calcular_poisson_prob(avg_local, avg_visit)

        cuota_simulada = 2.1
        value = (prob_local * cuota_simulada) - 1
        apostar = "✅ Sí" if value > 0 else "❌ No"

        lista.append({
            "Fecha": fecha,
            "Local": equipo_local,
            "Visitante": equipo_visitante,
            "Goles Prom Local": round(avg_local, 2),
            "Goles Prom Visitante": round(avg_visit, 2),
            "Prob. Local": prob_local,
            "Prob. Empate": prob_empate,
            "Prob. Visitante": prob_visit,
            "Cuota Local": cuota_simulada,
            "Value Bet": round(value, 2),
            "¿Apostar?": apostar
        })
    return pd.DataFrame(lista)

# Ejecutar análisis
st.info("Obteniendo partidos reales del día desde API-Football...")
df = analizar_partidos()

# Mostrar resultados
st.subheader("📋 Resultados del Análisis Real")
st.dataframe(df)

# Mostrar solo apuestas recomendadas
st.subheader("🎯 Apuestas Recomendadas (Value Bet > 0)")
st.dataframe(df[df["¿Apostar?"] == "✅ Sí"])
