import streamlit as st
import pandas as pd
from data_loader import load_data
from win_predictor import predict_winner
from visualizer import plot_match_trends, plot_head_to_head
from live_match_simulator import simulate_live_score
from live_scraper import get_live_score

st.set_page_config(page_title="🏏 IPL Live Analysis", layout="wide")

# Load Data
matches, deliveries = load_data()

st.title("🏏 IPL Match Analysis & Prediction")

# Sidebar for navigation
option = st.sidebar.radio(
    "Select an option",
    ["🏆 Match Prediction", "📊 Head-to-Head Stats", "📢 Live Match Simulation", "🌍 Live Score Updates"]
)

# 🏆 **Match Prediction**
if option == "🏆 Match Prediction":
    st.header("Match Winner Predictor")

    team1 = st.selectbox("Select Team 1", sorted(matches['team1'].unique()))
    team2 = st.selectbox("Select Team 2", sorted(matches['team2'].unique()))
    venue = st.selectbox("Select Venue", sorted(matches['venue'].unique()))
    toss_winner = st.selectbox("Who won the toss?", [team1, team2])
    toss_decision = st.radio("Toss Decision", ["bat", "field"])

    if st.button("Predict Match Winner"):
        result = predict_winner(team1, team2, venue, toss_winner)
        st.success(f"Predicted Winner 🏆: {result}")

# 📊 **Head-to-Head Stats**
elif option == "📊 Head-to-Head Stats":
    st.header("Team vs Team Head-to-Head Analysis")
    
    team1 = st.selectbox("Select Team 1", sorted(matches['team1'].unique()), key="h2h_team1")
    team2 = st.selectbox("Select Team 2", sorted(matches['team2'].unique()), key="h2h_team2")

    plot_head_to_head(matches, team1, team2)

    st.subheader("Match Trends Over the Years")
    plot_match_trends(matches)

# 📢 **Live Match Simulation**
elif option == "📢 Live Match Simulation":
    st.header("Simulate an IPL Match Live")
    match_id = st.selectbox("Select Match ID", sorted(deliveries["id"].unique()))
    if st.button("Start Simulation"):
        simulate_live_score(deliveries, match_id)

# 🌍 **Live Score Updates**
elif option == "🌍 Live Score Updates":
    st.header("Live IPL Match Scores")

    if st.button("Fetch Live Score"):
        live_score = get_live_score()
        st.success(f"Live Score: {live_score}")

