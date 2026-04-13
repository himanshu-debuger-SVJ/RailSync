import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("data.csv")

# Convert delay into classes
def classify_delay(x):
    if x <= 5:
        return 0   # On time
    elif x <= 30:
        return 1   # Minor delay
    else:
        return 2   # Major delay

df["delay_class"] = df["delay_minutes"].apply(classify_delay)

# Encode route (text → numeric)
route_encoder = LabelEncoder()
df["route_encoded"] = route_encoder.fit_transform(df["route"])

# Features and target
X = df[["hour", "day", "month", "route_encoded"]]
y = df["delay_class"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoder
joblib.dump(model, "model.pkl")
joblib.dump(route_encoder, "encoder.pkl")

print("✅ Model trained and saved successfully!")