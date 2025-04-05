import pickle
import pandas as pd

# Load the trained model
with open(r"C:\Users\eshaa\GPS_system\ml_model\route_model.pkl", "rb") as file:
    model = pickle.load(file)

def predict_route(time_of_day, day_of_week, weather, traffic_density):
    """ Predicts the best route based on input conditions. """
    
    # Convert inputs into dataframe format
    input_data = pd.DataFrame([[time_of_day, day_of_week, weather, traffic_density]],
                              columns=["time_of_day", "day_of_week", "weather", "traffic_density"])
    
    # Convert categorical data to numerical
    input_data = pd.get_dummies(input_data)

    # Make prediction
    predicted_route = model.predict(input_data)
    
    return predicted_route[0]

# Example prediction
if __name__ == "__main__":
    best_route = predict_route("Morning", "Monday", "Sunny", "High")
    print(f"🚗 Predicted Best Route: {best_route}")
