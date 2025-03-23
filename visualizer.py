import streamlit as st
import pandas as pd

def plot_match_trends(matches):
    st.subheader("📊 Total Matches Played per Season")

    if "season" not in matches.columns:
        st.error("⚠️ Column 'season' not found in dataset!")
        return

    season_wise_counts = matches.groupby("season").size().reset_index(name="matches_played")

    st.line_chart(season_wise_counts.set_index("season"))  # Using Streamlit's built-in line chart

def plot_head_to_head(matches, team1, team2):
    st.subheader(f"🏏 Head-to-Head: {team1} vs {team2}")

    if not {"team1", "team2", "winner"}.issubset(matches.columns):
        st.error("⚠️ Required columns ('team1', 'team2', 'winner') not found in dataset!")
        return

    h2h_data = matches[((matches["team1"] == team1) & (matches["team2"] == team2)) | 
                        ((matches["team1"] == team2) & (matches["team2"] == team1))]

    if h2h_data.empty:
        st.warning("⚠️ No head-to-head match data found!")
        return

    team1_wins = (h2h_data["winner"] == team1).sum()
    team2_wins = (h2h_data["winner"] == team2).sum()

    win_data = pd.DataFrame({ "Team": [team1, team2], "Wins": [team1_wins, team2_wins] })
    st.bar_chart(win_data.set_index("Team"))  # Using Streamlit's built-in bar chart
