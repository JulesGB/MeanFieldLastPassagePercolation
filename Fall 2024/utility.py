import networkx as nx
import queue
import math
import random

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

def path_cover(tree, root=0, return_tuples=False):
    dag = nx.bfs_tree(tree, root)
    topo = list(nx.topological_sort(dag))[::-1]
    weights = nx.get_edge_attributes(tree, 'weight')

    if dag.number_of_nodes() == 1:
        return {0 : (0, random.uniform(0,1), 0, 0, 0)}.items() if return_tuples else (-1,-1,0,-1,-1)
                    # This was previously returning ({0 : ...}, -1, 0, -1, -1) 

    # Make weights bidirectional
    for u,v in list(weights.keys()):
        weights[v,u] = weights[u,v]

    # Initialize leaves as (0, w_parent(leaf))
    max_weights = {}
    for node in dag.nodes():
        if dag.out_degree(node) == 0:
            parents = dag.predecessors(node)
            # max_weights[node] = (0, next(parents), None, None)
            max_weights[node] = (0, 0, None, None, 0)  #added delta = 0 for leaves
            
    while len(max_weights) < dag.number_of_nodes():
        # Iterate over nodes in (reverse) topological order
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
                
                if node != root:
                    parent = next(dag.predecessors(node))
                    parent_edge_weight = weights[(node, parent)]
                    z = parent_edge_weight - max(max2, 0)
                else:
                    z = random.uniform(0,1) - max(max2, 0)
                    
                delta = max(max2, 0)

                # max_weights[node] = (x, z, max1_v, max2_v)
                max_weights[node] = (x, z, max1_v, max2_v, delta)                


    # max_weights[root] = list(max_weights[root])
    
    # max_weights[root][1] = random.uniform(0,1) if dag.number_of_nodes() == 1 else (random.uniform(0,1) - max_weights[root][3])

    # max_weights[root] = tuple(max_weights[root])
    if return_tuples:
        #print(max_weights)
        return max_weights.items()

    # Recover vertex-disjoint path
    # -----------------------------------------------
    path = set()

    current_node = None
    queue = [root]
    while len(queue) > 0:
        current_node = queue.pop(0)
        
        # BFS traversal
        for child in dag.successors(current_node):
            queue.append(child)

        x,z,v1,v2, _= max_weights[current_node]
        #x, delta, v1, v2 = max_weights[current_node]
        if v1 != None:
        #if v1 is not None and weights[(current_node, v1)] - max_weights[v1][1] >= 0:
            z_v1 = max_weights[v1][1]
            #if z_v1 >= 0 or z + z_v1 >= 0:
            if z_v1 >= 0:
                path.add((current_node, v1))

        if v2 != None:
        #if v2 is not None and weights[(current_node, v2)] - max_weights[v2][1] >= 0:
            z_v2 = max_weights[v2][1]
            if current_node == root:
                if z_v2 >= 0:
                    path.add((current_node, v2))
            else:
                parent = next(dag.predecessors(current_node))
                if z_v2 >= 0 and (parent, current_node) not in path:
                    path.add((current_node,v2))

    path_len = sum(weights[e] for e in path)
    x_root = max_weights[root][0]
    diff = path_len - x_root

    if not math.isclose(diff, 0.0, abs_tol=1e-4):
        if diff < 0:
            print("ERROR: Undercounting!")
        else:
            print("ERROR: Overcounting!")
        print(diff)

    return list(path), diff, max_weights[root][0], max_weights[root][1], max_weights


def find_leaves(graph):
    leaves = [node for node, deg in graph.degree() if deg == 1]
    return leaves

def karp_sipser(graph):
    graph_copy = graph.copy()
    leaves = []
    temp_leaves = find_leaves(graph_copy)
    while temp_leaves:
        leaves.extend(temp_leaves)
        graph_copy.remove_nodes_from(temp_leaves)
        temp_leaves = find_leaves(graph_copy)
    return graph.subgraph(leaves).copy()
    


            
            
                






















