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
                z = 0
                
                if node != 0:
                    parent = next(dag.predecessors(node))
                    parent_edge_weight = weights[(node, parent)]
                    z = parent_edge_weight - max(max2, 0)
                
                max_weights[node] = (x, z, max1_v, max2_v)

    # Recover vertex-disjoint path
    path = []
    for node,(x,z,v1,v2) in max_weights.items():
        print(str(node) + ': ' + str((x,z,v1,v2)))
        if v1 != None and max_weights[v1][1] > 0:
            path.append((node, v1))

        if v2 != None:
            if node == 0:
                path.append((node, v2))
            else:
                parent = next(dag.predecessors(node))
                parent_z = max_weights[parent][1]
                if z <= 0: # or parent_z <= 0:
                    path.append((node, v2))

    print('Path edges: ' + str(path))
    print('Total path length (x(root)): ' + str(max_weights[0][0]))
    print('Total path length (actual): ' + str(sum(weights[e] for e in path)))
    print('Difference: ' + str(sum(weights[e] for e in path)-max_weights[0][0]))

    return path

def path_cover_two(tree):
    dag = nx.bfs_tree(tree, 0)
    topo = list(nx.topological_sort(dag))[::-1]
    weights = nx.get_edge_attributes(tree, 'weight')

    for u,v in list(weights.keys()):
        weights[v,u] = weights[u,v]
    
    X = {}
    for node in dag.nodes():
        if dag.out_degree(node) == 0:
            X[node] = 0

    while len(X) < tree.number_of_nodes():
        for node in topo:
            children = list(dag.successors(node))
            if len(children) == 0:
                continue
            if all(v in X for v in children):
                #case where one child

                # update X(node)
                child_nodes_weights = {}
                for child in children:
                    child_nodes_weights[child] = weights[child, node]
                max_key = max(child_nodes_weights, key = child_nodes_weights.get)
                #finds max weight
                fstmax = child_nodes_weights[max_key]
                if fstmax != 0:
                    child_nodes_weights[max_key] = -100
                #finds second max weight, sets to zero if it doesn't exist
                scdmax_key = max(child_nodes_weights, key = child_nodes_weights.get)
                scdmax = 0
                if child_nodes_weights[scdmax_key] != -100:
                    scdmax = child_nodes_weights[scdmax_key]
                if scdmax != 0:
                    child_nodes_weights[scdmax_key] = -100
                X[node] = fstmax + scdmax
                #adds all unused nodes, used nodes have been marked with -100
                for child in children:
                    if child_nodes_weights[child] != -100:
                        X[node] += X[child]
                
                #update the weights of the parents
                if (len(list(dag.predecessors(node))) != 0):
                    parent = list(dag.predecessors(node))[0]
                    if scdmax < weights[node, parent]:
                        weights[node, parent] = X[node] + weights[node, parent] - scdmax
                    else:
                        weights[node, parent] = 0
        
    return X



            
            
                

















