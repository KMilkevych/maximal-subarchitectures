# Remaps a nx.Graph into qmap.Architecture
def graph_to_architecture(graph):
    # import networkx as nx
    from mqt import qmap
    nm = {}
    new_edges = set()
    for edge in graph.edges():
        n1, n2 = edge
        if n1 not in nm.keys():
            nm[n1] = len(nm.keys())
        if n2 not in nm.keys():
            nm[n2] = len(nm.keys())
        new_edges.add((nm[n1], nm[n2]))
        new_edges.add((nm[n2], nm[n1])) # For bidirectional...
    return qmap.Architecture(len(nm.keys()), new_edges)

def normalize_graph(graph):
    import networkx as nx
    nm = {}
    new_edges = set()
    for edge in graph.edges():
        n1, n2 = edge
        n1, n2 = edge
        if n1 not in nm.keys():
            nm[n1] = len(nm.keys())
        if n2 not in nm.keys():
            nm[n2] = len(nm.keys())
        new_edges.add((nm[n1], nm[n2]))
    G = nx.Graph()
    G.add_nodes_from(nm.values())
    G.add_edges_from(list(new_edges))
    return G

def edge_view(graph, bidirectional=False):
    nm = {}
    new_edges = set()
    for edge in graph.edges():
        n1, n2 = edge
        n1, n2 = edge
        if n1 not in nm.keys():
            nm[n1] = len(nm.keys())
        if n2 not in nm.keys():
            nm[n2] = len(nm.keys())
        new_edges.add((nm[n1], nm[n2]))
        if bidirectional:
            new_edges.add((nm[n2], nm[n1]))
    return list(new_edges)
