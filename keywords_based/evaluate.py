import community
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from feature_extractor.story_clustering import calculate_edges


def num_of_communities_by_threshold(t, events_sim):
    edges = calculate_edges(t, events_sim)
    df = pd.DataFrame({'from': edges[0], 'to': edges[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.Graph())
    partition = community.best_partition(G)
    return float(len(set(partition.values())))


def num_of_communities_by_threshold_range_plot(events_sim, amounts, file):
    t = np.arange(0, 0.3, 0.005)
    s = [num_of_communities_by_threshold(t, events_sim) for t in np.arange(0, 0.3, 0.005)]

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='threshold', ylabel='number of communities')
    ax.grid()

    plt.axvline(amounts.mean(), color='k', linestyle='dashed', linewidth=1)
    # _, max_ = plt.ylim()
    # plt.text(amounts.mean() + amounts.mean() / 10, max_ - max_ / 10, '{:.2f}'.format(amounts.mean()))

    fig.savefig(file)
    plt.clf()


def edges_distribution_plot(events_sim, file):
    amounts = []
    for i in range(0, len(events_sim)):
        for j in range(0, len(events_sim[0])):
            if events_sim[i][j] > 0:
                amounts.append(events_sim[i][j])
    amounts = np.array(amounts)
    num_bins = 50
    plt.hist(amounts, num_bins, color='c', edgecolor='k', alpha=0.5)
    plt.title("Distribution of edge weights")
    plt.axvline(amounts.mean(), color='k', linestyle='dashed', linewidth=1)
    # _, max_ = plt.ylim()
    # plt.text(amounts.mean() + amounts.mean() / 10, max_ - max_ / 10, '{:.2f}'.format(amounts.mean()))
    plt.savefig(file)
    plt.clf()

    return amounts.mean()


def number_of_nodes_and_edges(events_sim, amounts, file):
    t = np.arange(0, 1, 0.005)
    s = [number_of_nodes(t, events_sim) for t in np.arange(0, 1, 0.005)]

    plt.plot(t, np.array(s).T[1], label="edges", linestyle='dashed')
    plt.plot(t, np.array(s).T[0], label="nodes")
    plt.legend(loc='best')
    plt.axvline(amounts.mean(), color='k', linestyle='dashed', linewidth=1)
    # _, max_ = plt.ylim()
    # plt.text(amounts.mean() + amounts.mean() / 10, max_ - max_ / 10, '{:.2f}'.format(amounts.mean()))
    plt.title("Number of nodes and edges")

    plt.savefig(file)
    plt.clf()


def number_of_nodes(t, events_sim):
    edges = calculate_edges(t, events_sim)

    df = pd.DataFrame({'from': edges[0], 'to': edges[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.Graph())

    return [len(G.nodes()), len(G.edges())]


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


def get_communities_from_graph(clusters):
    size = float(len(clusters))
    print("Number of communities: " + str(size))
    communities = []
    for com in clusters:
        communityr = []
        for node in com:
            communityr.append(node)
        communities.append(communityr)

    return communities