import numpy as np
import networkx as nx
from sklearn.cluster import KMeans


def normalize_dict(xy):
    X = np.array([val for val in xy.values()])
    norm_2 = np.sqrt((X ** 2).sum(axis=0))
    return {key: xy[key] / norm_2 for key in xy.keys()}


if __name__ == "__main__":
    NUM_CLUSTERS = 8
    NUM_OPINION_LEADERS = 10

    embedding = np.loadtxt("./embeddings/embeddings_tgn_UCI.txt")
    kmeans = KMeans(n_clusters=NUM_CLUSTERS)  # n_clusters:number of cluster
    kmeans.fit(embedding)

    labels = kmeans.labels_

    value_cnt = {}  
    for label in labels:  
        value_cnt[label] = value_cnt.get(label, 0) + 1
    print(value_cnt)

    G = nx.Graph()
    for i in range(len(embedding)):
        G.add_node(i + 1)

    scores = {}
    for i in range(len(embedding)):
        scores[i + 1] = 0

    start_time = 1082008561
    end_time = 1098744742  # 1085869012
    interval = 3600 * 24 * 14
    num_interval = int((end_time - start_time) / interval) + 1
    print('Divided into {} intervals'.format(num_interval))
    timestep = 0
    for time in range(start_time, end_time, interval):
        if time + interval > end_time:
            break
        G.remove_edges_from(G.edges)
        with open("./graphs/uc_irv_edges.txt", 'r', encoding="utf-8") as f:
            for line in f.readlines():
                data = line.split(" ")
                edge_time = int(data[3].strip('\n'))
                if time <= edge_time < time + interval:
                    G.add_edge(int(data[0]), int(data[1]))
        betweenness = normalize_dict(nx.betweenness_centrality(G, normalized=False))
        degree = normalize_dict(nx.degree_centrality(G))
        closeness = normalize_dict(nx.closeness_centrality(G))
        for score in scores:
            scores[score] += 1 * betweenness[score] * (1 - (timestep / num_interval) ** 2)
            scores[score] += 1 * degree[score] * (1 - (timestep / num_interval) ** 2)
            scores[score] += 1 * closeness[score] * (1 - (timestep / num_interval) ** 2)
        timestep += 1

    best_cluster = -1
    highest_score = -1
    for label in value_cnt:
        if value_cnt[label] > 600:
            continue
        else:
            cluster_score = 0
            for i in range(len(labels)):
                if labels[i] == label:
                    cluster_score += scores[i + 1]
            print("Cluster:", label, ", score=", cluster_score / value_cnt[label])
            if cluster_score / value_cnt[label] > highest_score:
                highest_score = cluster_score / value_cnt[label]
                best_cluster = label
    print("Best cluster:", best_cluster, ", score=", highest_score)
    candidate_node = {}
    for i in range(len(labels)):
        if labels[i] == best_cluster:
            candidate_node[i + 1] = scores[i + 1]
    node_ranking = sorted(candidate_node.items(), key=lambda x: x[1], reverse=True)
    print("Ranking of candidate_node:")
    final_rank = []
    for n in node_ranking:
        final_rank.append(n[0])
    print(final_rank[0:NUM_OPINION_LEADERS])
