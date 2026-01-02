from dataclasses import dataclass
from collections import defaultdict
from enum import Enum


@dataclass
class Node:
    predecessor: int
    length: int
    status: int
    index: int
    name: str


class NodeState(Enum):
    WHITE = 0,
    GRAY = 1,
    BLACK = 2


# s => in=0, out>0; t => in>0, out=0
def find_s_t(graph):
    in_deg = defaultdict(int)
    out_deg = defaultdict(int)

    for u in graph:
        for v in graph[u]:
            out_deg[u] += 1
            in_deg[v] += 1

    sources = [u for u in out_deg if in_deg[u] == 0 and out_deg[u] > 0]
    sinks = [u for u in in_deg if out_deg[u] == 0 and in_deg[u] > 0]

    if len(sources) != 1 and len(sinks) != 1:
        raise Exception("To many sources/sinks found.")

    return sources[0], sinks[0]


def parse_file(file_name):
    graph = defaultdict(dict)
    file = open("test_files/" + file_name)

    node_count, conn_count = None, None
    for line in file:
        # First line processing.
        if node_count is None or conn_count is None:
            node_count, conn_count = line.strip().split(" ")
            continue

        u, v, c = line.strip().split(" ")
        graph[u][v] = c

    if sum(len(neighbors) for neighbors in graph.values()) is not int(conn_count):
        raise Exception("The number of parsed connections does not match the provided connection count.")

    return graph, *find_s_t(graph)


def bfs(graph, s, t):
    visited = {v: False for u in graph for v in graph[u]}


    # Create a queue for BFS
    queue = []

    # Mark the source node as
    # visited and enqueue it
    queue.append(s)
    visited[s] = True

    while queue:

        # Dequeue a vertex from
        # queue and print it
        s = queue.pop(0)
        print(s, end="->")

        # Get all adjacent vertices of the
        # dequeued vertex s.
        # If an adjacent has not been visited,
        # then mark it visited and enqueue it
        for i in graph[s]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True

def edmonds_karp(graph, s, t):
    max_flow = 0

    flows = {u: {v: 0 for v in graph[u]} for u in graph}

    while bfs(graph, s, t):
        pass

def main():
    print("Ford–Fulkerson algorithm")
    print(100 * "=")
    # file_name = input("Provide the input file name (should be inside /test_files):")
    file_name = "primerZaZagovor2.txt"

    graph, s, t = parse_file(file_name)

    print(graph)

    print("Choose the search algorithm:")
    print("Edmonds-Karp(BFS) -> 1")
    print("Ford Fulkerson(DFS) -> 2")

    # algorithm = input("Choose the option: ")
    algorithm = 1

    if algorithm is 1:
        edmonds_karp(graph, s, t)
    elif algorithm is 2:
        pass
    else:
        print("Invalid algorithm choice")


if __name__ == '__main__':
    main()
