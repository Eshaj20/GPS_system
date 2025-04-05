import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv(r"path_to_csv_file")  # Relative to project root

# Convert timestamp to datetime object
data["timestamp"] = pd.to_datetime(data["timestamp"])

# Extract new features
data["time_of_day"] = data["timestamp"].dt.hour
data["day_of_week"] = data["timestamp"].dt.day_name()

# One-hot encode categorical columns
data = pd.get_dummies(data, columns=["time_of_day", "day_of_week", "weather", "traffic_density"])

# Drop unused columns
data.drop(["timestamp", "source", "destination"], axis=1, inplace=True)

# Split into features and target
X = data.drop("duration", axis=1)
y = data["duration"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save model
with open("ml_model/route_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Model trained and saved successfully!")
