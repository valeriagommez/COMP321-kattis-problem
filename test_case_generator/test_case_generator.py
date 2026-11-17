import random
from collections import defaultdict

# build adjacency map using the list of edges
def build_graph (edges) :
    graph = defaultdict(list)
    for source, dest in edges:
        graph[source].append(dest)

    graph = dict(graph)
    return graph


def topological_sort(edges) : 
    # build graph
    graph = build_graph(edges)
    visited = set()
    order = []

    def dfs(node, graph) :
        if node in visited : 
            return
        
        visited.add(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor, graph)
        order.append(node) 

    for node in graph.keys() : 
        dfs(node, graph)

    return order[::-1]

def create_input(directory, title, n, edges) : 
    # write input file
    input_file_path = "../data/" + directory + "/" +  title + ".in"
    with open(input_file_path, "w", encoding="utf-8") as file:
        file.write(f"{n} {len(edges)}\n")
        # print(edges)
        for edge in edges : 
            file.write(f"{edge[0]} {edge[1]}\n")

def create_output(directory, title, type, topological_order=None, added_edge=None) :
    output_file_path = "../data/" + directory + "/" +  title + ".ans"
    with open(output_file_path, "w", encoding="utf-8") as file:
        if type == "success" : 
            # print("hello")
            # print(" ".join(map(str, topological_order)))
            file.write(" ".join(map(str, topological_order)))

        elif type == "impossible" : 
            file.write("IMPOSSIBLE")

        elif type == "add_edge" : 
            file.write("POSSIBLE\n")
            file.write(f"{added_edge[0]} {added_edge[1]}")


def make_hamiltonian(n) : 
    # max num of edges in a DAG is (n * (n-1))//2
    max_edges = min((n * (n - 1)) // 2, 10**4 - 1 - n)

    # start by building the hamiltonian path
    topological_order = list(range(1, n+1))
    random.shuffle(topological_order)

    edges = set()
    hamiltonian_edges = []

    for i, curNode in enumerate(topological_order) : 
        if i != n-1 :
            curEdge = (curNode, topological_order[i + 1])
            edges.add(curEdge)
            hamiltonian_edges.append(curEdge)
    
    # add random forward edges to the graph (backwards create cycles)
    num_forward_edges = random.randint(n - 1, max_edges) - len(edges)

    possible_forward_edges = []
    for i in range(n) : 
        for j in range(i + 2, n) :
            possible_forward_edges.append((topological_order[i], topological_order[j]))

    edges.update(random.sample(possible_forward_edges, num_forward_edges))  # randomly choose edges

    sorted_edges = sorted(edges)
    return sorted_edges, topological_order, hamiltonian_edges


def make_cycle_in_hamiltonian(n) : 
    # make a graph with a hamiltonian path
    sorted_edges, topological_order, _ = make_hamiltonian(n)
    edge_set = set(sorted_edges)

    # adding a random backwards edge
    gap = random.randint(1, n - 1)
    i = random.randint(0, n - 1 - gap)
    j = random.randint(i + gap, n - 1)
    edge_set.add((topological_order[j], topological_order[i]))

    # print(sorted_edges)
    return sorted(edge_set)


def make_missing_edge(n) : 
    # make a graph with a hamiltonian path
    sorted_edges, _, hamiltonian_edges = make_hamiltonian(n)
    first_node = hamiltonian_edges[0][0]
    last_node = hamiltonian_edges[-1][1]

    # select random edge from hamiltonian to remove
    remove = random.randint(1, len(hamiltonian_edges) - 2)
    removed_edge = hamiltonian_edges[remove]
    removed_source, removed_dest = removed_edge

    edge_set = set(sorted_edges)
    edge_set.add((first_node, last_node))

    # make sure removed_source is a sink and removed_dest is a source (by removing edges)
    edge_set = [
        (u, v) for (u, v) in edge_set if u != removed_source and v != removed_dest
    ]

    return sorted(edge_set), removed_edge
    
def make_cycle_missing_edge(n):
    # make hamiltonian
    sorted_edges, order, hamiltonian_edges = make_hamiltonian(n)    
    first_node, last_node = order[0], order[-1]

    # choose random edge to get cut
    k = random.randint(1, len(hamiltonian_edges) - 2)               
    removed_edge = hamiltonian_edges[k]
    removed_source, removed_dest = removed_edge

    edge_set = set(sorted_edges)
    edge_set.add((first_node, last_node))
    edge_set = {
        (u, v) for (u, v) in edge_set if u != removed_source and v != removed_dest
    }

    # picking a side of the graph and two random vertices on it
    left = list(range(0, k + 1))
    right = list(range(k + 1, n))
    side = random.choices([left, right])[0]

    # adding backwards edge
    i, j = sorted(random.sample(side, 2))
    edge_set.add((order[j], order[i]))             

    return sorted(edge_set), removed_edge


def make_multi_missing_edges(n):
    sorted_edges, _, hamiltonian_edges = make_hamiltonian(n)

    # number of "cuts" made to the graph (2 is enough to show that more than 1 edge is missing)
    cuts = random.sample(range(len(hamiltonian_edges)), 2)
    removed_sources = {hamiltonian_edges[k][0] for k in cuts}
    removed_dests = {hamiltonian_edges[k][1] for k in cuts}

    edge_set = {
        (u, v) for (u, v) in sorted_edges if (u not in removed_sources) and (v not in removed_dests)
    }

    return sorted(edge_set), [hamiltonian_edges[k] for k in cuts]

if __name__ == "__main__" : 
    #### for the 'sample' test cases (3 total) :
    # 1 test case : successful hamiltonian path
    sorted_edges, topological_order, _ = make_hamiltonian(7)
    create_input("sample", "sample_success", 7, sorted_edges)
    create_output("sample", "sample_success", "success", topological_order)

    # 1 test case : graph with a cycle ("IMPOSSIBLE")
    # sorted_edges = make_cycle_in_hamiltonian(5)
    # create_input("sample", "sample_cycle", 5, sorted_edges)
    # create_output("sample", "sample_cycle", "impossible")

    # 1 test case : 1 edge away from a hamiltonian path  ("POSSIBLE" + missing edge)
    # sorted_edges, removed_edge = make_missing_edge(5)
    # create_input("sample", "sample_added_edge", 5, sorted_edges)
    # create_output("sample", "sample_added_edge", "add_edge", None, removed_edge)

    #### for the 'secret' test cases (20 total) : 
    # TLE / large inputs :
    # sorted_edges, topological_order, _ = make_hamiltonian(120)
    # create_input("secret", "tle_success", 120, sorted_edges)
    # create_output("secret", "tle_success", "success", topological_order, added_edge=None)

    # sorted_edges = make_cycle_in_hamiltonian(120)
    # create_input("secret", "tle_cycle_1", 120, sorted_edges)
    # create_output("secret", "tle_cycle_1", "impossible")

    # sorted_edges, removed_edge = make_missing_edge(120)
    # create_input("secret", "tle_added_edge", 120, sorted_edges)
    # create_output("secret", "tle_added_edge", "add_edge", None, removed_edge)

    # sorted_edges, _ = make_cycle_missing_edge(120)
    # create_input("secret", "tle_cycle_2", 120, sorted_edges)
    # create_output("secret", "tle_cycle_2", "impossible")

    # sorted_edges, _ = make_multi_missing_edges(120)
    # create_input("secret", "tle_multiple_missing", 120, sorted_edges)
    # create_output("secret", "tle_multiple_missing", "impossible")

    # node_number = [25, 50]
    # for node in node_number : 
    #     sorted_edges, topological_order, _ = make_hamiltonian(node)
    #     name = f"success_{node}"
    #     create_input("secret", name, node, sorted_edges)
    #     create_output("secret", name, "success", topological_order, added_edge=None)

    # for node in node_number : 
    #     sorted_edges = make_cycle_in_hamiltonian(node)
    #     name = f"cycle_{node}"
    #     create_input("secret", name, node, sorted_edges)
    #     create_output("secret", name, "impossible")

    # for node in node_number : 
    #     sorted_edges, removed_edge = make_missing_edge(node)
    #     name = f"missing_edge_{node}"
    #     create_input("secret", name, node, sorted_edges)
    #     create_output("secret", name, "add_edge", None, removed_edge)

    # for node in node_number : 
    #     sorted_edges, _ = make_multi_missing_edges(node)
    #     name = f"multiple_missing_{node}"
    #     create_input("secret", name, node, sorted_edges)
    #     create_output("secret", name, "impossible")

    # for node in node_number : 
    #     sorted_edges, _ = make_cycle_missing_edge(node)
    #     name = f"cycle_missing_edge_{node}"
    #     create_input("secret", name, node, sorted_edges)
    #     create_output("secret", name, "impossible")
    