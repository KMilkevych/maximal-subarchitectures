from typing import TypeVar, Iterable
from dataclasses import dataclass, field


# Representing a Generic Type to represent the set from which we take combinations
T = TypeVar("T")


# DataClass representing a TreeNode
@dataclass
class TreeNode:
    ident: int
    children: Iterable['TreeNode'] = field(default_factory=list)


# Helper function to extract paths from tree-walk
def tree_paths(root: TreeNode, path: list[int]) -> Iterable[list[int]]:

    # Base-case
    if len(root.children) == 0:
        return [path]

    # Append all children to path and call recursively
    paths: Iterable[list[int]] = []
    for child in root.children:

        # Call recursively
        ppath = path.copy()
        ppath.append(child.ident)
        child_paths: Iterable[list[int]] = tree_paths(child, ppath)

        # Append to existing paths
        paths += child_paths

    # Return found paths
    return paths

# Generate all subsets of S of size k
def k_combinations(k: int, S: list[T]) -> Iterable[Iterable[T]]:

    # Helper function to be called recursively
    def combination_rec(k: int, rest: int, s: int) -> Iterable[TreeNode]:

        # Base-case
        if k == 0:
            return []

        # Compute subtree
        tns: Iterable[TreeNode] = []
        for x in range(rest, s - k + 1):

            # Create new/empty treenode
            tn: TreeNode = TreeNode(x)

            # Call recursively
            tn.children = combination_rec(k-1, x+1, s)

            # Add to list of nodes generated at this step
            tns.append(tn)

        # Return computed nodes
        return tns

    # Compute tree
    root: TreeNode = TreeNode(-1)
    root.children = combination_rec(k, 0, len(S))

    # Now perform an in-order tree-walk to fetch the combinations
    paths: Iterable[list[int]] = tree_paths(root, [])

    # Parse them wrt. elements from S
    combinations: Iterable[list[T]] = []
    for path in paths:
        combinations.append(list(map(lambda v: S[v], path)))

    return combinations


def fixed_sum_k_combinations(k: int, S: int) -> Iterable[Iterable[int]]:

    # Helper function to be called recursively
    def k_sum_rec(k: int, S: int) -> Iterable[TreeNode]:

        # Base-case
        if k == 1:
            return [TreeNode(S)]

        # Compute subtree
        tns: Iterable[TreeNode] = []
        for x in range(1, S - k + 2):

            # Create node
            tn: TreeNode = TreeNode(x)

            # Compute children recursively
            tn.children = k_sum_rec(k-1, S-x)

            # Append to list of treenodes
            tns.append(tn)


        # Return computed treenodes
        return tns

    # Compute tree
    root: TreeNode = TreeNode(-1)
    root.children = k_sum_rec(k, S)

    # Perform in-order tree-walk to fetch all paths
    paths: Iterable[list[int]] = tree_paths(root, [])
    return paths


def test_k_combinations():

    print("Testing k-combinations")
    S: list[T] = [1, 2, 3, 4, 5]
    for k in range(0, len(S)+1):
        print(k, k_combinations(k, S))


def test_k_sum_combinations():

    print("Testing fixed-sum-l-combinations")
    S: int = 5
    for k in range(1, S+1):
        print(S,k,fixed_sum_k_combinations(k, S))


if __name__ == "__main__":
    test_k_combinations()
    test_k_sum_combinations()
