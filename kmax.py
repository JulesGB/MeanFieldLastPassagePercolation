import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

def generate_kmax(graph, k):
    # Copy nodes from G
    km = nx.Graph()
    km.add_nodes_from(G.nodes())
    
    # Get list of edges from node, then sort according to weight and take the largest k edges
    for node in G:
        edges = list(G.edges(node, data=True))
        edges.sort(key=lambda e: e[2]['weight'], reverse=True)
        km.add_weighted_edges_from(edges[:k])

    return km

def custom_draw(graph, dest, draw_edge_weights=True):
    nx.draw_circular(graph, with_labels=True)
    if draw_edge_weights:
        pos = nx.circular_layout(graph)
        labels = {k:v['weight'] for k,v in nx.get_edge_attributes(graph, 'weight').items()}

        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, verticalalignment='baseline', font_size=8)
    plt.savefig(dest)

# Test setup
n = 20
G = nx.complete_graph(n)

# Add random edge weights
for e in G.edges:
    G[e[0]][e[1]]["weight"] = random.uniform(0,1)

kmax = generate_kmax(G, 1)

# Drawing
plt.figure(1)
custom_draw(kmax, "kmax.png")

plt.figure(2)
custom_draw(G, "G.png", draw_edge_weights=False)