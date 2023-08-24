import networkx as nx
import random as rd

graph_properties = nx.DiGraph()
start_time = 0
end_time = 0
seeds = []
nodes_influenced = []


def SSA(seed_size):
    periods = int((end_time - start_time) / seed_size)
    for i in range(start_time, end_time, periods):
        temporal_graph = graph_properties.copy()
        temporal_graph.remove_edges_from(graph_properties.edges)
        if i + periods <= end_time:
            with open("graphs/uc_irv_edges.txt", 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    data = line.split(" ")
                    node1 = int(data[0].strip('\n'))
                    node2 = int(data[1].strip('\n'))
                    edge_time = int(data[3].strip('\n'))
                    if edge_time >= i and edge_time <= i + periods:
                        temporal_graph.add_edge(node1, node2)
        degree_centrality = nx.degree_centrality(temporal_graph)
        sorted_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        for node in sorted_degree_centrality:
            if node[0] not in nodes_influenced:
                seed = node[0]
                print("new seed:", seed)
                seeds.append(seed)
                nodes_influenced.append(node[0])
                break
        influence_new_node = True
        while influence_new_node:
            influence_new_node = False
            for node in nodes_influenced:
                out_edges = temporal_graph.out_edges(node)
                for edge in out_edges:
                    if graph_properties.edges[edge]['state'] == 0:
                        if rd.random() <= 0.5:
                            nodes_influenced.append(edge[1])
                            influence_new_node = True
                        graph_properties.edges[edge]['state'] = 1
        print("number of influenced nodes:", len(nodes_influenced))


if __name__ == "__main__":
    with open("D:/OLDinDynamicSocilaNetwork/DOLDBaseline/graphs/uc_irv_edges.txt", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            data = line.split(" ")
            node1 = int(data[0].strip('\n'))
            node2 = int(data[1].strip('\n'))
            if start_time == 0:
                start_time = int(data[3].strip('\n'))
            end_time = int(data[3].strip('\n'))
            graph_properties.add_node(node1)
            graph_properties.add_node(node2)
            graph_properties.add_edge(node1, node2, state=0)  # 0-未激活 1-已激活
    SSA(seed_size=10)
    print(seeds)
