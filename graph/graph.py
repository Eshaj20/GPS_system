import json

class Graph:
    """ Graph class to handle road networks and routing. """
    def __init__(self, file_path):
        self.graph = self.load_graph(file_path)

    def load_graph(self, file_path):
        """ Loads road network from JSON file. """
        with open(file_path, 'r') as file:
            return json.load(file)

    def get_neighbors(self, node):
        """ Returns connected nodes with weights. """
        return self.graph.get(node, {})
