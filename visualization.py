import json

import community
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(fromV, toV):
    df = pd.DataFrame({'from': fromV, 'to': toV})

    # Build your graph
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    print("Number of Stories: " + str(len(graphs)))

    for g in graphs:
        pos = nx.spring_layout(g)

    # Plot it
        nx.draw(g, pos, with_labels=True)
        plt.show()


def draw_graph3(fromV, toV):

    df = pd.DataFrame({'from': fromV, 'to': toV})

    # Build your graph
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())
    pos = nx.spring_layout(G)
    graphs = list(nx.weakly_connected_component_subgraphs(G))

    # Plot it
    nx.draw(G, pos, with_labels=True)
    plt.show()


def communities_to_stories(G, partition, news, events, dates):
    single = set(range(len(events))) - set(G.nodes())
    print("news number: " + str(len(news)))
    print("events number: " + str(len(events)))
    print("single stories number: " + str(len(single)))

    count = 0.
    stories = []

    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]

        news_by_dates = {date: [] for date in dates}
        for node in list_nodes:
            for doc in events[node]['news']:
                news_by_dates[news[doc]['date']].append({
                    'documentId': news[doc]['documentId'],
                    'text': news[doc]['vanilla'],
                    'date': news[doc]['date']
                })

        stories.append({
            # 'id': node,
            'events': news_by_dates
        })


    return stories


def show_graph_communities(G, partition, news):
    labels = {}

    size = float(len(set(partition.values())))
    for node in G.nodes():
        labels[node] = news[node]['keywords'][1]

    pos = nx.spring_layout(G)
    count = 0.

    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, labels=labels, with_labels=True, node_size=25,
                               node_color=str(count / size))

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=6)
    plt.show()



def draw_graph1(fromV, toV, ids, classes):
    df = pd.DataFrame({'from': fromV, 'to': toV})
    carac = pd.DataFrame({'ID': ids, 'classes': classes})

    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())
    G.nodes()
    carac = carac.set_index('ID')
    carac = carac.reindex(G.nodes())

    nx.draw(G, with_labels=True, node_color=carac['classes'])

    # graphs = list(nx.weakly_connected_component_subgraphs(G))
    # for g in graphs:
    #     pos = nx.spring_layout(g)
    #
    # # Plot it
    #     nx.draw(g, pos, with_labels=True)

    plt.show()