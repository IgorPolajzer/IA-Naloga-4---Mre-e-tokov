from main import ford_fulkerson
from utils import *
import time
import matplotlib.pyplot as plt


def test_time_vs_nodes(algorithm_func, algorithm_name):
    results = []

    for i in range(1, 6):
        graph, node_count, conn_count = parse_file(f"generated/generated_{i}.txt")
        node_count = int(node_count)
        conn_count = int(conn_count)

        times = []
        for j in range(10):
            start = time.time()
            max_flow, flows = ford_fulkerson(graph, 1, node_count, algorithm_func)
            times.append((time.time() - start) * 1000)

        results.append((node_count, min(times), sum(times) / len(times), max(times), conn_count))

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
    plt.savefig(f'time_vs_nodes_{algorithm_name.lower().replace(" ", "_").replace("-", "_")}.png', dpi=300,
                bbox_inches='tight')
    plt.show()


def test_time_vs_edges(algorithm_func, algorithm_name):
    results = []

    for i in range(6, 11):
        graph, node_count, conn_count = parse_file(f"generated/generated_{i}.txt")
        node_count = int(node_count)
        conn_count = int(conn_count)

        times = []
        for j in range(10):
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
    plt.savefig(f'time_vs_edges_{algorithm_name.lower().replace(" ", "_").replace("-", "_")}.png', dpi=300,
                bbox_inches='tight')
    plt.show()


def run_all_tests():
    test_time_vs_nodes(bfs, "Edmonds-Karp (BFS)")
    test_time_vs_nodes(dfs, "Ford-Fulkerson (DFS)")
    test_time_vs_edges(bfs, "Edmonds-Karp (BFS)")
    test_time_vs_edges(dfs, "Ford-Fulkerson (DFS)")


if __name__ == '__main__':
    run_all_tests()