# Dominating Set
# n[1 + ln(\delta + 1)] / (\delta + 1)

import math
import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def generate_graph(num_vertices=10, edge_prob=0.2, min_degree=1):

    adj = np.zeros([num_vertices, num_vertices]).astype(int)  # Adjacency matrix
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))

    """
    for i in range(num_vertices):
        others = list(range(num_vertices))
        others.remove(i)
        random.shuffle(others)
        connect_vertices = others[:min_degree]
        random_vertices = others[min_degree:]
        for vertice in connect_vertices:
            adj[i,vertice] = 1
        for vertice in random_vertices:
            if random.random() < edge_prob:
                adj[i,vertice] = 1
    """

    # 给每个结点至少连接min_degree个结点
    for vertice in range(num_vertices):
        diff = min_degree - adj[vertice].sum()
        if diff > 0:
            connect_vertices = list(range(num_vertices))
            connect_vertices.remove(vertice)
            random.shuffle(connect_vertices)
            for i in connect_vertices[:diff]:
                adj[vertice,i] = 1
                adj[i,vertice] = 1
                G.add_edge(vertice,i)

    # 随机连接其余结点
    for i in range(num_vertices):
        for j in range(i+1,num_vertices):
            if random.random() < edge_prob:
                adj[i,j] = 1
                adj[j,i] = 1
                G.add_edge(i,j)

    return adj,G


def sel2dom(adj, selection):

    num_vertices = selection.shape[0]
    domination = np.zeros_like(selection).astype(int)
    for vertice in range(num_vertices):
        if selection[vertice]:
            domination[vertice] += 1
            domination += adj[vertice]

    # 0: not dominated   others: dominated
    return domination


def iter(adj, selection, min_degree):

    domination = sel2dom(adj, selection)
    not_dominated = domination==0   # True: 未被支配的点  False: 被支配
    not_selected = selection==0
    avg = not_dominated.sum()*(1+min_degree)/selection.shape[0]
    # print("avg:",avg)
    # print("not dominated:",not_dominated)
    """
    for candidate in range(not_dominated.shape[0]):
        if not_dominated[candidate]:
            count = adj[selection,candidate].sum()
            if count >= avg:
                selection[candidate] = 1
                break
    """
    """
    for candidate in range(not_selected.shape[0]):
        if not_selected[candidate]:
            count = adj[not_dominated,candidate].sum()
            if count >= avg:
                selection[candidate] = 1
                break
    """
    candidates = adj[not_dominated,:]
    count = np.sum(candidates, axis=0)
    index = np.argmax(count*not_selected)
    selection[index] = 1

    return selection


def greedy(adj, min_degree, selection=None):

    num_vertices = adj.shape[0]
    if selection is None:
        selection = np.zeros(num_vertices).astype(int)
    
    decay = math.exp(-1 * (1 + min_degree) * selection.sum() / num_vertices)
    domination = sel2dom(adj, selection)

    while decay > 1 / (1 + min_degree) and domination.sum()<num_vertices:
        selection = iter(adj, selection, min_degree)
        decay = math.exp(-1 * (1 + min_degree) * selection.sum() / num_vertices)
        domination = sel2dom(adj, selection)

    not_dominated = (domination==0).astype(int)
    selection += not_dominated

    # print("selection:",selection)
    # print("selection count:",selection.sum())
    # print("bound:",num_vertices*(1+math.log(min_degree+1))/(min_degree+1))

    return selection


def main():

    num_vertices = 200
    edge_prob = 0.02
    min_degree = 5
    random.seed(114514)

    adj,G = generate_graph(num_vertices=num_vertices, edge_prob=edge_prob, min_degree=min_degree)
    # selection = np.array([1,0,0,1,0]).astype(int)
    # print(adj)
    # print(sel2dom(adj,selection=selection))
    # nx.draw(G, with_labels=True)
    # plt.show()
    selection = greedy(adj,min_degree=min_degree)
    size_domination_set = selection.sum()
    bound = num_vertices*(1+math.log(min_degree+1))/(min_degree+1)
    print("selection count:",size_domination_set)
    print("bound:",bound)
    color_map = {0:"yellow",1:"red"}
    node_color = [color_map[i] for i in selection]
    nx.draw_networkx(G, with_labels=True, node_color=node_color, node_size=3000/num_vertices, width=10/num_vertices)

    plt.title("Number of vertices: " + str(num_vertices) + 
    "  minimum degree: $\delta=$" + str(min_degree) + 
    "\n Size of domination set: " + str(size_domination_set) + 
    "  Upper bound: " + str(round(bound,3)))

    plt.savefig(fname = "./figs/n="+str(num_vertices))
    plt.show()

    return 0

main()
