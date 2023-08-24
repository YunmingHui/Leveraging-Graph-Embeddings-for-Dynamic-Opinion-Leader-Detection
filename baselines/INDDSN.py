# On Influential Node Discovery in Dynamic Social Networks
import networkx as nx

start_time = 0
end_time = 0
graph_nodes = nx.DiGraph()


def DynInfluenceVal(network):
    num_periods = 20
    periods = int((end_time - start_time) / num_periods)

    for i in range(start_time, end_time, periods):
        temporal_graph = network.copy()
        if i + periods <= end_time:
            with open("graphs/uc_irv_edges.txt", 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    data = line.split(" ")
                    node1 = int(data[0].strip('\n'))
                    node2 = int(data[1].strip('\n'))
                    edge_time = int(data[3].strip('\n'))
                    if edge_time >= i and edge_time <= i + periods:
                        temporal_graph.add_edge(node1, node2)
            for node in temporal_graph.nodes:
                tansmit_rate = 1
                in_edges = temporal_graph.in_edges(node)
                if in_edges:
                    for edge in in_edges:
                        tansmit_rate *= 1 - temporal_graph.nodes[edge[0]]['contain_info'] * 0.5
                network.nodes[node]['contain_info'] = temporal_graph.nodes[node]['contain_info'] + (
                        1 - temporal_graph.nodes[node]['contain_info']) * (1 - tansmit_rate)
    res = 0
    for node in network.nodes:
        res += network.nodes[node]['contain_info']
    return res


def ForwardInfluence(seed_size):
    initial_score = {}
    graph_influence = graph_nodes.copy()

    with open("INDDSN_ini_res_uc_irv_save.txt", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            data = line.split(" ")
            initial_score[int(data[0].strip('\n'))] = float(data[1].strip('\n'))


    sorted_ini_score = sorted(initial_score.items(), key=lambda x: x[1], reverse=True)
    sorted_node = []
    for node in sorted_ini_score:
        sorted_node.append(node[0])
    seeds = sorted_node[0:seed_size]

    min_iter = 3
    no_replace = 0

    for seed in seeds:
        graph_influence.nodes[seed]['contain_info'] = 1
    best_influence = DynInfluenceVal(graph_influence.copy())

    print("current influence=", best_influence, ",", "initial seeds:", seeds)

    candidate_node = seed_size

    while no_replace < min_iter:
        graph_influence.nodes[sorted_node[candidate_node]]['contain_info'] = 1
        replaced = False
        replace_seed = 0
        for seed in seeds:
            graph_influence.nodes[seed]['contain_info'] = 0
            influence = DynInfluenceVal(graph_influence.copy())
            if influence > best_influence:
                replaced = True
                best_influence = influence
                replace_seed = seed
            graph_influence.nodes[seed]['contain_info'] = 1
        if replaced:
            seeds.remove(replace_seed)
            seeds.append(sorted_node[candidate_node])
            no_replace = 0
        else:
            no_replace += 1
        candidate_node += 1
        print("current influence=", best_influence, ",", "no replace time=", no_replace, ",", "current seeds:", seeds)
    print("final seeds:", seeds)


if __name__ == "__main__":
    print("UC-IRV")
    with open("graphs/uc_irv_edges.txt", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            data = line.split(" ")
            node1 = int(data[0].strip('\n'))
            node2 = int(data[1].strip('\n'))
            if start_time == 0:
                start_time = int(data[3].strip('\n'))
            end_time = int(data[3].strip('\n'))
            graph_nodes.add_node(node1, contain_info=0)
            graph_nodes.add_node(node2, contain_info=0)

    ForwardInfluence(seed_size=50)
