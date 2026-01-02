from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum


class NodeStatus(Enum):
    WHITE = 0,
    GRAY = 1,
    BLACK = 2


@dataclass
class Node:
    predecessor: str | None
    length: int
    status: NodeStatus
    index: int = field(init=False)
    name: str

    _counter: int = 0  # Class-level variable to track the index

    def __post_init__(self):
        self.index = Node._counter
        Node._counter += 1


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


def get_cf(graph, flows, p):
    cf = float('inf')
    for i in range(len(p)-1):
        u = p[i]
        v = p[i+1]
        residual = graph[u][v] - flows[u][v]

        if residual < cf:
            cf = residual

    return cf


def get_nodes_from_graph(graph, s):
    nodes = {}

    for u in graph:
        if u not in nodes and u != s:
            nodes[u] = Node(None, -1, NodeStatus.WHITE, u)

        for v in graph[u]:
            if v not in nodes and v != s:
                nodes[v] = Node(None, -1, NodeStatus.WHITE, v)

    return nodes


def get_path(nodes, s, t):
    path = []

    if s == t:
        path.append(t)
    elif nodes[t].predecessor is not None:
        path += get_path(nodes, s, nodes[t].predecessor)
        path.append(nodes[t].name)

    return path


def bfs(graph, flows, s, t):
    nodes = get_nodes_from_graph(graph, s)

    queue = deque()

    nodes[s] = Node(None, 0, NodeStatus.GRAY, s)
    queue.append(nodes[s])

    while queue:
        u = queue.popleft()
        u.status = NodeStatus.BLACK

        if u.name == t:
            return get_path(nodes, s, t)

        # neighbours from v.
        for v in graph[u.name]:
            if nodes[v].status == NodeStatus.WHITE and (graph[u.name][v] - flows[u.name][v]) > 0:
                nodes[v].predecessor = u.name
                nodes[v].length = nodes[u.name].length + 1
                nodes[v].status = NodeStatus.GRAY
                queue.append(nodes[v])

    return None


def edmonds_karp(graph, s, t):
    max_flow = 0
    flows = defaultdict(dict)
    for u in graph:
        for v in graph[u]:
            flows[u][v] = 0
            flows[v][u] = 0

    p = bfs(graph, flows, s, t)
    while p is not None:
        print(p)
        cf_p = get_cf(graph, flows, p)

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
    file_name = "vhod.txt"

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
