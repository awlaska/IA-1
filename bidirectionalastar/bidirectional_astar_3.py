import os
import sys
import math
import heapq
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + 
                "/../../bidirectionalastar/")

from bidirectionalastar import plotting, env

class BidirectionalAStar:
    def __init__(self, s_start, s_goal, heuristic_type, graph, weights):
        self.s_start = s_start
        self.s_goal = s_goal
        self.heuristic_type = heuristic_type
        self.graph = graph  # adjacency list representation of graph
        self.weights = weights  # Weights for kms, litros, and minutos
        
        self.OPEN_fore = []
        self.OPEN_back = []
        self.CLOSED_fore = []
        self.CLOSED_back = []
        self.PARENT_fore = dict()
        self.PARENT_back = dict()
        self.g_fore = dict()
        self.g_back = dict()

    def init(self):
        self.g_fore[self.s_start] = 0.0
        self.g_fore[self.s_goal] = math.inf
        self.g_back[self.s_goal] = 0.0
        self.g_back[self.s_start] = math.inf
        self.PARENT_fore[self.s_start] = self.s_start
        self.PARENT_back[self.s_goal] = self.s_goal
        heapq.heappush(self.OPEN_fore, (self.f_value_fore(self.s_start), self.s_start))
        heapq.heappush(self.OPEN_back, (self.f_value_back(self.s_goal), self.s_goal))

    def searching(self):
        self.init()
        s_meet = self.s_start

        while self.OPEN_fore and self.OPEN_back:
            _, s_fore = heapq.heappop(self.OPEN_fore)

            if s_fore in self.PARENT_back:
                s_meet = s_fore
                break

            self.CLOSED_fore.append(s_fore)

            for s_n in self.get_neighbors(s_fore):
                new_cost = self.g_fore[s_fore] + self.cost(s_fore, s_n)

                if s_n not in self.g_fore or new_cost < self.g_fore[s_n]:
                    self.g_fore[s_n] = new_cost
                    self.PARENT_fore[s_n] = s_fore
                    heapq.heappush(self.OPEN_fore, (self.f_value_fore(s_n), s_n))

            _, s_back = heapq.heappop(self.OPEN_back)

            if s_back in self.PARENT_fore:
                s_meet = s_back
                break

            self.CLOSED_back.append(s_back)

            for s_n in self.get_neighbors(s_back):
                new_cost = self.g_back[s_back] + self.cost(s_back, s_n)

                if s_n not in self.g_back or new_cost < self.g_back[s_n]:
                    self.g_back[s_n] = new_cost
                    self.PARENT_back[s_n] = s_back
                    heapq.heappush(self.OPEN_back, (self.f_value_back(s_n), s_n))

        return self.extract_path(s_meet), self.CLOSED_fore, self.CLOSED_back

    def get_neighbors(self, s):
        return self.graph.get(s, {}).keys()

    def extract_path(self, s_meet):
        path_fore = [s_meet]
        s = s_meet
        while s != self.s_start:
            s = self.PARENT_fore[s]
            path_fore.append(s)
        
        path_back = []
        s = s_meet
        while s != self.s_goal:
            s = self.PARENT_back[s]
            path_back.append(s)
        
        return list(reversed(path_fore)) + list(path_back)

    def f_value_fore(self, s):
        return self.g_fore[s] + self.h(s, self.s_goal)

    def f_value_back(self, s):
        return self.g_back[s] + self.h(s, self.s_start)

    def h(self, s, goal):
        return 0  # No heuristic (Dijkstra-like behavior)

    def cost(self, s_start, s_goal):
        edge = self.graph[s_start][s_goal]
        return (self.weights['kms'] * edge['kms'] +
                self.weights['litros'] * edge['litros'] +
                self.weights['minutos'] * edge['minutos'])


def main():
    df = pd.read_csv("data.csv")
    graph = {}

    for _, row in df.iterrows():
        start, end = row["start"], row["end"]
        if start not in graph:
            graph[start] = {}
        graph[start][end] = {"kms": row["kms"], "litros": row["litros"], "minutos": row["minutos"]}

    start_node = "A"  # Example starting node
    goal_node = "Z"  # Example goal node
    weights = {"kms": 1.0, "litros": 1.0, "minutos": 1.0}  # Adjust weights as needed
    
    bastar = BidirectionalAStar(start_node, goal_node, "none", graph, weights)
    path, visited_fore, visited_back = bastar.searching()
    
    print("Optimal path:", path)
    
    result_df = pd.DataFrame({"path": [path]})
    result_df.to_csv("results.csv", index=False)
    print("Results saved to results.csv")

if __name__ == '__main__':
    main()
