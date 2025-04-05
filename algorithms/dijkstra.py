import heapq

def dijkstra(graph, start, end):
    """ Implements Dijkstra's algorithm for shortest path finding. """
    pq = []
    heapq.heappush(pq, (0, start))
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev_nodes = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            break  # Shortest path found

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                prev_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct shortest path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev_nodes[node]
    path.reverse()

    return path, distances[end]
