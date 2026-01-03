from utils import *


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

    graph, _, _ = parse_file(file_name)

    print("Choose the search algorithm:")
    print("1 - Edmonds-Karp (BFS)")
    print("2 - Ford-Fulkerson (DFS)\n")
    algorithm = int(input("Choose the option: "))

    print("Please define the source and sink nodes:")
    print("(If not provided, the algorithm will attempt to define them automatically.)")
    s = input("Enter the source node: ").strip()
    t = input("Enter the sink node: ").strip()

    if s == "" or t == "":
        print("Source or sink node not provided. Defining them automatically...")
        s, t = find_s_t(graph)

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
    main()