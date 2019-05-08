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


def communities_to_stories(G, partition, news, events, dates):
    single = set(range(len(events))) - set(G.nodes())
    print("news number: " + str(len(news)))
    print("events number: " + str(len(events)))
    print("single stories number: " + str(len(single)))

    count = 0.
    stories = {'events': []}

    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]

        events_by_dates = {date: [] for date in dates}
        for node in list_nodes:
            news_by_event = [{
                    'documentId': news[doc]['documentId'],
                    'text': news[doc]['vanilla'],
                    'date': news[doc]['date']
                } for doc in events[node]['news']]
            events_by_dates[events[node]['date']].append({
                'news': news_by_event,
                'keywords': events[node]['keywords']
            })

        stories['events'].append(events_by_dates)

    return stories


def show_graph_communities(G, partition, events):
    labels = {}
    for node in G.nodes():
        labels[node] = events[node]['keywords'][1]

    pos = nx.spring_layout(G)

    values = [partition.get(node) for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, labels=labels, with_labels=True, node_size=25,
                               node_color=values)

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=6)

    plt.axis('off')
    plt.savefig("labels_and_colors.png")
    plt.show()
