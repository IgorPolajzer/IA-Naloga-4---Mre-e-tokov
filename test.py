from main import ford_fulkerson
from utils import *
import time
import matplotlib.pyplot as plt

NUMBER_OF_ITERATIONS = 10

def test_time_vs_nodes(algorithm_func, algorithm_name):
    results = []

    for i in range(1, 6):
        graph, node_count, conn_count = parse_file(f"generated/generated_{i}.txt")

        times = []
        for j in range(NUMBER_OF_ITERATIONS + 1):
            start = time.time()
            max_flow, flows = ford_fulkerson(graph, 1, node_count, algorithm_func)
            times.append((time.time() - start) * 1000)

        results.append((int(node_count), min(times), sum(times) / len(times), max(times)))

    results.sort(key=lambda x: x[0])

    nodes = [r[0] for r in results]
    min_times = [r[1] for r in results]
    avg_times = [r[2] for r in results]
    max_times = [r[3] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(nodes, min_times, 'b-o', linewidth=2, markersize=8, label='Minimalni čas')
    plt.plot(nodes, avg_times, 'g-o', linewidth=2, markersize=8, label='Povprečni čas')
    plt.plot(nodes, max_times, 'r-o', linewidth=2, markersize=8, label='Maksimalni čas')
    plt.xlabel('Število vozlišč', fontsize=12)
    plt.ylabel('Čas (ms)', fontsize=12)
    plt.title(f'Čas iskanja maksimalnega toka glede na število vozlišč ({algorithm_name})', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def test_time_vs_edges(algorithm_func, algorithm_name):
    results = []

    for i in range(6, 10):
        graph, node_count, conn_count = parse_file(f"generated/generated_{i}.txt")
        node_count = int(node_count)
        conn_count = int(conn_count)

        times = []
        for j in range(NUMBER_OF_ITERATIONS + 1):
            start = time.time()
            max_flow, flows = ford_fulkerson(graph, 1, node_count, algorithm_func)
            times.append((time.time() - start) * 1000)

        results.append((conn_count, min(times), sum(times) / len(times), max(times)))

    results.sort(key=lambda x: x[0])

    edges = [r[0] for r in results]
    min_times = [r[1] for r in results]
    avg_times = [r[2] for r in results]
    max_times = [r[3] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(edges, min_times, 'b-o', linewidth=2, markersize=8, label='Minimalni čas')
    plt.plot(edges, avg_times, 'g-o', linewidth=2, markersize=8, label='Povprečni čas')
    plt.plot(edges, max_times, 'r-o', linewidth=2, markersize=8, label='Maksimalni čas')
    plt.xlabel('Število povezav', fontsize=12)
    plt.ylabel('Čas (ms)', fontsize=12)
    plt.title(f'Čas iskanja maksimalnega toka glede na število povezav (30 vozlišč, {algorithm_name})', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def run_all_tests():
    test_time_vs_nodes(bfs, "Edmonds-Karp (BFS)")
    test_time_vs_nodes(dfs, "Ford-Fulkerson (DFS)")
    test_time_vs_edges(bfs, "Edmonds-Karp (BFS)")
    test_time_vs_edges(dfs, "Ford-Fulkerson (DFS)")


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
        f.write(f"{u} {max_edges}\n")
        for a, b, c in edges:
            f.write(f"{a} {b} {c}\n")


def generate_test_files():
    generated_file_name = input("File name: ")

    pairs = [
        (5, 20),  # full graph for 5 nodes
        (10, 90),  # full graph for 10 nodes
        (15, 210),  # full graph for 15 nodes
        (20, 380),  # full graph for 20 nodes
        (25, 600),  # full graph for 25 nodes
        (30, 100),  # sparse graph for 30 nodes
        (30, 250),
        (30, 500),
        (30, 700),
        (30, 870)  # full graph for 30 nodes
    ]

    for i in range (1, 11):
        for j, pair in enumerate(pairs, start=1):
            u, v = pair
            file_name = f"{generated_file_name}_{i}_{j}"
            generate_graph(int(u), int(v), file_name)


if __name__ == '__main__':
    run_all_tests()
    # generate_test_files()