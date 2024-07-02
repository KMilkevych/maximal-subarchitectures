from typing import Callable, TypeAlias, Iterable, TypeVar

# Type aliases used here
Node: TypeVar = TypeVar("T")
Vertex: TypeAlias = int
iSet: TypeAlias = Iterable[Node]
Set: TypeAlias = Iterable[iSet]


# Computes the Refined Union Product as a CSP
def ref_union_product(
    sets: list[Set],
    vertex_disjoint: Callable[[iSet, iSet], bool],
    hasmark_new: Callable[iSet, bool],
    nochildren_of: Callable[[iSet, iSet], bool],
) -> Set:

    # Model as a CSP
    import constraint as cst

    problem = cst.Problem()

    # Model variables
    maxi = -1
    for idx, values in enumerate(sets):

        # If domain is empty, we stop from now on
        if len(values) == 0:
            break

        # Each set is a variable
        problem.addVariable(idx, values)
        maxi = idx

    # Follow initial constraints
    if maxi == -1:
        return []
    if maxi < 1:
        return sets[maxi]

    # Model all constraints
    for idx, values in enumerate(sets[: maxi + 1]):

        for jdx in range(idx + 1, min(maxi + 1, len(sets))):

            # Add constraints between idx and jdx
            problem.addConstraint(vertex_disjoint, (idx, jdx))
            problem.addConstraint(
                lambda a, b: hasmark_new(b) or nochildren_of(a, b), (idx, jdx)
            )

    # Set of all solutions
    solutions: Set = []
    for solution in problem.getSolutionIter():

        # Merge all subsolutions
        # solutions.append(sum(solution.values(), []))
        # Maybe maybe maybe...
        solutions.append(sum(map(list, solution.values()), []))

    # Return all solutions
    return solutions


# Try and test some constraint satisfaction
def test_rup():
    import networkx as nx

    G = nx.Graph()

    # Model all constraints in a fake way
    children = {
        1: set([2, 6, 8]),
        2: set([3, 5]),
        3: set([4]),
        4: set(),
        5: set([9]),
        6: set([7]),
        7: set(),
        8: set(),
        9: set(),
    }

    vertices = {1: "a", 2: "b", 3: "c", 4: "d", 5: "d", 6: "d", 7: "c", 8: "e", 9: "f"}

    def mpd(d):
        return lambda v: d[v]

    def vertex_disjoint(s1: iSet, s2: iSet) -> bool:
        # Convert to vertices
        vcs = mpd(vertices)
        v1 = map(vcs, s1)
        v2 = map(vcs, s2)

        # Check for disjoint
        return set(v1).isdisjoint(set(v2))

    def hasmark_new(s: iSet) -> bool:
        return not set([1, 2, 3, 4, 8]).isdisjoint(set(s))

    def notchild_of(s1: iSet, s2: iSet) -> bool:
        # Map to children to vertices
        from functools import reduce

        vcs = mpd(vertices)
        chd = mpd(children)
        c1 = map(chd, s1)
        v1 = map(vcs, reduce(lambda x, y: x.union(y), c1))
        v2 = map(vcs, s2)

        # Check that they are not the same
        return set(v1).isdisjoint(set(v2))

    r1 = ref_union_product([[[2]], [[6, 7]]], vertex_disjoint, hasmark_new, notchild_of)
    r2 = ref_union_product(
        [[[2, 3], [2, 5]], [[6]]], vertex_disjoint, hasmark_new, notchild_of
    )
    r3 = ref_union_product(
        [[[2, 3], [2, 5]], [[8]]], vertex_disjoint, hasmark_new, notchild_of
    )
    r4 = ref_union_product([[[6, 7]], [[8]]], vertex_disjoint, hasmark_new, notchild_of)

    r5 = ref_union_product(
        [[], [[1], [2], [3]]], vertex_disjoint, hasmark_new, notchild_of
    )
    r6 = ref_union_product(
        [[[7], [8], [9]], []], vertex_disjoint, hasmark_new, notchild_of
    )
    print(r1)
    print(r2)
    print(r3)
    print(r4)

    print()
    print(r5)
    print(r6)

    r7 = ref_union_product(
        [[[2, 3], [2, 5]], [[8]], [[9]]], vertex_disjoint, hasmark_new, notchild_of
    )
    print(r7)


if __name__ == "__main__":
    test_rup()
