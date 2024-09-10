import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

n = 20
G = nx.complete_graph(n)

# Add random edge weights
for e in G.edges:
    G[e[0]][e[1]]["weight"] = random.uniform(0,1)

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

kmax = generate_kmax(G, 2)

# Drawing
plt.figure(1)
nx.draw_circular(kmax, with_labels=True)
plt.savefig("kmax.png")

plt.figure(2)
nx.draw_circular(G, with_labels=True)
plt.savefig("G.png")