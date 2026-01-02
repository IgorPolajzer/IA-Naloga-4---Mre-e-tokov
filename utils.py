import os
import random
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum

import graphviz


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

    if len(sources) < 1 and len(sinks) < 1:
        raise Exception("Couldnt find any sources/sinks.")

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

    if sum(len(neighbors) for neighbors in graph.values()) != int(conn_count):
        raise Exception("The number of parsed connections does not match the provided connection count.")

    return graph, node_count, conn_count


def get_cf(graph, flows, p):
    cf = float('inf')
    for i in range(len(p) - 1):
        u = p[i]
        v = p[i + 1]
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


def print_solution(graph, flows, max_flow, s, t, file_name):
    print("Result: ")
    for u, val in graph.items():
        for v in graph[u]:
            print(f"({u},{v})[{flows[u][v]}/{graph[u][v]}]")

    print(f"\nmax. tok:  {max_flow}")

    draw_graph(graph, f"{file_name}_result_graph", s, t, flows)


def draw_graph(graph, graph_name, s, t, flows=None):
    if flows is None:
        flows = defaultdict(lambda: defaultdict(int))

    dot = graphviz.Digraph(comment=graph_name)

    dot.node(s, style="filled", fillcolor="green")
    dot.node(t, style="filled", fillcolor="red")

    for u in graph:
        for v in graph[u]:
            max_weight = 0 if graph[u][v] < 0 else graph[u][v]
            remaining_weight = 0 if flows[u][v] < 0 else flows[u][v]
            dot.edge(u, v, label=f"[{remaining_weight}/{max_weight}]")

    dot.render(f'graphs/{graph_name}.gv').replace('\\', '/')


def bfs(graph, flows, s, t):
    nodes = get_nodes_from_graph(graph, s)

    queue = deque()

    nodes[s] = Node(None, 0, NodeStatus.GRAY, s)
    queue.append(nodes[s])

    while queue:
        u = queue.popleft()

        if u.name == t:
            return get_path(nodes, s, t)

        # neighbours from v.
        for v in graph[u.name]:
            if nodes[v].status == NodeStatus.WHITE and (graph[u.name][v] - flows[u.name][v]) > 0:
                nodes[v].predecessor = u.name
                nodes[v].length = nodes[u.name].length + 1
                nodes[v].status = NodeStatus.GRAY
                queue.append(nodes[v])
        u.status = NodeStatus.BLACK

    return None


def dfs(graph, flows, s, t):
    nodes = get_nodes_from_graph(graph, s)

    stack = []

    nodes[s] = Node(None, 0, NodeStatus.GRAY, s)
    stack.append(nodes[s])

    while stack:
        u = stack.pop()

        if u.name == t:
            return get_path(nodes, s, t)

        # neighbours from v.
        for v in graph[u.name]:
            if nodes[v].status == NodeStatus.WHITE and (graph[u.name][v] - flows[u.name][v]) > 0:
                nodes[v].predecessor = u.name
                nodes[v].length = nodes[u.name].length + 1
                nodes[v].status = NodeStatus.GRAY
                stack.append(nodes[v])
        u.status = NodeStatus.BLACK

    return None


# u = input("Node number: ")
# v = input("Connection number: ")
# generated_file_name = input("File name: ")
# generate_graph(int(u), int(v), generated_file_name)
#
# pairs = [
#     (5, 20),  # full graph for 5 nodes
#     (10, 90),  # full graph for 10 nodes
#     (15, 210),  # full graph for 15 nodes
#     (20, 380),  # full graph for 20 nodes
#     (25, 600),  # full graph for 25 nodes
#     (30, 100),  # sparse graph for 30 nodes
#     (30, 250),
#     (30, 500),
#     (30, 700),
#     (30, 870)  # full graph for 30 nodes
# ]
#
# for i, pair in enumerate(pairs, start=1):
#     u, v = pair
#     file_name = f"{generated_file_name}_{i}"
#     generate_graph(int(u), int(v), file_name)
def generate_graph(u, v, file_name, max_capacity=20):
    max_edges = u*(u-1)
    if v > max_edges:
        raise ValueError("Too many edges for a simple directed graph.")

    nodes = list(range(1, u+1))
    all_possible_edges = [(a, b) for a in nodes for b in nodes if a != b]

    # Shuffle edges
    random.shuffle(all_possible_edges)

    edges = []
    for i, (a, b) in enumerate(all_possible_edges):
        if i < v:
            capacity = random.randint(1, max_capacity)  # active edge
        else:
            capacity = 0  # zero-capacity edge
        edges.append((a, b, capacity))

    # Save to file
    os.makedirs("test_files/generated", exist_ok=True)
    file_path = f"test_files/generated/{file_name}.txt"
    with open(file_path, "w") as f:
        f.write(f"{u} {max_edges}\n")  # total edges = u*(u-1)
        for a, b, c in edges:
            f.write(f"{a} {b} {c}\n")
