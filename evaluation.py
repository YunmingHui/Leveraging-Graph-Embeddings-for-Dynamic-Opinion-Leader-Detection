import random as rd
import networkx as nx


def SI_model(Gx, initial_infecteds, beta, start_time, end_time, interval):
    # Initialize parameters
    initialNodesInfected = initial_infecteds
    population = len(Gx.nodes())

    # Declare the empty lists
    sData = []  # susceptible data
    infectedData = []  # infected data

    # Function for finding neighbours and infected nodes
    def getInfected(graph):
        return [x for x, y in graph.nodes(data=True) if y['infected'] == 1]

    def getNeighbors(graph, givenNode):
        return [x for x in graph.neighbors(givenNode)]

    # setting initial conditions
    for node in Gx.nodes():
        if int(node) in initialNodesInfected:
            Gx.nodes[node]['infected'] = True
        else:
            Gx.nodes[node]['infected'] = False

    # Iterate for t_simulation
    for time in range(start_time, end_time, interval):
        if time + interval > end_time:
            break
        Gx.remove_edges_from(list(Gx.edges))
        with open("./graphs/uc_irv_edges.txt", 'r', encoding="utf-8") as f:
            for line in f.readlines():
                data = line.split(" ")
                edge_time = int(data[3].strip('\n'))
                if time <= edge_time < time + interval:
                    Gx.add_edge(int(data[0]), int(data[1]))

        # infecting nodes based on beta value
        infected = getInfected(Gx)
        for j in infected:
            neighbors = getNeighbors(Gx, j)
            for n in neighbors:
                if Gx.nodes[n]['infected'] == False:
                    rand = rd.random()
                    if rand <= beta:
                        Gx.nodes[n]['infected'] = True

        # Append all infected results
        infected = getInfected(Gx)
        infectedData.append(len(infected))
        sData.append(population - len(infected))

    return sData, infectedData


if __name__ == "__main__":
    Gx = nx.DiGraph()
    with open("./graphs/uc_irv_edges.txt", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            data = line.split(" ")
            Gx.add_edge(int(data[0]), int(data[1]))
    initial_infecteds_tgn = [9, 32, 103, 41, 249, 713, 3, 67, 1713, 12]
    
    beta = 0.5
    start_time = 1082008561
    end_time = 1098744742  # 1085869012
    interval = 3600 * 24 * 14

    num_test = 100

    _, infected = SI_model(Gx, initial_infecteds_tgn, beta, start_time, end_time, interval)
    for i in range(num_test):
        sData, infectedData = SI_model(Gx, initial_infecteds_tgn, beta, start_time, end_time, interval)
        for j in range(len(infectedData)):
            infected[j] += infectedData[j]
    infected_tgn = [int(x / (num_test + 1)) for x in infected]
    print(infected_tgn)
   
