import pickle
import pandas as pd

# Load the trained model and columns
with open("route_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("model_columns.pkl", "rb") as file:
    model_columns = pickle.load(file)

def predict_route(time_of_day, day_of_week, weather, traffic_density):
    # Prepare input as a DataFrame
    input_data = pd.DataFrame([[time_of_day, day_of_week, weather, traffic_density]],
                              columns=["time_of_day", "day_of_week", "weather", "traffic_density"])

    # One-hot encode the input
    input_data = pd.get_dummies(input_data)

    # Add any missing columns from training with 0s
    for col in model_columns:
        if col not in input_data:
            input_data[col] = 0

    # Ensure column order matches training
    input_data = input_data[model_columns]

    # Predict
    prediction = model.predict(input_data)
    return prediction[0]

# Example usage
if __name__ == "__main__":
    best_route_duration = predict_route("10", "Monday", "Sunny", "High")
    print(f"🚗 Predicted Duration: {best_route_duration:.2f} minutes")
