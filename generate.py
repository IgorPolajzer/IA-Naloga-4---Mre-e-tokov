import random
import os


def generate_flow_network(num_nodes, num_edges, filename):
    """
    Generate a flow network graph suitable for max-flow testing.
    Ensures no direct edge from source (1) to sink (num_nodes).
    """
    if num_nodes < 3:
        raise ValueError("Need at least 3 nodes for meaningful flow network")

    max_possible_edges = num_nodes * (num_nodes - 1)
    if num_edges > max_possible_edges:
        raise ValueError(f"Too many edges requested. Max for {num_nodes} nodes is {max_possible_edges}")

    edges = set()
    source = 1
    sink = num_nodes

    # Step 1: Ensure connectivity from source to sink through middle nodes
    # Create a path from source through some middle nodes to sink
    middle_nodes = list(range(2, num_nodes))
    random.shuffle(middle_nodes)

    # Guarantee at least one path from source to sink
    path_length = min(3, len(middle_nodes))
    path_nodes = [source] + middle_nodes[:path_length] + [sink]

    for i in range(len(path_nodes) - 1):
        u, v = path_nodes[i], path_nodes[i + 1]
        capacity = random.randint(1, 20)
        edges.add((u, v, capacity))

    # Step 2: Add random edges, but NEVER direct source->sink edge
    attempts = 0
    max_attempts = num_edges * 10

    while len(edges) < num_edges and attempts < max_attempts:
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)

        # Skip if same node, or direct source->sink edge
        if u == v or (u == source and v == sink) or (u == sink and v == source):
            attempts += 1
            continue

        # Skip if reverse edge already exists (directed graph)
        if (v, u, capacity) in edges:
            attempts += 1
            continue

        capacity = random.randint(1, 20)
        edge = (u, v, capacity)

        if edge not in edges:
            edges.add(edge)

        attempts += 1

    # Step 3: Write to file
    edges_list = sorted(list(edges))

    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)

    with open(filename, 'w') as f:
        f.write(f"{num_nodes} {len(edges_list)}\n")
        for u, v, capacity in edges_list:
            f.write(f"{u} {v} {capacity}\n")

    print(f"Generated: {filename} ({num_nodes} nodes, {len(edges_list)} edges)")


def generate_all_test_files():
    """
    Generate all 10 test files:
    - Files 1-5: Complete graphs with increasing nodes
    - Files 6-10: Fixed 30 nodes with varying edge density
    """

    print("Generating test files...")
    print("=" * 80)

    # Files 1-5: Complete/dense graphs with different node counts
    configs_nodes = [
        (5, 20),  # 5 nodes, full graph (5*4 = 20 edges)
        (10, 90),  # 10 nodes, full graph (10*9 = 90 edges)
        (15, 210),  # 15 nodes, full graph (15*14 = 210 edges)
        (20, 380),  # 20 nodes, full graph (20*19 = 380 edges)
        (25, 600),  # 25 nodes, full graph (25*24 = 600 edges)
    ]

    for i, (nodes, edges) in enumerate(configs_nodes, 1):
        # For complete graphs, subtract 1 to avoid source->sink direct edge
        actual_edges = min(edges - 1, nodes * (nodes - 1) - 1)
        generate_flow_network(nodes, actual_edges, f"test_files/generated/generated_{i}.txt")

    print()

    # Files 6-10: Fixed 30 nodes with varying edge counts
    configs_edges = [
        (30, 100),  # sparse
        (30, 250),  # sparse
        (30, 500),  # medium density
        (30, 700),  # dense
        (30, 869),  # almost complete (30*29 = 870, minus source->sink)
    ]

    for i, (nodes, edges) in enumerate(configs_edges, 6):
        generate_flow_network(nodes, edges, f"test_files/generated/generated_{i}.txt")

    print()
    print("=" * 80)
    print("All test files generated successfully!")
    print("\nFiles 1-5: Different node counts (5, 10, 15, 20, 25 nodes)")
    print("Files 6-10: Fixed 30 nodes with varying edge density (100-869 edges)")


if __name__ == '__main__':
    generate_all_test_files()