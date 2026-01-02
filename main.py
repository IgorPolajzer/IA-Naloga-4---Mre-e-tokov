from utils import *
import time
import matplotlib.pyplot as plt


def test():
    times = {}
    node_counts = {}

    for i in range(1, 5):
        graph, node_count, conn_count = parse_file(f"generated/generated_{i}.txt")

        iterations = 10
        time_sum = 0
        for j in range(1, iterations):
            start = time.time()
            max_flow, flows = ford_fulkerson(graph, 1, node_count, bfs)
            time_sum += time.time() - start

        avg_time = time_sum / iterations
        times[node_count] = avg_time * 1000  # [ms]
        node_counts[node_count] = conn_count

    plt.figure(figsize=(10, 6))
    plt.plot(times.keys(), times.values(), 'g-o', linewidth=2, markersize=8, label='Ford-Fulkerson')

    plt.xlabel('Število vozlišč', fontsize=12)
    plt.ylabel('Čas (ms)', fontsize=12)
    plt.title('Čas iskanja maksimalnega toka glede na število vozlišč', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig('time_based_on_node_count.png', dpi=300, bbox_inches='tight')
    plt.show()


def ford_fulkerson(graph, s, t, algorithm):
    max_flow = 0
    flows = defaultdict(dict)
    for u in graph:
        for v in graph[u]:
            flows[u][v] = 0
            flows[v][u] = 0

    p = algorithm(graph, flows, s, t)
    while p is not None:
        cf_p = get_cf(graph, flows, p)

        for i in range(len(p) - 1):
            u = p[i]
            v = p[i + 1]
            flows[u][v] += cf_p
            flows[v][u] -= cf_p

        max_flow += cf_p
        p = bfs(graph, flows, s, t)

    return max_flow, flows


def main():
    print("Ford–Fulkerson algorithm")
    print(100 * "=")
    file_name = input("Provide the input file name (should be inside /test_files):")
    # file_name = "vhod.txt"

    graph = parse_file(file_name)

    print("Choose the search algorithm:")
    print("1 - Edmonds-Karp (BFS)")
    print("2 - Ford-Fulkerson (DFS)\n")
    # algorithm = input("Choose the option: ")

    print("Please define the source and sink nodes:")
    print("(If not provided, the algorithm will attempt to define them automatically.)")
    s = input("Enter the source node: ").strip()
    t = input("Enter the sink node: ").strip()

    if s == "" or t == "":
        print("Source or sink node not provided. Defining them automatically...")
        s, t = find_s_t(graph)

    algorithm = 3
    print(100 * "=")

    if algorithm == 1:
        draw_graph(graph, file_name, s, t)
        max_flow, flows = ford_fulkerson(graph, s, t, bfs)
        print_solution(graph, flows, max_flow, s, t, file_name)
    elif algorithm == 2:
        draw_graph(graph, file_name, s, t)
        max_flow, flows = ford_fulkerson(graph, s, t, dfs)
        print_solution(graph, flows, max_flow, s, t, file_name)
    else:
        print("Invalid algorithm choice")


if __name__ == '__main__':
    # main()
    test()
