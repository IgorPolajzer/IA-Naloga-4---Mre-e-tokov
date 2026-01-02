from dataclasses import dataclass
from collections import defaultdict
from enum import Enum


class NodeState(Enum):
    WHITE = 0,
    GRAY = 1,
    BLACK = 2


@dataclass
class Node:
    predecessor: int
    length: int
    status: NodeState
    index: int
    name: str



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
        graph[u][v] = int(c)

    if sum(len(neighbors) for neighbors in graph.values()) is not int(conn_count):
        raise Exception("The number of parsed connections does not match the provided connection count.")

    return graph, *find_s_t(graph)


def get_cf(graph, p):
    full_path_weights = []
    for u in p:
        path_weight_sum = 0
        for v in graph[u]:
            path_weight_sum += graph[u][v]
        full_path_weights.append(path_weight_sum)

    return min(full_path_weights)


def bfs(graph, flows, s, t):
    visited = {v: False for u in graph for v in graph[u]}

    queue = []
    path = []

    queue.append(s)
    visited[s] = True

    while queue:

        u = queue.pop(0)
        path.append(u)
        # print(u, end="->")

        for v in graph[u]:
            if not visited[v] and (graph[u][v] - flows[u][v]) > 0:
                queue.append(v)
                visited[v] = True

    return path


def edmonds_karp(graph, s, t):
    max_flow = 0
    flows = defaultdict(dict)
    for u in graph:
        for v in graph[u]:
            flows[u][v] = 0
            flows[v][u] = 0

    p = bfs(graph, flows, s, t)
    while p:
        print(p)
        cf_p = get_cf(graph, p)

        for i in range(len(p) - 1):
            u = p[i]
            v = p[i + 1]
            flows[u][v] += cf_p
            flows[v][u] -= cf_p

        max_flow += cf_p
        p = bfs(graph, flows, s, t)

    return max_flow


def main():
    print("Ford–Fulkerson algorithm")
    print(100 * "=")
    # file_name = input("Provide the input file name (should be inside /test_files):")
    file_name = "primerZaZagovor2.txt"

    graph, s, t = parse_file(file_name)

    print("Choose the search algorithm:")
    print("Edmonds-Karp(BFS) -> 1")
    print("Ford Fulkerson(DFS) -> 2")

    # algorithm = input("Choose the option: ")
    algorithm = 1

    if algorithm == 1:
        edmonds_karp(graph, s, t)
    elif algorithm == 2:
        pass
    else:
        print("Invalid algorithm choice")


if __name__ == '__main__':
    main()
