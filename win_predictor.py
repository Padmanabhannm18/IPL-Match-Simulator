import os
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Ensure the models folder exists
if not os.path.exists("models"):
    os.makedirs("models")

def train_win_predictor():
    file_path = "data/matches.csv"

    if not os.path.exists(file_path):
        print(f"❌ ERROR: Data file not found at {file_path}")
        return
    
    matches = pd.read_csv(file_path)

    # Debug: Print available columns
    print("✅ Available Columns in CSV:")
    print(matches.columns)

    # Check if required columns exist
    required_columns = {"team1", "team2", "toss_winner", "winner", "venue"}
    if not required_columns.issubset(matches.columns):
        print(f"❌ ERROR: Missing columns {required_columns - set(matches.columns)}")
        return

    # 🔹 Train encoder on the FULL dataset before splitting
    encoder = LabelEncoder()
    all_labels = pd.concat([matches["team1"], matches["team2"], matches["toss_winner"], matches["winner"], matches["venue"]])
    encoder.fit(all_labels)  # Fit on ALL unique values

    # Apply encoding
    for col in ["team1", "team2", "toss_winner", "winner", "venue"]:
        matches[col] = encoder.transform(matches[col])

    # Prepare training data
    X = matches[["team1", "team2", "toss_winner", "venue"]]
    y = matches["winner"]

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    with open("models/win_predictor.pkl", "wb") as f:
        pickle.dump(model, f)

    # Save Label Encoder
    with open("models/win_encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)

    print("✅ Match Winner Prediction Model Trained & Saved!")
def predict_winner(team1, team2, venue, toss_winner):
    model_path = "models/win_predictor.pkl"
    encoder_path = "models/win_encoder.pkl"

    # Check if model exists
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        return "🚨 Model not trained! Please run `train_win_predictor()` first."

    # Load Model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Load Encoder
    with open(encoder_path, "rb") as f:
        encoder = pickle.load(f)

    # Handle unseen labels
    try:
        team1_enc = encoder.transform([team1])[0]
        team2_enc = encoder.transform([team2])[0]
        toss_winner_enc = encoder.transform([toss_winner])[0]
        venue_enc = encoder.transform([venue])[0]
    except ValueError as e:
        return f"🚨 Error: Unrecognized team/venue. Make sure all teams exist in training data."

    # Predict Winner
    prediction = model.predict([[team1_enc, team2_enc, toss_winner_enc, venue_enc]])[0]
    
    # Decode prediction back to team name
    predicted_team = encoder.inverse_transform([prediction])[0]
    return f"{predicted_team}"

# Run training when executed
if __name__ == "__main__":
    train_win_predictor()
