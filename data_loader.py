import pandas as pd
import streamlit as st
def load_data():
    matches = pd.read_csv("data\matches.csv")
    deliveries = pd.read_csv("data\deliveries.csv")
    
    deliveries = deliveries.sort_values(by=["match_id", "inning", "over", "ball"]).reset_index(drop=True)

    # Extract year from the 'date' column to create a 'season' column
    matches["date"] = pd.to_datetime(matches["date"])  # Convert to datetime
    matches["season"] = matches["date"].dt.year  # Extract the year

    return matches,deliveries

