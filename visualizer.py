import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_match_trends(matches):
    st.subheader("Total Matches Played per Season")

    # Ensure 'season' column exists
    if "season" not in matches.columns:
        st.error("Column 'season' not found in dataset!")
        return

    season_wise_counts = matches.groupby("season").size()
    
    fig, ax = plt.subplots()
    season_wise_counts.plot(kind="bar", ax=ax, color="royalblue")
    ax.set_xlabel("Season")
    ax.set_ylabel("Matches Played")
    ax.set_title("Matches per IPL Season")

    st.pyplot(fig)

def plot_head_to_head(matches, team1, team2):
    st.subheader(f"Head-to-Head: {team1} vs {team2}")
    h2h_data = matches[(matches["team1"] == team1) & (matches["team2"] == team2)]
    
    if h2h_data.empty:
        st.warning("No head-to-head match data found!")
        return

    team1_wins = (h2h_data["winner"] == team1).sum()
    team2_wins = (h2h_data["winner"] == team2).sum()

    fig, ax = plt.subplots()
    ax.bar([team1, team2], [team1_wins, team2_wins], color=["blue", "red"])
    ax.set_ylabel("Matches Won")
    st.pyplot(fig)
