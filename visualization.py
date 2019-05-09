import json

import community
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from keywords_based.evaluate import get_communities_from_graph


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

    stories = []

    for com in set(partition.values()):

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


def get_stories(G, partition, news, events, dates):
    single = set(range(len(events))) - set(G.nodes())
    communities = get_communities_from_graph(partition)

    stories = {
        'newsNumber': len(news),
        'eventsNumber': len(events),
        'singleNewsNumber': (len(single)),
        'storiesNumber': (len(communities)),
        'stories': []
    }

    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]

        events_by_dates = {date: [] for date in dates}
        # result_events_by_dates = {}
        for event_idx in list_nodes:
            event = events[event_idx]
            news_by_event = [{
                    'documentId': news[doc]['documentId'],
                    'text': news[doc]['vanilla']
                } for doc in event['news']]

            events_by_dates[event['date']].append({
                'event': news_by_event,
                'keywords': event['keywords']
            })

        # for date in events_by_dates:
        #     if not len(events_by_dates[date]) == 0:
        #         result_events_by_dates[date] = events_by_dates[date]

        stories['newsNumber'] = len(news)
        stories['eventsNumber'] = len(events)
        stories['singleNewsNumber'] = (len(single))
        stories['storiesNumber'] = (len(communities))

        stories['stories'].append({
            'storyId': events[list_nodes[0]]['start_time'],
            'events': events_by_dates  # result_events_by_dates
        })

    return stories


def show_graph_communities(G, partition, events):
    labels = {}
    for node in G.nodes():
        labels[node] = events[node]['keywords'][0]

    pos = nx.spring_layout(G)

    values = [partition.get(node) for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, labels=labels, with_labels=True, node_size=25,
                               node_color=values)

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=6)

    plt.axis('off')
    plt.savefig("labels_and_colors.png")
    plt.show()
