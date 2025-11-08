# combine_data.py
import pandas as pd
import os

RAW_DIR = "data/raw"
OUT_FILE = "data/raw/combined_raw.csv"

# Load team appearances (each team per tournament)
team_appearances = pd.read_csv(os.path.join(RAW_DIR, "team_appearances.csv"))
tournaments = pd.read_csv(os.path.join(RAW_DIR, "tournaments.csv"))
teams = pd.read_csv(os.path.join(RAW_DIR, "teams.csv"))

# Keep only the useful columns
team_appearances = team_appearances[
    [
        "team_id",
        "tournament_id",
        "goals_for",
        "goals_against",
        "wins_count",
        "losses_count",
        "draws_count",
        "matches_played_count",
        "minutes_played_count",
    ]
]

tournaments = tournaments[["tournament_id", "year", "host_country_id", "tournament_name"]]
teams = teams[["team_id", "team_name", "fifa_code", "confederation_id"]]

# Merge them
df = (
    team_appearances
    .merge(tournaments, on="tournament_id", how="left")
    .merge(teams, on="team_id", how="left")
)

# Basic feature engineering
df["goal_diff"] = df["goals_for"] - df["goals_against"]
df["win_rate"] = df["wins"] / df["matches_played"]
df["loss_rate"] = df["losses"] / df["matches_played"]

# Create is_finalist label using tournament_standings
standings = pd.read_csv(os.path.join(RAW_DIR, "tournament_standings.csv"))
finalists = standings[standings["position"].isin([1, 2])][
    ["tournament_id", "team_id", "position"]
].copy()
finalists["is_finalist"] = 1

df = df.merge(finalists[["tournament_id", "team_id", "is_finalist"]], on=["tournament_id", "team_id"], how="left")
df["is_finalist"] = df["is_finalist"].fillna(0).astype(int)

# Rename columns for clarity
df = df.rename(columns={
    "team_name": "team",
    "year": "season",
    "tournament_name": "tournament"
})

# Save
os.makedirs("data/raw", exist_ok=True)
df.to_csv(OUT_FILE, index=False)
print(f"✅ Combined data saved to {OUT_FILE}")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print(df.head())
