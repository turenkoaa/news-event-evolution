import json

import community
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from keywords_based.evaluate import get_communities_from_graph
from preprocessing.normalize_word import remove_urls


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

    return get_stories(G, clusters, news, events, dates), get_toloka(clusters, news, events)


def get_stories_by_components(G, news, events, dates):
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    clusters = []

    for g in graphs:
        res = []
        for node in g.nodes():
            res.append(node)
        clusters.append(res)

    return get_stories(G, clusters, news, events, dates), get_toloka(clusters, news, events)


def get_stories(G, clusters, news, events, dates):
    single = set(range(len(events))) - set(G.nodes())
    communities = get_communities_from_graph(clusters)
    # num_of_communities_by_threshold_range_plot(events_sim, dates)

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


def get_toloka(clusters, news, events):
    toloka_news = {}

    for cluster in clusters:
        story_id = events[cluster[0]]['start_time']
        toloka_news[story_id] = []
        for event_idx in cluster:
            event = events[event_idx]
            doc1 = news[event['news'][0]]
            toloka_news[story_id].append(remove_urls(doc1['vanilla']))

    toloka = []
    count = 0
    for story in toloka_news.values():
        for i in range(0, len(story)):
            for j in range(i + 1, len(story)):
                toloka.append({
                    "id": str(count),
                    "input_values": {
                        "story1": story[i],
                        "story2": story[j]
                    }
                })
                count = count + 1

    return toloka


def show_graph_communities(news, G, partition, events, file):
    labels = {}
    for node in G.nodes():
        labels[node] = events[node]['keywords'][0]
        G.node[node]['label'] = remove_urls(news[events[node]['news'][0]]['vanilla'])
        G.node[node]['color'] = partition.get(node)
        # G.node[node]['keywords'] = events[node]['keywords']

    pos = nx.spring_layout(G)

    values = [partition.get(node) for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, labels=labels, with_labels=True, node_size=25,
                               node_color=values)

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=6)
    nx.write_gexf(G, "test.gexf")

    plt.axis('off')
    plt.savefig(file)
    plt.clf()


def to_json(data, file_name):
    with open(file_name, "w", encoding="utf8") as write_file:
        json.dump(data, write_file, ensure_ascii=False)