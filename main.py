import openrouteservice
import folium
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time
from utils.news_alerts import fetch_road_alerts

ORS_API_KEY = "ORS_API_KEY_HERE"

def get_coordinates_from_city(city_name):
    try:
        geolocator = Nominatim(user_agent="city-to-coordinates")
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return [location.longitude, location.latitude]
        else:
            print(f"❌ Could not find coordinates for {city_name}")
            return None
    except Exception as e:
        print(f"❌ Error getting coordinates for {city_name}: {e}")
        return None

def get_city_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="VisionAssist/1.0 (esha@example.com)")
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        address = location.raw.get('address', {})
        city = (
            address.get('city') or
            address.get('town') or
            address.get('village') or
            address.get('county') or
            address.get('state_district') or
            address.get('state') or
            "Unknown"
        )
        print(f"📍 Detected location at [{lat:.4f}, {lon:.4f}] → {city}")
        return city
    except Exception as e:
        print(f"❌ Reverse geocoding error at [{lat}, {lon}]: {e}")
        return "Unknown"

def get_route_from_ors(source_coords, destination_coords, avoid_polygons=None):
    try:
        client = openrouteservice.Client(key=ORS_API_KEY)
        coords = [source_coords, destination_coords]

        params = {
            "coordinates": coords,
            "profile": "driving-car",
            "format": "geojson",
            "optimize_waypoints": True,
            "validate": True,
            "elevation": True,
        }

        if avoid_polygons:
            params["options"] = {"avoid_polygons": avoid_polygons}

        route = client.directions(**params)
        print("✅ Route fetched successfully!")
        return route
    except openrouteservice.exceptions.HttpError as e:
        print("🛑 HTTP Error:", e)
    except Exception as e:
        print("❌ Unexpected Error:", e)

def plot_route_on_map(route, source_coords, destination_coords, filename="route_map.html"):
    source_coords_latlon = [source_coords[1], source_coords[0]]
    destination_coords_latlon = [destination_coords[1], destination_coords[0]]

    m = folium.Map(location=source_coords_latlon, zoom_start=12)
    folium.Marker(location=source_coords_latlon, tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=destination_coords_latlon, tooltip="End", icon=folium.Icon(color='red')).add_to(m)

    colors = ["blue", "purple", "orange"]
    for i, feature in enumerate(route["features"]):
        folium.GeoJson(
            feature,
            name=f"Route {i+1}",
            style_function=lambda x, color=colors[i % len(colors)]: {"color": color, "weight": 5}
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(filename)
    print(f"✅ Map saved as {filename}")

def get_route_details(route):
    summary = route["features"][0]["properties"]["summary"]
    distance_km = summary["distance"] / 1000
    duration_min = summary["duration"] / 60
    print(f"🚗 Estimated Distance: {distance_km:.2f} km")
    print(f"⏳ Estimated Duration: {duration_min:.2f} mins")

def plot_elevation_profile(route):
    coordinates = route["features"][0]["geometry"]["coordinates"]
    distances = [0]
    elevations = [coordinates[0][2]]

    for i in range(1, len(coordinates)):
        prev = coordinates[i - 1]
        curr = coordinates[i]
        segment_distance = geodesic((prev[1], prev[0]), (curr[1], curr[0])).meters
        distances.append(distances[-1] + segment_distance)
        elevations.append(curr[2])

    distances_km = [d / 1000 for d in distances]
    plt.figure(figsize=(10, 4))
    plt.plot(distances_km, elevations, color='brown')
    plt.title("Elevation Profile")
    plt.xlabel("Distance (km)")
    plt.ylabel("Elevation (m)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("elevation_profile.png")
    plt.show()
    print("📈 Elevation profile plotted and saved as elevation_profile.png")

def show_city_alerts(cities):
    print("\n🚧 Checking for live traffic alerts...\n")
    alerts_by_city = fetch_road_alerts(cities)
    affected_cities = []

    for city in cities:
        if city in alerts_by_city and alerts_by_city[city]:
            print(f"\n🛑 Alerts for {city}:")
            for alert in alerts_by_city[city]:
                print(f" - {alert['title']} ({alert['source']}, {alert['publishedAt'][:10]})\n   🔗 {alert['url']}")
            affected_cities.append(city)
        else:
            print(f"✅ No alerts for {city}")

    return affected_cities

def get_city_polygon(city_name):
    """Get bounding polygon for a city (simplified as a buffer around its coordinates)."""
    coords = get_coordinates_from_city(city_name)
    if not coords:
        return None
    lon, lat = coords
    # Simple square polygon (0.02 deg ~ 2 km buffer) around the city center
    buffer = 0.02
    polygon = {
        "type": "Polygon",
        "coordinates": [[
            [lon-buffer, lat-buffer],
            [lon-buffer, lat+buffer],
            [lon+buffer, lat+buffer],
            [lon+buffer, lat-buffer],
            [lon-buffer, lat-buffer]
        ]]
    }
    return polygon

if __name__ == "__main__":
    source_city = input("Enter source city name: ")
    destination_city = input("Enter destination city name: ")

    source = get_coordinates_from_city(source_city)
    destination = get_coordinates_from_city(destination_city)

    if not source or not destination:
        print("❌ Unable to fetch both source and destination coordinates.")
    else:
        print("📡 Fetching initial route...")
        route = get_route_from_ors(source, destination)

        if route:
            print("\n🗺️ Plotting initial route...")
            plot_route_on_map(route, source, destination, "route_initial.html")
            get_route_details(route)
            plot_elevation_profile(route)

            print("\n🔍 Detecting intermediate cities on the route...")
            coords = route["features"][0]["geometry"]["coordinates"]
            sample_interval = max(len(coords) // 20, 1)
            sampled_points = coords[::sample_interval]

            intermediate_cities = set()
            for point in sampled_points:
                lon, lat = point[0], point[1]
                city = get_city_name(lat, lon)
                if city != "Unknown":
                    intermediate_cities.add(city)
                time.sleep(1.2)  # Respect rate limits

            if intermediate_cities:
                affected = show_city_alerts(list(intermediate_cities))

                if affected:
                    print("\n⚠️ Some cities have alerts! Re-routing to avoid them...")
                    avoid_polygons = [get_city_polygon(c) for c in affected if get_city_polygon(c)]
                    if avoid_polygons:
                        route_alt = get_route_from_ors(source, destination, avoid_polygons={"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": p} for p in avoid_polygons]})
                        if route_alt:
                            plot_route_on_map(route_alt, source, destination, "route_alternate.html")
                            get_route_details(route_alt)
                        else:
                            print("❌ Could not generate alternate route.")
                else:
                    print("✅ No affected cities, original route is safe.")
            else:
                print("⚠️ No intermediate cities could be resolved.")

