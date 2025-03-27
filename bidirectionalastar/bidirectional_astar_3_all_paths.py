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
        self.graph = graph
        self.weights = weights

        self.OPEN_fore = []
        self.OPEN_back = []
        self.CLOSED_fore = set()
        self.CLOSED_back = set()
        self.PARENT_fore = {}
        self.PARENT_back = {}
        self.g_fore = {}
        self.g_back = {}
        self.meeting_nodes = []

    def init(self):
        self.g_fore[self.s_start] = 0.0
        self.g_back[self.s_goal] = 0.0
        self.PARENT_fore[self.s_start] = []
        self.PARENT_back[self.s_goal] = []

        heapq.heappush(self.OPEN_fore, (self.f_value_fore(self.s_start), self.s_start))
        heapq.heappush(self.OPEN_back, (self.f_value_back(self.s_goal), self.s_goal))

    def searching(self):
        self.init()

        while self.OPEN_fore and self.OPEN_back:
            _, s_fore = heapq.heappop(self.OPEN_fore)
            if s_fore in self.PARENT_back:
                self.meeting_nodes.append(s_fore)

            self.CLOSED_fore.add(s_fore)

            for s_n in self.get_neighbors(s_fore):
                new_cost = self.g_fore[s_fore] + self.cost(s_fore, s_n)
                if s_n not in self.g_fore or new_cost < self.g_fore[s_n]:
                    self.g_fore[s_n] = new_cost
                    self.PARENT_fore[s_n] = [s_fore]
                    heapq.heappush(self.OPEN_fore, (self.f_value_fore(s_n), s_n))
                elif new_cost == self.g_fore[s_n]:
                    self.PARENT_fore[s_n].append(s_fore)

            _, s_back = heapq.heappop(self.OPEN_back)
            if s_back in self.PARENT_fore:
                self.meeting_nodes.append(s_back)

            self.CLOSED_back.add(s_back)

            for s_n in self.get_neighbors(s_back):
                new_cost = self.g_back[s_back] + self.cost(s_back, s_n)
                if s_n not in self.g_back or new_cost < self.g_back[s_n]:
                    self.g_back[s_n] = new_cost
                    self.PARENT_back[s_n] = [s_back]
                    heapq.heappush(self.OPEN_back, (self.f_value_back(s_n), s_n))
                elif new_cost == self.g_back[s_n]:
                    self.PARENT_back[s_n].append(s_back)

        if self.meeting_nodes:
            return self.extract_all_paths(), self.CLOSED_fore, self.CLOSED_back
        else:
            return [], self.CLOSED_fore, self.CLOSED_back

    def get_neighbors(self, s):
        return self.graph.get(s, {}).keys()

    def extract_all_paths(self):
        all_paths = []
        for node in self.meeting_nodes:
            paths_fore = self.reconstruct_paths(self.PARENT_fore, node, direction='fore')
            paths_back = self.reconstruct_paths(self.PARENT_back, node, direction='back')
            for fore in paths_fore:
                for back in paths_back:
                    all_paths.append(fore + back[1:])
        return all_paths

    def reconstruct_paths(self, parents, node, direction):
        if direction == 'fore':
            if not parents[node]:
                return [[node]]
            paths = []
            for parent in parents[node]:
                for path in self.reconstruct_paths(parents, parent, direction):
                    paths.append(path + [node])
            return paths
        else:
            if not parents[node]:
                return [[node]]
            paths = []
            for parent in parents[node]:
                for path in self.reconstruct_paths(parents, parent, direction):
                    paths.append([node] + path)
            return paths

    def f_value_fore(self, s):
        return self.g_fore.get(s, math.inf) + self.h(s, self.s_goal)

    def f_value_back(self, s):
        return self.g_back.get(s, math.inf) + self.h(s, self.s_start)

    def h(self, s, goal):
        return 0

    def cost(self, s_start, s_goal):
        edge = self.graph[s_start][s_goal]
        return (self.weights['kms'] * edge['kms'] +
                self.weights['litros'] * edge['litros'] +
                self.weights['minutos'] * edge['minutos'])


def load_graph_from_csv(filename):
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
        graph[end][start] = edge_data

    return graph


def main():
    filename = "../graph3.csv"
    graph = load_graph_from_csv(filename)

    start_node = "A"
    goal_node = "L"
    weights = {"kms": 1.0, "litros": 1.0, "minutos": 1.0}

    bastar = BidirectionalAStar(start_node, goal_node, "none", graph, weights)
    paths, visited_fore, visited_back = bastar.searching()

    if paths:
        print("All Paths:")
        for i, path in enumerate(paths):
            print(f"Path {i + 1}: {path}")
    else:
        print("No path found between", start_node, "and", goal_node)


if __name__ == '__main__':
    main()
