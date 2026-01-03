from main import ford_fulkerson
from utils import *
import time
import matplotlib.pyplot as plt

NUMBER_OF_ITERATIONS = 10


def test_time_vs_nodes(algorithm_func, algorithm_name):
    global node_count
    results = []

    for i in range(1, 6):
        times_for_dimension = []

        for j in range(1, 11):
            graph, node_count, conn_count = parse_file(f"generated/generated_{j}_{i}.txt")

            times = []
            for x in range(NUMBER_OF_ITERATIONS):
                start = time.time()
                ford_fulkerson(graph, 1, node_count, algorithm_func)
                times.append((time.time() - start) * 1000)

            times_for_dimension.append(sum(times)/len(times))

        results.append((
            int(node_count),
            min(times_for_dimension),
            sum(times_for_dimension) / len(times_for_dimension),
            max(times_for_dimension)
        ))

    nodes = [dim[0] for dim in results]
    min_times = [dim[1] for dim in results]
    avg_times = [dim[2] for dim in results]
    max_times = [dim[3] for dim in results]

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
    global conn_count
    results = []

    for i in range(1, 6):
        times_for_dimension = []

        for j in range(1, 11):
            graph, node_count, conn_count = parse_file(f"generated/generated_{j}_{i}.txt")

            times = []
            for x in range(NUMBER_OF_ITERATIONS):
                start = time.time()
                ford_fulkerson(graph, 1, node_count, algorithm_func)
                times.append((time.time() - start) * 1000)

            times_for_dimension.append(sum(times)/len(times))

        results.append((
            int(conn_count),
            min(times_for_dimension),
            sum(times_for_dimension) / len(times_for_dimension),
            max(times_for_dimension)
        ))

    edges = [dim[0] for dim in results]
    min_times = [dim[1] for dim in results]
    avg_times = [dim[2] for dim in results]
    max_times = [dim[3] for dim in results]

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
        # Full graphs
        (5, 20),
        (10, 90),
        (15, 210),
        (20, 380),
        (25, 600),
        # sparse graphs
        (30, 100),
        (30, 250),
        (30, 500),
        (30, 700),
        (30, 870)
    ]

    for i in range (1, 11):
        for j, pair in enumerate(pairs, start=1):
            u, v = pair
            file_name = f"{generated_file_name}_{i}_{j}"
            generate_graph(int(u), int(v), file_name)


if __name__ == '__main__':
    run_all_tests()
    # generate_test_files()