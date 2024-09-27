import networkx as nx
import queue

def kmax_diameter(graph):
    if nx.is_strongly_connected(graph):
        return nx.diameter(graph)
    else:
        sum = 0
        S = [graph.subgraph(c).copy() for c in nx.weakly_connected_components(graph)]
        for sub in S:
            sum += nx.diameter(sub)
        print("not sure what to put here yet so I just summed the diameter of the connected components")
        return sum
    
def count_bidrectional(graph):
    return 0.5 * len([ 1 for (u,v) in graph.edges() if u in graph[v] ])

def path_cover(tree):
    dag = nx.bfs_tree(tree, 0)
    topo = list(nx.topological_sort(dag))[::-1]
    weights = nx.get_edge_attributes(tree, 'weight')

    # Make weights bidirectional
    for u,v in list(weights.keys()):
        weights[v,u] = weights[u,v]

    # Initialize leaves as (0, w_parent(leaf))
    max_weights = {}
    for node in dag.nodes():
        if dag.out_degree(node) == 0:
            parents = dag.predecessors(node)
            max_weights[node] = (0, next(parents), None, None)

    while len(max_weights) < tree.number_of_nodes():
        # Iterate over nodes in (reverse) topological order so that leaf nodes
        for node in topo:               
            children = list(dag.successors(node))
            
            # All children are defined
            if all(v in max_weights for v in children): 
                max1 = max2 = float('-inf')
                max1_v = max2_v = None
                for v in children:
                    zv = max_weights[v][1]
                    if zv > max2:
                        if zv >= max1:
                            max2, max2_v = max1, max1_v
                            max1, max1_v = zv, v
                        else:
                            max2, max2_v = zv, v

                x = sum([max_weights[v][0] for v in children]) + max(max1, 0) + max(max2, 0)
                z = None
                
                if node != 0:
                    parent = next(dag.predecessors(node))
                    parent_edge_weight = weights[(node, parent)]
                    z = parent_edge_weight - max(max2, 0)
                
                max_weights[node] = (x, z, max1_v, max2_v)

    # Recover vertex-disjoint path
    path = []
    for node,(x,z,v1,v2) in max_weights.items():
        if v1 != None and max_weights[v1][1] > 0:
            path.append((node, v1))
        if v2 != None and (node == 0 or (z != None and z <= 0)):
            path.append((node, v2))

    print('Path edges: ' + str(path))
    print('Total path length (x(root)): ' + str(max_weights[0][0]))
    print('Total path length (actual): ' + str(sum(weights[e] for e in path)))
    print('Difference: ' + str(sum(weights[e] for e in path)-max_weights[0][0]))

    return path

            
            
    


















