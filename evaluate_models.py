# modeling/evaluate_models.py
import pandas as pd, joblib, os
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/clean/dataset_clean.csv")
features = [f for f in ["goals_for","goals_against","goal_diff","win_rate","loss_rate","draw_rate"] if f in df.columns]
if not features:
    features = df.select_dtypes(include=["int","float"]).columns.tolist()
    if "is_finalist" in features: features.remove("is_finalist")

X = df[features].fillna(0)
y = df["is_finalist"]

log = joblib.load("models/log_model.pkl")
rf = joblib.load("models/rf_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# logistic uses scaled features
X_scaled = scaler.transform(X)

# predictions
log_pred = log.predict(X_scaled)
rf_pred = rf.predict(X)

# classification reports
print("=== Logistic Report ===")
print(classification_report(y, log_pred))
print("=== Random Forest Report ===")
print(classification_report(y, rf_pred))

# confusion matrix for RF
cm = confusion_matrix(y, rf_pred)
plt.figure(figsize=(4,3))
plt.imshow(cm, interpolation='nearest')
plt.colorbar()
plt.title("Confusion Matrix (RF)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i,j], ha='center', va='center', color='white')
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/confusion_matrix.png")
plt.close()
print("Saved plots/confusion_matrix.png")

# ROC for RF (if predict_proba exists)
if hasattr(rf, "predict_proba"):
    probs = rf.predict_proba(X)[:,1]
    fpr, tpr, _ = roc_curve(y, probs)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.plot([0,1],[0,1],'--')
    plt.title(f"ROC (RF) AUC={roc_auc:.3f}")
    plt.savefig("plots/roc_curve.png")
    plt.close()
    print("Saved plots/roc_curve.png")

# feature importance
if hasattr(rf, "feature_importances_"):
    fi = rf.feature_importances_
    order = np.argsort(fi)
    labels = np.array(features)[order]
    plt.figure(figsize=(6,4))
    plt.barh(labels, fi[order])
    plt.title("Feature importance (RF)")
    plt.savefig("plots/feature_importance.png")
    plt.close()
    print("Saved plots/feature_importance.png")
