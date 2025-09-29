import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from RandomForest import RandomForest  # your custom RandomForest

DATA_PATH = r"processed\iotsim-combined-cycle-1.csv"
USE_DOWNSAMPLE = True       #  Toggle here: True = use sample, False = full dataset
SAMPLE_SIZE_PER_CLASS = 5000   # max per class

# ---------------------------
# Load dataset
# ---------------------------
df = pd.read_csv(DATA_PATH, low_memory=False)
print("Initial shape:", df.shape)

# ---------------------------
# Downsample if enabled
# ---------------------------
if USE_DOWNSAMPLE:
    df = df.groupby("label", group_keys=False).apply(
        lambda x: x.sample(min(len(x), SAMPLE_SIZE_PER_CLASS), random_state=42)
    )
    print("Downsampled shape:", df.shape)

# ---------------------------
# Drop leak columns (if exist)
# ---------------------------
leak_cols = ['src_ip', 'dst_ip', 'src_port', 'dst_port', 'timestamp']
df = df.drop(columns=[c for c in leak_cols if c in df.columns], errors="ignore")
print("Dropped leak columns (if present). Current shape:", df.shape)

# ---------------------------
# Binary classification: Attack vs Benign
# ---------------------------
df["label"] = df["label"].apply(lambda x: 0 if x == "Benign" else 1)
print("Binary classification: Attack vs Benign")

# ---------------------------
# Features and labels
# ---------------------------
X = df.drop(columns=["label"])
y = df["label"]

# ---------------------------
# Encode categorical features
# ---------------------------
encoders = {}
for col in X.select_dtypes(include=["object"]).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le
print(f"Encoded categorical features. Encoders prepared for columns: {list(encoders.keys())}")
joblib.dump(encoders, "encoders.joblib")
print("Saved encoders to encoders.joblib")

# ---------------------------
# Train-test split
# ---------------------------
print("Train-test split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ---------------------------
# Train Random Forest
# ---------------------------
print("Train Random Forest")
clf = RandomForest(n_trees=10, max_depth=10)
clf.fit(X_train.to_numpy(), y_train.to_numpy())

# ---------------------------
# Predict
# ---------------------------
print("Predict")
y_pred = clf.predict(X_test.to_numpy())

print("Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ---------------------------
# Save model
# ---------------------------
joblib.dump(clf, "rf_gotham_ddos.pkl")
print("Model saved as rf_gotham_ddos.pkl")
