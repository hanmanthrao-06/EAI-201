# predict_final.py (robust debug + fallback)
import os, sys, traceback
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

print("=== predict_final.py starting ===")
print("Working dir:", os.getcwd())
print("Python:", sys.executable)
print()

# 1) check files
print("Root files:")
for f in sorted(os.listdir(".")):
    print(" ", f)
print()

models_dir = "models"
print("Models folder listing:")
if os.path.exists(models_dir):
    for f in sorted(os.listdir(models_dir)):
        print(" ", f)
else:
    print("  (models folder not found)")
print()

# 2) load model
model_path = os.path.join("models", "rf_tuned.pkl")
if not os.path.exists(model_path):
    print("ERROR: model file not found at", model_path)
    sys.exit(1)

try:
    model = joblib.load(model_path)
    print("Loaded model from", model_path)
    print("Model type:", type(model))
except Exception as e:
    print("ERROR loading model:", e)
    traceback.print_exc()
    sys.exit(1)
print()

# 3) Inspect model for expected feature names (scikit-learn stores them sometimes)
expected_features = None
if hasattr(model, "feature_names_in_"):
    try:
        expected_features = list(model.feature_names_in_)
        print("Model.feature_names_in_ found:", expected_features)
    except Exception as e:
        print("Could not read model.feature_names_in_:", e)

# 4) Build the future-data DataFrame (you can edit values here)
data_2026 = {
    "team": ["Argentina", "France", "Brazil", "England", "Portugal", "Spain", "Germany", "Netherlands"],
    # These are fallback fields — we will adapt to model expected features below
    "goals_for": [2.1, 2.0, 1.9, 1.8, 1.7, 1.7, 1.6, 1.5],
    "goals_against": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "goal_diff": [1.8, 1.6, 1.4, 1.2, 1.0, 0.9, 0.7, 0.5],
    "draw_rate": [0.10, 0.12, 0.15, 0.14, 0.13, 0.11, 0.16, 0.18],
    "loss_rate": [0.05, 0.08, 0.10, 0.12, 0.10, 0.13, 0.15, 0.17],
    # extra possible features (harmless if unused)
    "win_rate": [0.72,0.70,0.69,0.65,0.64,0.63,0.60,0.58],
    "ranking_strength": [0.95,0.93,0.94,0.91,0.89,0.88,0.86,0.85],
}
df = pd.DataFrame(data_2026)
print("Future DataFrame shape:", df.shape)
print(df.head().to_string(index=False))
print()

# 5) Determine features to feed the model
# Priority: use model.feature_names_in_ if present; else infer from training-time features seen earlier in error messages
if expected_features:
    use_features = expected_features
else:
    # fallback list that often worked for your project
    fallback = ["goals_for","goals_against","goal_diff","draw_rate","loss_rate"]
    # use whichever of fallback exists in df
    use_features = [c for c in fallback if c in df.columns]
    print("No model.feature_names_in_; using fallback features found in df:", use_features)

# Ensure all expected columns exist; if missing, create them with zeros
missing = [c for c in use_features if c not in df.columns]
if missing:
    print("Adding missing columns with zeros:", missing)
    for c in missing:
        df[c] = 0.0

# Reorder X according to model expectation
X = df[use_features].copy()
print("Final feature columns used for prediction:", use_features)
print("X shape:", X.shape)
print()

# 6) Try prediction with helpful error handling
probs = None
try:
    if hasattr(model, "predict_proba"):
        print("Trying model.predict_proba(X)...")
        probs = model.predict_proba(X)[:, 1]
        print("predict_proba OK. sample:", probs[:4])
    else:
        print("Model has no predict_proba. Using predict() instead and mapping to 0/1.")
        preds = model.predict(X)
        probs = preds.astype(float)  # fallback to 0/1 as probability
        print("predict() OK. sample:", preds[:4])
except ValueError as ve:
    # likely feature name mismatch; show message and try reindexing if model has feature_names_in_ or uses different names
    print("ValueError during prediction:", ve)
    traceback.print_exc()
    # Attempt reindexing by intersecting columns that model may accept if feature_names_in_ present
    if hasattr(model, "feature_names_in_"):
        print("Attempting reindex with model.feature_names_in_ ...")
        fn = list(model.feature_names_in_)
        # add any missing columns as zeros
        for c in fn:
            if c not in df.columns:
                df[c] = 0.0
        X2 = df[fn]
        try:
            probs = model.predict_proba(X2)[:, 1] if hasattr(model,"predict_proba") else model.predict(X2)
            use_features = fn
            X = X2
            print("Reindex+predict OK. sample:", probs[:4])
        except Exception as e:
            print("Reindex attempt failed:", e)
            traceback.print_exc()
    else:
        print("No feature_names_in_ available; trying to match by simple name variants...")
        # try to map common synonyms
        mapping = {
            "goal_difference":"goal_diff",
            "goals_difference":"goal_diff",
            "goals_for":"goals_for",
            "goals_against":"goals_against",
            "draw_rate":"draw_rate",
            "loss_rate":"loss_rate",
            "win_rate":"win_rate"
        }
        for src, tgt in mapping.items():
            if src in df.columns and tgt not in df.columns:
                df[tgt] = df[src]
        # try with fallback features again
        try:
            X3 = df[use_features]
            probs = model.predict_proba(X3)[:,1] if hasattr(model,"predict_proba") else model.predict(X3)
            print("Second attempt succeeded. sample:", probs[:4])
            X = X3
        except Exception as e:
            print("Second attempt also failed:", e)
            traceback.print_exc()

except Exception as e:
    print("Unexpected error during prediction:", e)
    traceback.print_exc()

# 7) If we obtained probs, save results
if probs is None:
    print("\nERROR: No probabilities computed. Prediction failed. See messages above.")
    sys.exit(1)

df["finalist_probability"] = np.array(probs).reshape(-1)
df["predicted_finalist"] = (df["finalist_probability"] >= 0.50).astype(int)

out_csv = "final_predictions.csv"
df.to_csv(out_csv, index=False)
print("\n✅ Predictions saved to", out_csv)
print(df[["team","finalist_probability","predicted_finalist"]])

# 8) Save plot
try:
    plt.figure(figsize=(10,5))
    plt.bar(df["team"], df["finalist_probability"], color="tab:blue")
    plt.ylabel("Finalist Probability")
    plt.title("World Cup 2026 - Finalist Prediction")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    img_out = "final_predictions_chart.png"
    plt.savefig(img_out, dpi=200)
    print("✅ Saved chart to", img_out)
except Exception as e:
    print("Failed to save chart:", e)
    traceback.print_exc()

print("\n=== predict_final.py finished ===")
