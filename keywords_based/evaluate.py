import community
import networkx as nx
import numpy
import pandas as pd
import matplotlib.pyplot as plt

from story_clustering import create_events_graph


def num_of_communities_by_threshold(t, events_sim):
    edges = create_events_graph(t, events_sim)
    df = pd.DataFrame({'from': edges[0], 'to': edges[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.Graph())
    partition = community.best_partition(G)
    return float(len(set(partition.values())))


def num_of_communities_by_threshold_range_plot(events_sim):
    t = numpy.arange(0.1, 0.3, 0.01)
    s = [num_of_communities_by_threshold(t, events_sim) for t in numpy.arange(0.1, 0.3, 0.01)]

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='threshold', ylabel='number of communities',
           title='')
    ax.grid()

    fig.savefig("test.png")
    plt.show()