from graph.graph import Graph
from algorithms.dijkstra import dijkstra
from ml_model.predict_route import predict_route

def get_optimized_route(graph_file, start, end, time_of_day, day_of_week, weather, traffic_density):
    """ Predicts the best route and finds the shortest path using Dijkstra. """
    
    # Load road graph
    graph = Graph(graph_file)

    # Get ML-based best route
    predicted_route = predict_route(time_of_day, day_of_week, weather, traffic_density).split(" → ")

    # Find shortest path using Dijkstra
    shortest_path, distance = dijkstra(graph.graph, start, end)

    print(f"🛣 ML Predicted Best Route: {predicted_route}")
    print(f"📏 Dijkstra’s Shortest Path: {shortest_path}")

    return shortest_path

# Example run
if __name__ == "__main__":
    get_optimized_route("../data/sample_map.json", "A", "D", "Morning", "Monday", "Sunny", "High")
