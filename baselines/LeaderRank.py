# -*- coding: UTF-8 -*-
"""
This file runs the LeaderRank algorithm.
"""
import networkx as nx
import time


def leaderrank():
    """
    Node ordering
    :param graph: complex network graph Graph
    :return: Return the node sort value
    """
    graph = nx.DiGraph()
    with open("graphs/wikitalk_cy_edges.txt", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            data = line.split(" ")
            graph.add_edge(int(data[0]), int(data[1]))
    print("Graph created!")
    # Number of nodes
    num_nodes = graph.number_of_nodes()
    # Node
    nodes = graph.nodes()
    # Add node g to the network and connect to all nodes
    graph.add_node(0)
    for node in nodes:
        graph.add_edge(0, node)
    # LR value initialization
    print("Initialized graph!")
    LR = dict.fromkeys(nodes, 1.0)
    LR[0] = 0.0
    print("Initialized LeaderRank!")
    # Iterate to satisfy the stop condition
    cnt = 0
    while True:
        st = time.time()
        cnt += 1
        tempLR = {}
        for node1 in graph.nodes():
            s = 0.0
            for node2 in graph.nodes():
                if node2 in graph.neighbors(node1):
                    s += 1.0 / graph.degree([node2])[node2] * LR[node2]
            tempLR[node1] = s
        # Termination condition: LR value is not changing
        error = 0.0
        for n in tempLR.keys():
            error += abs(tempLR[n] - LR[n])
        if error <= 1.0:
            break
        LR = tempLR
        print(f"Time for iteration {cnt}: {time.time() - st} seconds | Error = {error}")
    # The LR value of node g is equally distributed to other N nodes and the node
    avg = LR[0] / num_nodes
    LR.pop(0)
    for k in LR.keys():
        LR[k] += avg

    rank = sorted(LR.items(), key=lambda x: x[1], reverse=True)
    rank_node = []
    for r in rank:
        rank_node.append(r[0])
    print(rank_node[0:50])


if __name__ == "__main__":
    leaderrank()
