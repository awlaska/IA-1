#TODO ValueError: could not convert string to float: 'distancia'

import csv
import heapq
import math


def load_graph_from_csv(file_path):
    graph = {}

    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            node1, node2, cost = row[0], row[1], float(row[2])

            if node1 not in graph:
                graph[node1] = []
            if node2 not in graph:
                graph[node2] = []

            graph[node1].append((node2, cost))
            graph[node2].append((node1, cost))

    return graph


class BidirectionalAStarGraph:
    def __init__(self, graph, start, goal, heuristic_type="euclidean"):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.heuristic_type = heuristic_type

        self.open_fwd = []
        self.open_bwd = []
        self.closed_fwd = set()
        self.closed_bwd = set()
        self.g_fwd = {start: 0}
        self.g_bwd = {goal: 0}
        self.parents_fwd = {start: None}
        self.parents_bwd = {goal: None}

        heapq.heappush(self.open_fwd, (self.h(start, goal), start))
        heapq.heappush(self.open_bwd, (self.h(goal, start), goal))

    def h(self, node1, node2):
        return 0

    def search(self):
        meeting_point = None

        while self.open_fwd and self.open_bwd:
            if self.expand_front():
                meeting_point = self.open_fwd[0][1]
                break
            if self.expand_back():
                meeting_point = self.open_bwd[0][1]
                break

        return self.extract_path(meeting_point), self.g_fwd.get(meeting_point, float('inf')) + self.g_bwd.get(
            meeting_point, float('inf'))

    def expand_front(self):
        if not self.open_fwd:
            return False

        _, current = heapq.heappop(self.open_fwd)
        if current in self.closed_bwd:
            return True

        self.closed_fwd.add(current)

        for neighbor, cost in self.graph.get(current, []):
            new_cost = self.g_fwd[current] + cost
            if neighbor not in self.g_fwd or new_cost < self.g_fwd[neighbor]:
                self.g_fwd[neighbor] = new_cost
                self.parents_fwd[neighbor] = current
                heapq.heappush(self.open_fwd, (new_cost + self.h(neighbor, self.goal), neighbor))

        return False

    def expand_back(self):
        if not self.open_bwd:
            return False

        _, current = heapq.heappop(self.open_bwd)
        if current in self.closed_fwd:
            return True

        self.closed_bwd.add(current)

        for neighbor, cost in self.graph.get(current, []):
            new_cost = self.g_bwd[current] + cost
            if neighbor not in self.g_bwd or new_cost < self.g_bwd[neighbor]:
                self.g_bwd[neighbor] = new_cost
                self.parents_bwd[neighbor] = current
                heapq.heappush(self.open_bwd, (new_cost + self.h(neighbor, self.start), neighbor))

        return False

    def extract_path(self, meeting_point):
        if meeting_point is None:
            return []  # No path found

        path_fwd = []
        node = meeting_point
        while node:
            path_fwd.append(node)
            node = self.parents_fwd.get(node)
        path_fwd.reverse()

        path_bwd = []
        node = self.parents_bwd.get(meeting_point)
        while node:
            path_bwd.append(node)
            node = self.parents_bwd.get(node)

        return path_fwd + path_bwd


if __name__ == "__main__":
    graph = load_graph_from_csv("../graph.csv")
    start, goal = "A", "H"

    bi_astar = BidirectionalAStarGraph(graph, start, goal)
    path, cost = bi_astar.search()

    print("Shortest path:", " -> ".join(path))
    print("Total cost:", cost)
