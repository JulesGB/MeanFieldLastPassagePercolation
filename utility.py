import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

def kmax_diameter(graph):
    if nx.is_connected(graph):
        return nx.diameter(graph)
    else:
        sum = 0
        S = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
        for sub in S:
            sum += nx.diameter(sub)
        print("not sure what to put here yet so I just summed the diameter of the connected components")
        return sum