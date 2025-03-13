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
        # km.add_weighted_edges_from(edges[:k])
        for e in edges[:k]:
            # TODO: use km.addedge(0, 1, weight=w) so that weights are passed 
            km.add_edge(e[0], e[1], weight=e[2]['weight'])
    return km

def custom_draw(graph, dest,
                draw_edge_weights=True, layout=nx.circular_layout):
    pos1 = layout(graph)
    nx.draw_networkx(graph, pos=pos1, with_labels=True,
                     arrows=True, node_size=100)
    
    if draw_edge_weights:
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos1, edge_labels=labels, verticalalignment='baseline', font_size=8)
    plt.savefig(dest)