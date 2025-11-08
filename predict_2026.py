import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load model
model = joblib.load("models/rf_tuned.pkl")

# Create 2026 team data (Can be expanded later)
data_2026 = {
    "team": ["Argentina", "France", "Brazil", "England",
             "Portugal", "Spain", "Germany", "Netherlands"],
    "win_rate": [0.72, 0.70, 0.69, 0.65, 0.64, 0.63, 0.60, 0.58],
    "goal_difference": [1.8, 1.6, 1.5, 1.3, 1.2, 1.1, 1.0, 0.9],
    "ranking_strength": [0.95, 0.93, 0.94, 0.91, 0.89, 0.88, 0.86, 0.85],
    "form_trend": [0.85, 0.83, 0.82, 0.81, 0.80, 0.79, 0.78, 0.77],
    "squad_age_balance": [27.5, 26.8, 27.0, 26.5, 27.2, 26.9, 27.1, 26.6],
}

df = pd.DataFrame(data_2026)

# Feature selection
features = ["win_rate", "goal_difference", "ranking_strength",
            "form_trend", "squad_age_balance"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# Predict
df["finalist_probability"] = model.predict_proba(X_scaled)[:, 1]
df["predicted_finalist"] = (df["finalist_probability"] > 0.50).astype(int)

# Save results
df.to_csv("final_predictions.csv", index=False)
print("✅ Predictions Saved: final_predictions.csv")
print(df)

# Visualization
plt.figure(figsize=(9, 5))
plt.bar(df["team"], df["finalist_probability"])
plt.xticks(rotation=45)
plt.xlabel("Team")
plt.ylabel("Finalist Probability")
plt.title("Predicted World Cup Finalist Probabilities - 2026")
plt.tight_layout()
plt.savefig("final_predictions_chart.png", dpi=300)
plt.show()
