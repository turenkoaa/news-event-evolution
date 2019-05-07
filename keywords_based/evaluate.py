import community
import networkx as nx
import numpy
import pandas as pd
import matplotlib.pyplot as plt

from story_clustering import calculate_edges


def num_of_communities_by_threshold(t, events_sim):
    edges = calculate_edges(t, events_sim)
    df = pd.DataFrame({'from': edges[0], 'to': edges[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.Graph())
    partition = community.best_partition(G)
    return float(len(set(partition.values())))


def num_of_communities_by_threshold_range_plot(events_sim, dates):
    t = numpy.arange(0.1, 0.3, 0.01)
    s = [num_of_communities_by_threshold(t, events_sim) for t in numpy.arange(0.1, 0.3, 0.01)]

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='threshold', ylabel='number of communities', title=dates[0] + ' - ' + dates[-1])
    ax.grid()

    fig.savefig("test.png")
    plt.show()


def get_components_from_graph(G):
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    print("Number of components: " + str(len(graphs)))
    communities = []
    for g in graphs:
        com = []
        for node in g.nodes():
            com.append(node)
        communities.append(com)

    return communities


def get_communities_from_graph(partition):
    size = float(len(set(partition.values())))
    print("Number of communities: " + str(size))
    communities = []
    for com in set(partition.values()):
        communityr = []
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]

        for node in list_nodes:
            communityr.append(node)
        communities.append(communityr)

    return communities