import folium

def plot_route_on_map(waypoints, filename="route_map.html"):
    """ Plots the shortest route on an interactive map using Folium. """
    map_ = folium.Map(location=waypoints[0], zoom_start=12)

    # Add markers
    folium.Marker(waypoints[0], tooltip="Start", icon=folium.Icon(color="green")).add_to(map_)
    folium.Marker(waypoints[-1], tooltip="End", icon=folium.Icon(color="red")).add_to(map_)

    # Draw the route
    folium.PolyLine(waypoints, color="blue", weight=5, opacity=0.7).add_to(map_)

    # Save to file
    map_.save(filename)
    print(f"✅ Route map saved as {filename}")
