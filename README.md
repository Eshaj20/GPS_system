## Smart GPS Routing System

- Calculates the best driving route between two cities
- Displays an interactive route map (`route_map.html`)
- Detects intermediate cities using reverse geocoding
- Fetches real-time **traffic-related news alerts** for those cities

---

# Features

- Route plotting with OpenRouteService
- Dynamic map with intermediate waypoints
- City detection along the path
- Live traffic alerts from NewsAPI
- Filters out irrelevant news (e.g., airport alerts)

---

# Tech Stack

- Python 3.8+
- OpenRouteService API
- NewsAPI
- Folium (map visualization)
- Geopy, Requests, Dotenv

---

# Project Structure
```bash
algorithms/
├── __pycache__/
├── dijkstra.py
├── ml_route_predict.py
data/
├── historical_traffic.csv
├── sample_map.json
graph/
├── __pycache__/
├── graph.py
├── union_find.py
ml_model/
├── __pycache__/
├── predict_route.py
├── route_model.pk1
├── train_model.py
├── model_columns.pk1
utils/
├── __pycache__/
├── news_alerts.py
├── visualizer.py
app.py
elevation_profile.png
main.py
README.md
requirements.txt
route_map.html
```
# Run python file
            python main.py

# Install dependencies
            pip install -r requirements.txt

# Add your API keys

Create a .env file:

            ORS_API_KEY=your_openrouteservice_key
            NEWS_API_KEY=your_newsapi_key
            
# Future Enhancements

- Enhanced Routing Algorithms: Incorporate additional algorithms for improved route optimization.
- User Preferences: Allow users to set preferences (e.g., avoid tolls, prefer highways).
- Mobile Responsiveness: Optimize the application for mobile devices.
- Historical Traffic Data: Integrate historical traffic patterns for better predictions.


