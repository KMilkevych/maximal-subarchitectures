import networkx as nx
from typing import Iterable
from lib.archlogging import Logger, DummyLogger
from lib.kcongraph.consubgraph import size_k_connected_subgraphs_tree

logger = DummyLogger()

# Utility function for logging progress
def enable_logger(architecture, qubits):
    global logger
    logger = Logger(architecture, qubits)


# Utility functions for hashing graphs with specific number of iterations
def hash_it(G: nx.Graph) -> int:
    return 8


def hash_graph(G: nx.Graph) -> str:
    return nx.weisfeiler_lehman_graph_hash(G, iterations=hash_it(G))


def size_k_subgraphs(G: nx.Graph, k: int) -> Iterable[nx.Graph]:

    # Compute all connected sub-graphs of size k
    subgraphs = bf_connected_subgraphs(G, k)  # need to be all edges config
    # subgraphs = size_k_connected_subgraphs_tree(G, k)

    return subgraphs


def size_k_non_isomorphic_subgraphs(G: nx.Graph, k: int) -> Iterable[nx.Graph]:

    # Compute all subgraphs of size k
    subgraphs = bf_connected_subgraphs(G, k)  # need to be all edges config
    # subgraphs = size_k_connected_subgraphs_tree(G, k)

    # Compute all non-isomorphic of those
    non_isomorphic_subgraphs = non_isomorphic_graphs_hash(subgraphs)

    return non_isomorphic_subgraphs


def size_k_induced_non_isomorphic_subgraphs(G: nx.Graph, k: int) -> Iterable[nx.Graph]:

    # Compute all induced subgraphs of size k
    # subgraphs = size_k_non_isomorphic_subgraphs(G, k)
    subgraphs = size_k_induced_connected_subgraphs(G, k)

    # Compute all non-isomorphic of those
    non_isomorphic_subgraphs = non_isomorphic_graphs_hash(subgraphs)

    return non_isomorphic_subgraphs


def size_k_induced_connected_subgraphs(G: nx.Graph, k: int) -> Iterable[nx.Graph]:

    global logger

    logger.pre_start_induced_connected_subgraphs()

    # Compute all configurations of nodes
    configs: Iterable[Iterable[int]] = size_k_connected_subgraphs_tree(G, k)

    logger.start_induced_connected_subgraphs(len(configs))

    # Extract all subgraphs
    subgraphs: Iterable[nx.Graph] = []
    for idx, config in enumerate(configs):
        logger.update_induced_connected_subgraphs(idx + 1)
        g = nx.Graph(nx.induced_subgraph(G, config))
        subgraphs.append(g)

    # Return found subgraphs
    return subgraphs


def count_size_k_induced_connected_subgraphs_tree(G: nx.Graph, k: int) -> int:
    configs: Iterable[Iterable[int]] = size_k_connected_subgraphs_tree(G, k)
    return len(configs)


def count_size_k_induced_connected_subgraphs_bf(G: nx.Graph, k: int) -> int:
    global logger

    # Resulting iterable
    subgraph_count = 0

    # Import useful tool
    from itertools import combinations

    # Enumerate all subsets of k vertices
    combs = list(combinations(G.nodes, k))

    # Log progress
    logger.start_induced_connected_subgraphs(len(combs))

    # Perform enumeration
    for idx, combination in enumerate(combs):

        # Log progress
        logger.update_induced_connected_subgraphs(idx + 1)

        # Generate subgraph
        subgraph = nx.induced_subgraph(G, combination)

        # Check if subgraph is connected
        if nx.is_connected(subgraph):
            subgraph_count += 1

    # Return generated subgraphs
    return subgraph_count


def size_k_induced_connected_subgraphs_ram(G: nx.Graph, k: int) -> Iterable[nx.Graph]:

    global logger
    logger.pre_start_induced_connected_subgraphs()

    # Compute all configurations of nodes
    configs: Iterable[Iterable[int]] = size_k_connected_subgraphs_tree(G, k)

    logger.start_induced_connected_subgraphs(len(configs))

    # Extract all subgraphs with hashing to avoid isomorphisms
    hashes: set[str] = set()
    subgraphs: Iterable[nx.Graph] = []
    for idx, config in enumerate(configs):
        logger.update_induced_connected_subgraphs(idx + 1)
        g = nx.Graph(nx.induced_subgraph(G, config))
        g_h = hash_graph(g)

        if g_h not in hashes:
            hashes.add(g_h)
            subgraphs.append(g)

    # Return found subgraphs
    return subgraphs



def bf_induced_connected_subgraphs(G: nx.Graph, k: int) -> Iterable[nx.Graph]:
    """
    Computes all connected, induced subgraphs.
    """
    global logger

    # Resulting iterable
    subgraphs: Iterable[nx.Graph] = []

    # Import useful tool
    from itertools import combinations

    # Enumerate all subsets of k vertices
    combs = list(combinations(G.nodes, k))

    # Log progress
    logger.start_induced_connected_subgraphs(len(combs))

    # Perform enumeration
    for idx, combination in enumerate(combs):

        # Log progress
        logger.update_induced_connected_subgraphs(idx + 1)

        # Generate subgraph
        subgraph = nx.induced_subgraph(G, combination)

        # Check if subgraph is connected
        if nx.is_connected(subgraph):
            g = nx.Graph(subgraph)
            subgraphs.append(g)

    # Return generated subgraphs
    return subgraphs



def bf_induced_connected_subgraphs_ram(G: nx.Graph, k: int) -> Iterable[nx.Graph]:
    """
    Computes all connected, induced subgraphs.
    """
    global logger

    # Resulting iterable
    subgraphs: Iterable[nx.Graph] = []
    hashes: set[str] = set()

    # Import useful tool
    from itertools import combinations

    # Enumerate all subsets of k vertices
    combs = list(combinations(G.nodes, k))

    # Log progress
    logger.start_induced_connected_subgraphs(len(combs))

    # Perform enumeration
    for idx, combination in enumerate(combs):

        # Log progress
        logger.update_induced_connected_subgraphs(idx + 1)

        # Generate subgraph
        subgraph = nx.induced_subgraph(G, combination)
        g_hash = hash_graph(subgraph)

        # Check if subgraph is connected
        if nx.is_connected(subgraph) and g_hash not in hashes:
            g = nx.Graph(subgraph)
            subgraphs.append(g)
            hashes.add(g_hash)

    # Return generated subgraphs
    return subgraphs

def bf_connected_subgraphs(G: nx.Graph, k: int) -> Iterable[nx.Graph]:
    """
    Computes all connected subgraphs.
    This includes all connected edge combinations as well,
    and is thus not limited to only induced subgraphs.
    """

    global logger

    # Resulting iterable
    subgraphs: Iterable[nx.Graph] = []

    # Get all induced subgraphs
    induced_subgraphs = bf_induced_connected_subgraphs(G, k)

    # Start logging
    logger.start_connected_subgraphs(len(induced_subgraphs))

    # Get all subgraphs from induced_subgraphs
    # for idx, isg in enumerate(non_isomorphic_subgraphs):
    for idx, isg in enumerate(induced_subgraphs):

        # Log progress
        logger.update_connected_subgraphs(idx + 1)

        # Generate all connected subgraphs
        connected_subgraphs = connected_edge_reduction(isg)

        # Append list
        subgraphs += connected_subgraphs

    # Return computed subgraphs
    return subgraphs


def connected_edge_reduction(G: nx.Graph) -> Iterable[nx.Graph]:
    """
    Performs a state-search over all subgraphs consisting of the same vertices
    but with less edges while still being connected.
    """

    # Import datastructure used for BFS
    from collections import deque

    # Create queue
    queue = deque()
    queue.append(G)

    # Create results list
    subgraphs: Iterable[nx.Graph] = [G]

    # Consume queue
    while len(queue) > 0:

        # Pop graph
        g: nx.Graph = queue.popleft()

        # Enumerate all edge removals
        for edge in g.edges:

            # Try to remove edge
            gp = nx.Graph(g)
            gp.remove_edge(*edge)

            # See if still connected
            if nx.is_connected(gp):
                subgraphs.append(gp)
                queue.append(gp)

    # Return found connected subgraphs
    return subgraphs


def non_isomorphic_graphs_hash(graphs: Iterable[nx.Graph]) -> Iterable[nx.Graph]:
    global logger
    logger.start_isomorphism_elimination(len(graphs))

    # Non-isomorphic subgraphs
    non_isomorphic: Iterable[nx.Graph] = []

    # Keep set of all hashes for isomorphism
    hashes: set[str] = set()

    # Check each graph manually
    for g in graphs:

        # Compute hash and check if already saved
        ghash = hash_graph(g)

        # If not existing graph, save it
        if ghash not in hashes:
            hashes.add(ghash)
            non_isomorphic.append(g)

    return non_isomorphic


def size_k_optimal_subgraphs_slow(G: nx.Graph, k: int) -> Iterable[nx.Graph]:
    global logger

    # Generate al non-isomorphic, induced connected subgraphs of size k
    # subgraphs = bf_induced_connected_subgraphs(G, k)
    #subgraphs = size_k_induced_connected_subgraphs(G, k)  # try new method
    #candidates = non_isomorphic_graphs_hash(subgraphs)

    # Use RAM-friendly implementation
    candidates = size_k_induced_connected_subgraphs_ram(G, k)

    # Optimal graphs
    C: Iterable[nx.Graph] = set()

    # Start logging
    logger.start_optimal_subgraphs(len(candidates))

    # Check every candidate for subgraph isomorphism
    candidates_all = candidates[:]
    for idx, cand in enumerate(candidates_all):

        # Report progress
        logger.update_optimal_subgraphs(idx + 1)

        # Compare to candidates in candidates
        subgraph_isomorphic = False
        for candp in candidates:

            if cand == candp:
                continue

            # Check for subgraph isomorphism
            gm = nx.algorithms.isomorphism.GraphMatcher(candp, cand)
            if gm.subgraph_is_monomorphic():
                subgraph_isomorphic = True
                break

        # If not subgraph isomorphic, add to set of optimal candidates
        # If is isomorphic, remove from list of candidates
        if subgraph_isomorphic:
            candidates.remove(cand)
        else:
            C.add(cand)

    # Return optimal subgraphs
    return C
