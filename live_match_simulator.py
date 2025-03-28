import streamlit as st
import pandas as pd
import time

def simulate_live_score(deliveries, matches, match_id):
    # Fetch match details (Team names & Venue)
    match_info = matches[matches["id"] == match_id]
    
    if match_info.empty:
        st.error("⚠️ Match details not found!")
        return

    team1 = match_info["team1"].values[0]
    team2 = match_info["team2"].values[0]
    venue = match_info["venue"].values[0]

    # Identify which team batted first (Based on first inning deliveries)
    first_inning_team = deliveries[(deliveries["match_id"] == match_id) & (deliveries["inning"] == 1)]["batting_team"].iloc[0]
    second_inning_team = team1 if first_inning_team != team1 else team2

    # Display Match Info
    st.subheader(f"🏏 Live Match Simulation - {team1} vs {team2}")
    st.write(f"📍 **Live from {venue}**")

    # Filter deliveries for selected match
    match_data = deliveries[deliveries["match_id"] == match_id]
    
    # Split into two innings
    innings_1 = match_data[match_data["inning"] == 1]
    innings_2 = match_data[match_data["inning"] == 2]

    def get_extra_type(row):
        """Determine the type of extra runs."""
        if "wide_runs" in row and row["wide_runs"] > 0:
            return "Wide"
        if "noball_runs" in row and row["noball_runs"] > 0:
            return "No Ball"
        if "bye_runs" in row and row["bye_runs"] > 0:
            return "Bye"
        if "legbye_runs" in row and row["legbye_runs"] > 0:
            return "Leg Bye"
        return None  # No extras

    def simulate_inning(inning_data, inning_num, batting_team, bowling_team):
        """Simulate an inning ball-by-ball with extra type tracking."""
        st.write(f"### 🏏 **{batting_team} is Batting | {bowling_team} is Bowling**")

        score = 0
        wickets = 0
        extras_total = 0
        batsman_scores = {}  # Dictionary to track individual batsman scores
        bowler_wickets = {}  # Dictionary to track bowlers' wickets
        
        total_balls = len(inning_data)

        for idx, row in inning_data.iterrows():
            time.sleep(0.5)  # Simulate ball delay

            # Player details
            batsman = row["batter"]
            non_striker = row["non_striker"]
            bowler = row["bowler"]

            # Runs & Extras
            runs = row["batsman_runs"]
            extras = row["extra_runs"] if "extra_runs" in row else 0
            extra_type = get_extra_type(row)

            # Update total score
            score += runs + extras
            extras_total += extras

            # Update batsman's score (only if not an extra)
            if batsman not in batsman_scores:
                batsman_scores[batsman] = 0
            if extra_type is None:  # Don't count extras in batsman's score
                batsman_scores[batsman] += runs

            # Check for wicket
            wicket_info = ""
            if "player_dismissed" in row and pd.notna(row["player_dismissed"]):
                wickets += 1
                dismissal_type = row["dismissal_kind"] if "dismissal_kind" in row else "Unknown"
                dismissed_player = row["player_dismissed"]
                wicket_info = f" ❌ {dismissed_player} Out ({dismissal_type})"
                batsman_scores.pop(dismissed_player, None)  # Remove dismissed player
                
                # Track bowler wickets
                if bowler not in bowler_wickets:
                    bowler_wickets[bowler] = 0
                bowler_wickets[bowler] += 1

            # Extras Display
            extra_display = f" | **Extras:** {extras} ({extra_type})" if extra_type else ""

            # Display full ball details
            st.write(f"🎾 **Over {row['over']}.{row['ball']}** | {batsman} vs {bowler} | Runs: {runs}{extra_display}{wicket_info}")

            # Display Updated Scoreboard
            st.write(f"🏏 **Score: {score}/{wickets}** | {batsman}: {batsman_scores.get(batsman, 0)}* | {non_striker}: {batsman_scores.get(non_striker, 0)} | Extras: {extras_total}")

        st.success(f"🏆 {batting_team} Inning {inning_num} Ends! Final Score: {score}/{wickets} (Extras: {extras_total})")

        # 📊 Display Scorecard
        show_scorecard(batsman_scores, bowler_wickets, score, wickets, extras, batting_team)

    def show_scorecard(batsman_scores, bowler_wickets, total_score, wickets, extras, team):
        """Display a detailed scoreboard at the end of the innings."""
        st.subheader(f"📋 {team} Scorecard")

        # Batsman Scores
        st.write("### 🏏 Batting Performance")
        batsman_df = pd.DataFrame({
            "Batsman": list(batsman_scores.keys()),
            "Runs": list(batsman_scores.values())
        })
        st.table(batsman_df)

        # Bowler Wickets
        st.write("### 🎯 Bowling Performance")
        bowler_df = pd.DataFrame({
            "Bowler": list(bowler_wickets.keys()),
            "Wickets": list(bowler_wickets.values())
        })
        st.table(bowler_df)

        st.write(f"🏏 **Final Score:** {total_score}/{wickets} | Extras: {extras}")

    # Simulate First Innings
    simulate_inning(innings_1, 1, first_inning_team, second_inning_team)

    # Break before second innings
    st.write("## 🏏 **Innings Break** ⏸️")
    time.sleep(2)  # Simulated break time

    # Simulate Second Innings
    simulate_inning(innings_2, 2, second_inning_team, first_inning_team)
    
    # Match Summary
    st.subheader("📢 **Match Summary**")
    team1_score = f"{innings_1['total_runs'].sum()}/{innings_1['player_dismissed'].count()}"
    team2_score = f"{innings_2['total_runs'].sum()}/{innings_2['player_dismissed'].count()}"

    st.write(f"🏏 **{first_inning_team} Score:** {team1_score}")
    st.write(f"🏏 **{second_inning_team} Score:** {team2_score}")

    # Determine Winner
    if innings_1["total_runs"].sum() > innings_2["total_runs"].sum():
        st.success(f"🎉 **{first_inning_team} Wins the Match!** 🏆")
    elif innings_1["total_runs"].sum() < innings_2["total_runs"].sum():
        st.success(f"🎉 **{second_inning_team} Wins the Match!** 🏆")
    else:
        st.warning("🤝 **Match Tied!**")

    st.success("🎉 Match Simulation Completed!")
