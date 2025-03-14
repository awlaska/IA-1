import os
import sys
import math
import heapq
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../bidirectionalastar/")


class BidirectionalAStar:
    def __init__(self, s_start, s_goal, heuristic_type, graph, weights):
        self.s_start = s_start
        self.s_goal = s_goal
        self.heuristic_type = heuristic_type
        self.graph = graph  # adjacency list representation of graph
        self.weights = weights  # Weights for kms, litros, and minutos

        self.OPEN_fore = []
        self.OPEN_back = []
        self.CLOSED_fore = set()
        self.CLOSED_back = set()
        self.PARENT_fore = {}
        self.PARENT_back = {}
        self.g_fore = {}
        self.g_back = {}
        self.all_paths = []

    def init(self):
        """Initialize search structures."""
        self.g_fore[self.s_start] = 0.0
        self.g_back[self.s_goal] = 0.0
        self.PARENT_fore[self.s_start] = None
        self.PARENT_back[self.s_goal] = None

        heapq.heappush(self.OPEN_fore, (self.f_value_fore(self.s_start), self.s_start))
        heapq.heappush(self.OPEN_back, (self.f_value_back(self.s_goal), self.s_goal))

    def searching(self):
        """Perform bidirectional A* search."""
        self.init()
        s_meet = None

        while self.OPEN_fore and self.OPEN_back:
            _, s_fore = heapq.heappop(self.OPEN_fore)
            if s_fore in self.PARENT_back:
                s_meet = s_fore
                self.all_paths.append(self.extract_path(s_meet))

            self.CLOSED_fore.add(s_fore)

            for s_n in self.get_neighbors(s_fore):
                new_cost = self.g_fore[s_fore] + self.cost(s_fore, s_n)
                if s_n not in self.g_fore or new_cost < self.g_fore[s_n]:
                    self.g_fore[s_n] = new_cost
                    self.PARENT_fore[s_n] = s_fore
                    heapq.heappush(self.OPEN_fore, (self.f_value_fore(s_n), s_n))

            _, s_back = heapq.heappop(self.OPEN_back)
            if s_back in self.PARENT_fore:
                s_meet = s_back
                self.all_paths.append(self.extract_path(s_meet))

            self.CLOSED_back.add(s_back)

            for s_n in self.get_neighbors(s_back):
                new_cost = self.g_back[s_back] + self.cost(s_back, s_n)
                if s_n not in self.g_back or new_cost < self.g_back[s_n]:
                    self.g_back[s_n] = new_cost
                    self.PARENT_back[s_n] = s_back
                    heapq.heappush(self.OPEN_back, (self.f_value_back(s_n), s_n))

        return self.all_paths if self.all_paths else None

    def get_neighbors(self, s):
        return self.graph.get(s, {}).keys()

    def extract_path(self, s_meet):
        """Reconstruct the optimal path."""
        path_fore = []
        s = s_meet
        while s is not None:
            path_fore.append(s)
            s = self.PARENT_fore.get(s)

        path_back = []
        s = self.PARENT_back.get(s_meet)
        while s is not None:
            path_back.append(s)
            s = self.PARENT_back.get(s)

        return list(reversed(path_fore)) + path_back

    def f_value_fore(self, s):
        return self.g_fore.get(s, math.inf) + self.h(s, self.s_goal)

    def f_value_back(self, s):
        return self.g_back.get(s, math.inf) + self.h(s, self.s_start)

    def h(self, s, goal):
        """Heuristic function (currently disabled)."""
        return 0  # Can be modified if a heuristic is needed

    def cost(self, s_start, s_goal):
        edge = self.graph[s_start][s_goal]
        return (self.weights['kms'] * edge['kms'] +
                self.weights['litros'] * edge['litros'] +
                self.weights['minutos'] * edge['minutos'])

    def get_path_cost(self, path):
        total_kms = 0
        total_litros = 0
        total_minutos = 0
        for i in range(len(path) - 1):
            start, end = path[i], path[i + 1]
            edge_data = self.graph[start][end]
            total_kms += edge_data['kms']
            total_litros += edge_data['litros']
            total_minutos += edge_data['minutos']
        return total_kms, total_litros, total_minutos


def load_graph_from_csv(filename):
    """Load graph data from CSV file with bidirectional edges."""
    df = pd.read_csv(filename, header=None, names=["start", "end", "kms", "litros", "minutos"])
    graph = {}

    for _, row in df.iterrows():
        start, end = row["start"], row["end"]
        edge_data = {"kms": row["kms"], "litros": row["litros"], "minutos": row["minutos"]}

        if start not in graph:
            graph[start] = {}
        if end not in graph:
            graph[end] = {}

        graph[start][end] = edge_data
        graph[end][start] = edge_data  # Ensure bidirectional edges

    return graph


def main():
    filename = "../graph/graph3.csv"  # Adjust this if needed
    graph = load_graph_from_csv(filename)

    start_node = "A"
    goal_node = "L"
    weights = {"kms": 1.0, "litros": 1.0, "minutos": 1.0}  # Adjustable weights

    bastar = BidirectionalAStar(start_node, goal_node, "none", graph, weights)
    all_paths = bastar.searching()

    if all_paths:
        print("Todos os caminhos encontrados:")
        best_kms, best_litros, best_minutos = float('inf'), float('inf'), float('inf')
        best_path_kms, best_path_litros, best_path_minutos = None, None, None

        for path in all_paths:
            total_kms, total_litros, total_minutos = bastar.get_path_cost(path)

            # Compare and select the optimal paths for each variable
            if total_kms < best_kms:
                best_kms = total_kms
                best_path_kms = path

            if total_litros < best_litros:
                best_litros = total_litros
                best_path_litros = path

            if total_minutos < best_minutos:
                best_minutos = total_minutos
                best_path_minutos = path

        print(f"\nCaminho otimizado para kms: {best_path_kms} com custo {best_kms} kms")
        print(f"Caminho otimizado para litros: {best_path_litros} com custo {best_litros} litros")
        print(f"Caminho otimizado para minutos: {best_path_minutos} com custo {best_minutos} minutos")
    else:
        print("Nenhum caminho encontrado entre", start_node, "e", goal_node)


if __name__ == '__main__':
    main()
