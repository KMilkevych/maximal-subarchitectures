import networkx as nx
from typing import Iterable, TypeVar, TypeAlias, Callable
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum


# Wrapper for performing memoization of heavy computations
def init_memoization(core_fun: Callable) -> Callable:

    # Memoization dictionary
    mem = {}

    # Construct wrapper
    def wrapper(*args):
        print(args)
        print(*args)
        if args in mem.keys():
            return mem[args]
        else:
            res = core_fun(*args)
            mem[args] = res
            return res

    # Return wrapper
    return wrapper


if __name__ != "__main__":
    from lib.kcongraph.kcombinations import k_combinations, fixed_sum_k_combinations
    from lib.kcongraph.refunionprod import ref_union_product
else:
    from kcombinations import k_combinations, fixed_sum_k_combinations
    from refunionprod import ref_union_product

T: TypeAlias = int
NT: TypeAlias = int


# Mark enum used for marking nodes and vertices
class Mark(Enum):
    NONE = 0
    NEW = 1
    VISITED = 2
    SEEN = 3


# TreeNode class used for tree structure
@dataclass
class TreeNode:
    ident: T
    idx: int
    children: Iterable[int] = field(default_factory=list)
    mark: Mark = Mark.NONE


NodeMap: TypeAlias = dict[NT, TreeNode]


def __make_vertex_disjoint_constraint(nm: NodeMap):
    def vertex_disjoint(s1: Iterable[TreeNode], s2: Iterable[TreeNode]) -> bool:
        v1 = map(lambda tn: nm[tn].ident, s1)
        v2 = map(lambda tn: nm[tn].ident, s2)
        return set(v1).isdisjoint(set(v2))

    return vertex_disjoint


def __make_hasmark_new_constraint(nm: NodeMap):
    def hasmark_new(s: Iterable[TreeNode]) -> bool:
        return Mark.NEW in set(map(lambda tn: nm[tn].mark, s))

    return hasmark_new


def __make_nochildren_of_contraint(nm: NodeMap):
    def nochildren_of(s1: Iterable[TreeNode], s2: Iterable[TreeNode]) -> bool:
        c1 = sum(list(map(lambda tn: nm[tn].children, s1)), [])
        v1 = map(lambda tn: nm[tn].ident, c1)
        v2 = map(lambda tn: nm[tn].ident, s2)
        return set(v1).isdisjoint(set(v2))

    return nochildren_of


def combinations_from_tree(
    nodemap: NodeMap, root: TreeNode, k: int
) -> Iterable[Iterable[NT]]:

    # Variable to hold result
    lnodesets: Iterable[Iterable[NT]] = []

    # Base case
    if k == 1:
        return [[root.idx]]

    # Try every combination of various sizes
    for i in range(1, min(len(root.children), k - 1) + 1):

        # Try each node combination
        for comb in k_combinations(i, root.children):

            for comp in fixed_sum_k_combinations(i, k - 1):

                fail: bool = False
                Ss: list[Iterable[Iterable[T]]] = [[[]] for _ in range(i)]

                for pos in range(0, i):

                    subtree_root: TreeNode = nodemap[comb[pos]]
                    size: int = comp[pos]

                    Ss[pos] = combinations_from_tree(nodemap, subtree_root, size)
                    if len(Ss[pos]) == 0:
                        fail = True
                        break

                if fail:
                    continue

                # Create all combinations
                const_1 = __make_vertex_disjoint_constraint(nodemap)
                const_2 = __make_hasmark_new_constraint(nodemap)
                const_3 = __make_nochildren_of_contraint(nodemap)

                union_prod = ref_union_product(Ss, const_1, const_2, const_3)
                for comb_prod in union_prod:
                    lnodesets.append(([root.idx] + comb_prod))

    return lnodesets


def size_k_combinations_with_v(v: T, k: int, G: nx.Graph) -> Iterable[Iterable[T]]:

    # Build combination tree
    nodemap: NodeMap = dict()
    root: TreeNode = TreeNode(v, 0)
    nodemap[0] = root

    # Initalize list
    lst: list[Iterable[T]] = [[] for _ in range(k + 1)]  # Need larger size
    lst[0].append(v)

    # Initialize marks for vertices
    v_marks = defaultdict(lambda: Mark.NONE)

    # Helper function to build the tree
    def build_tree(
        nodemap: NodeMap, root: TreeNode, depth: int, G: nx.Graph, k: int
    ) -> None:

        # Update list with ancestors
        lst[depth] = lst[depth - 1].copy()

        # Examine each neighbor vertex
        for v in G.neighbors(root.ident):

            # If we are ancestor, sibling or sibling of ancestor
            if v in lst[depth]:
                # Skip
                continue

            # Add as child
            nt_id: int = len(nodemap)
            nt: TreeNode = TreeNode(v, nt_id)
            nodemap[nt_id] = nt
            root.children.append(nt_id)
            lst[depth].append(v)

            # Handle marks
            if v_marks[v] != Mark.VISITED:
                nt.mark = Mark.NEW
                v_marks[v] = Mark.VISITED
            else:
                nt.mark = Mark.SEEN

            # Call recursively with this node as root
            if depth + 1 <= k:
                build_tree(nodemap, nt, depth + 1, G, k)

        return

    # Build tree
    build_tree(nodemap, root, 1, G, k)

    # Map found combinations into their respective vertices
    combinations: Iterable[Iterable[NT]] = combinations_from_tree(nodemap, root, k)

    def nodemap_mapper(nlist: Iterable[NT]) -> Iterable[T]:
        return list(map(lambda v: nodemap[v].ident, nlist))

    # and return them
    return list(map(nodemap_mapper, combinations))


def size_k_connected_subgraphs_tree(G: nx.Graph, k: int) -> Iterable[nx.Graph]:

    combinations: Iterable[nx.Graph] = []
    Gp = nx.Graph(G)

    for v in G.nodes:
        combinations += size_k_combinations_with_v(v, k, Gp)
        Gp.remove_node(v)

    return combinations


def test_size_k_connected_subgraphs():

    """
    g = nx.Graph()
    g.add_nodes_from([0, 1, 2, 3, 4])
    g.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (0, 4),
        (1, 4),
        (2, 4)
    ])
    subgraphs = size_k_connected_subgraphs(4, g)
    print(subgraphs)
    """

    """
    g = nx.Graph()
    g.add_nodes_from([0, 1, 2, 3, 4])
    g.add_edges_from([
        (0, 1),
        (1, 2),
        (1, 3),
        (2, 3),
        (0, 3),
        (0, 4)
    ])
    combinations = size_k_combinations_with_v(0, 4, g)
    print(combinations)
    """

    # Test using brute force
    def k_connected_bf(G: nx.Graph, k: int) -> set[frozenset[int]]:
        from itertools import combinations

        true_comb: set[frozenset[int]] = set()
        combs = combinations(G.nodes, k)
        for comb in combs:
            g = nx.Graph(nx.induced_subgraph(G, comb))
            if nx.is_connected(g):
                true_comb.add(frozenset(comb))
        return list(true_comb)

    # Test using implementation
    def k_connected_tr(G: nx.Graph, k: int) -> set[frozenset[int]]:
        combs = size_k_connected_subgraphs_tree(G, k)
        return list(map(lambda v: frozenset(v), combs))

    # Test for various graphs
    from collections import Counter

    failed = False
    for n in range(1, 8):
        g = nx.complete_graph(n)
        for k in range(1, n + 1):
            combs_1 = k_connected_bf(g, k)
            combs_2 = k_connected_tr(g, k)
            if Counter(combs_1) != Counter(combs_2):
                print("ERRONEOUS ON")
                print(g, g.nodes, g.edges)
                print(combs_1)
                print(combs_2)
                failed = True
                break
        if failed:
            break

    if failed:
        print("FAILED")
    else:
        print("ALL GOOD")


if __name__ == "__main__":
    test_size_k_connected_subgraphs()
