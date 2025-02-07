import random, math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace

################################################################
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree, this will return the positions to plot it in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of the current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed
        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos
         
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


################################################################
def hierarchyc_pos(G, root=None, width=2*math.pi, vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    # Circular structure only for trees
    pos = hierarchy_pos(G, root, width = 2*math.pi, xcenter=0)
    new_pos = {u:(r*math.cos(theta),r*math.sin(theta)) for u, (theta, r) in pos.items()}
    return new_pos

################################################################
# Evenly distribute positions in a label
def hierarchye_pos(G, root, levels=None, width=1., height=1., xcenter = 0.5):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node
       levels: a dictionary
               key: level number (starting from 0)
               value: number of nodes in this level
       width: horizontal space allocated for drawing
       height: vertical space allocated for drawing'''
    TOTAL = "total"
    CURRENT = "current"
    def make_levels(levels, node=root, currentLevel=0, parent=None):
        """Compute the number of nodes for each level
        """
        if not currentLevel in levels:
            levels[currentLevel] = {TOTAL : 0, CURRENT : 0}
        levels[currentLevel][TOTAL] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                levels =  make_levels(levels, neighbor, currentLevel + 1, node)
        return levels

    def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0, xcenter = 0.5):
        dx = 1/levels[currentLevel][TOTAL]
        left = dx/2
        pos[node] = (xcenter+(left + dx*levels[currentLevel][CURRENT])*width, vert_loc)
        levels[currentLevel][CURRENT] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc-vert_gap)
        return pos
    if levels is None:
        levels = make_levels({})
    else:
        levels = {l:{TOTAL: levels[l], CURRENT:0} for l in levels}
    vert_gap = height / (max([l for l in levels])+1)
    return make_pos({})
	

# Generate GW Branching tree with Poisson(a) offspring upto level MAXLEVEL
def GWBP(a = 1, MAXLEVEL = 10, dist = None):
    if dist is None:
        dist = lambda: np.random.poisson(a)
    
    G = nx.DiGraph()
    G.add_node(0, level = 0)
    level = [0] * MAXLEVEL
    level[0] = 0
    #X = np.random.poisson(a)
    X = dist()
    level[1] = X

    for v in range(level[0]+1, level[1]+1):
        G.add_node(v, level = 1)
        G.add_edge(0, v)
    
    for i in range(1, MAXLEVEL-1):
        if level[i]==level[i-1]:
            break ## stop, no more growth
        level[i+1] = level[i]
        for j in range(level[i-1]+1, level[i]+1):
            #X = np.random.poisson(a)
            X = dist()
            for v in range(level[i+1]+1, level[i+1]+X+1):
                G.add_node(v, level = i+1)
                G.add_edge(j, v)
            level[i+1] = level[i+1] + X
    level = level[0:i]
    return G

def GWBP_finite_flag(a = 1, MAXLEVEL = 10, dist = None):
    if dist is None:
        dist = lambda: np.random.poisson(a)
    
    G = nx.DiGraph()
    G.add_node(0, level = 0)
    level = [0] * MAXLEVEL
    level[0] = 0
    #X = np.random.poisson(a)
    X = dist()
    level[1] = X

    for v in range(level[0]+1, level[1]+1):
        G.add_node(v, level = 1)
        G.add_edge(0, v)
    
    flag = False
    
    for i in range(1, MAXLEVEL-1):
        if level[i]==level[i-1]:
            flag = True
            break ## stop, no more growth
        level[i+1] = level[i]
        for j in range(level[i-1]+1, level[i]+1):
            #X = np.random.poisson(a)
            X = dist()
            for v in range(level[i+1]+1, level[i+1]+X+1):
                G.add_node(v, level = i+1)
                G.add_edge(j, v)
            level[i+1] = level[i+1] + X
    level = level[0:i]
    return G, flag


# Generate a branching tree using a uniform branching process upto level MAXLEVEL
def uniformtree(MAXLEVEL = 10):
    G = nx.DiGraph()
    G.add_node(0, level = 0)
    nodes_at_level = [0]
    node_id = 1

    for level in range(MAXLEVEL):
        children = []
        for node in nodes_at_level:
            num_leaves = np.random.randint(4)
            for _ in range(num_leaves):
                G.add_node(node_id, level)
                G.add_edge(node, node_id)
                children += node_id
                node_id += 1
        nodes_at_level = children
    
    return G


#nx.write_graphml(G, "tree.graphml")