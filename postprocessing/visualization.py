import json

import community
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from keywords_based.evaluate import get_communities_from_graph


def draw_graph(G):
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


def get_stories_by_partition(G, partition, news, events, dates):
    clusters = []
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        clusters.append(list_nodes)

    return get_stories(G, clusters, news, events, dates)


def get_stories_by_components(G, news, events, dates):
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    clusters = []

    for g in graphs:
        res = []
        for node in g.nodes():
            res.append(node)
        clusters.append(res)

    return get_stories(G, clusters, news, events, dates)


def get_stories(G, clusters, news, events, dates):
    single = set(range(len(events))) - set(G.nodes())
    communities = get_communities_from_graph(clusters)

    stories = {
        'newsNumber': len(news),
        'eventsNumber': len(events),
        'singleNewsNumber': (len(single)),
        'storiesNumber': (len(communities)),
        'stories': []
    }

    for cluster in clusters:
        events_by_dates = {date: [] for date in dates}
        # result_events_by_dates = {}
        for event_idx in cluster:
            event = events[event_idx]
            for doc in event['news']:
                events_by_dates[event['date']].append({
                     'documentId': news[doc]['documentId'],
                     'text': news[doc]['vanilla']
                })

        # for date in events_by_dates:
        #     if not len(events_by_dates[date]) == 0:
        #         result_events_by_dates[date] = events_by_dates[date]

        stories['newsNumber'] = len(news)
        stories['eventsNumber'] = len(events)
        stories['singleNewsNumber'] = (len(single))
        stories['storiesNumber'] = (len(communities))

        stories['stories'].append({
            'storyId': events[cluster[0]]['start_time'],
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


def to_json(data, file_name):
    with open(file_name, "w", encoding="utf8") as write_file:
        json.dump(data, write_file, ensure_ascii=False)