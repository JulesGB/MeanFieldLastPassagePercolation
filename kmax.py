import matplotlib.pyplot as plt
import networkx as nx

def generate_kmax(graph, k):
    # Copy nodes from G
    km = nx.DiGraph()
    km.add_nodes_from(graph.nodes())
    
    # Get list of edges from node, then sort according to weight and take the largest k edges
    for node in graph:
        edges = list(graph.edges(node, data=True))
        edges.sort(key=lambda e: e[2]['weight'], reverse=True)
        km.add_weighted_edges_from(edges[:k])

    return km

def custom_draw(graph, dest, draw_edge_weights=True, layout=nx.circular_layout):
    nx.draw(graph, with_labels=True, arrows=True, pos=layout(graph))
    if draw_edge_weights:
        pos = nx.circular_layout(graph)
        labels = {k:v['weight'] for k,v in nx.get_edge_attributes(graph, 'weight').items()}

        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, verticalalignment='baseline', font_size=8)
    plt.savefig(dest)