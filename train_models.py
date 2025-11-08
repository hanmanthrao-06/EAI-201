# modeling/train_models.py
import pandas as pd
import os, joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# --- Config ---
CLEAN_PATH = "data/clean/dataset_clean.csv"
OUT_DIR = "models"
os.makedirs(OUT_DIR, exist_ok=True)

# --- Load data ---
df = pd.read_csv(CLEAN_PATH)
print("Loaded cleaned dataset:", CLEAN_PATH)
print("Columns:", df.columns.tolist())
print("Rows:", len(df))

# --- Auto-detect best candidate features (common names)
candidate_features = ["goals_for","goals_against","goal_diff","wins","losses","draws","matches_played",
                      "win_rate","loss_rate","draw_rate","goals_per_match","defense_ratio"]
features = [c for c in candidate_features if c in df.columns]

if not features:
    # If none of the usual features exist, use all numeric cols except target
    numeric_cols = df.select_dtypes(include=["int","float"]).columns.tolist()
    if "is_finalist" in numeric_cols:
        numeric_cols.remove("is_finalist")
    features = numeric_cols
    print("No standard features found — falling back to numeric columns:", features)
else:
    print("Selected features:", features)

# --- Target
if "is_finalist" not in df.columns:
    raise ValueError("Target column 'is_finalist' not found in cleaned dataset. Add it or run data_prep again.")

X = df[features].fillna(0)
y = df["is_finalist"]

# --- Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y if y.nunique()>1 else None, random_state=42)

# --- Scale numeric features for linear model
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Logistic Regression
log = LogisticRegression(max_iter=2000)
log.fit(X_train_scaled, y_train)
log_pred = log.predict(X_test_scaled)
print("\n=== Logistic Regression ===")
print("Accuracy:", accuracy_score(y_test, log_pred))
print(classification_report(y_test, log_pred))

# --- Random Forest (on original features)
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
print("\n=== Random Forest ===")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print(classification_report(y_test, rf_pred))

# --- Save artifacts
joblib.dump(log, os.path.join(OUT_DIR, "log_model.pkl"))
joblib.dump(rf, os.path.join(OUT_DIR, "rf_model.pkl"))
joblib.dump(scaler, os.path.join(OUT_DIR, "scaler.pkl"))
print("\nSaved models to", OUT_DIR)
