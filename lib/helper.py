import networkx as nx
import matplotlib.pyplot as plt


def save_to_img(G: nx.Graph, filename: str):
    plt.clf() # Needed to avoid figures stacking
    nx.draw(G, with_labels=True)
    plt.savefig(filename)

def save_to_img_pp(G: nx.Graph, filename: str):
    plt.clf()
    nx.draw(G, pos=nx.planar_layout(G), with_labels=True)
    plt.savefig(filename)
