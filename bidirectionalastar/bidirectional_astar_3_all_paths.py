import os
import sys
import math
import heapq
import pandas as pd
from itertools import permutations

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../bidirectionalastar/")


class BidirectionalAStar:
    def __init__(self, s_start, s_goal, heuristic_type, graph, weights):
        self.s_start = s_start
        self.s_goal = s_goal
        self.heuristic_type = heuristic_type
        self.graph = graph  # representação da lista de adjacência do grafo
        self.weights = weights  # Pesos para kms, litros e minutos

    def find_all_paths(self, start, goal, path=[]):
        """Encontra todos os caminhos possíveis de start a goal."""
        path = path + [start]
        if start == goal:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path:
                new_paths = self.find_all_paths(node, goal, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def calculate_cost(self, path):
        """Calcula o custo total de um caminho."""
        total_kms = 0
        total_litros = 0
        total_minutos = 0
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            edge_data = self.graph[start][end]
            total_kms += edge_data['kms']
            total_litros += edge_data['litros']
            total_minutos += edge_data['minutos']
        return total_kms, total_litros, total_minutos

    def find_best_path(self):
        """Encontra todos os caminhos possíveis e retorna o que minimiza as três variáveis."""
        all_paths = self.find_all_paths(self.s_start, self.s_goal)
        if not all_paths:
            print("Nenhum caminho encontrado entre", self.s_start, "e", self.s_goal)
            return

        best_path = None
        min_cost = (math.inf, math.inf, math.inf)

        print("Caminhos possíveis e seus custos:")
        for path in all_paths:
            total_kms, total_litros, total_minutos = self.calculate_cost(path)
            print(f"{path} -> KMs: {total_kms}, Litros: {total_litros}, Minutos: {total_minutos}")

            if (total_kms, total_litros, total_minutos) < min_cost:
                min_cost = (total_kms, total_litros, total_minutos)
                best_path = path

        print("\nMelhor caminho encontrado:")
        print(f"{best_path} -> KMs: {min_cost[0]}, Litros: {min_cost[1]}, Minutos: {min_cost[2]}")


def load_graph_from_csv(filename):
    """Carrega os dados do grafo a partir de um arquivo CSV."""
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
        graph[end][start] = edge_data  # Garante conexões bidirecionais

    return graph


def main():
    filename = "../graph/graph3_2.csv"  # Ajuste conforme necessário
    graph = load_graph_from_csv(filename)

    start_node = "A"
    goal_node = "L"
    weights = {"kms": 1.0, "litros": 1.0, "minutos": 1.0}  # Pesos ajustáveis

    bastar = BidirectionalAStar(start_node, goal_node, "none", graph, weights)
    bastar.find_best_path()


if __name__ == '__main__':
    main()
