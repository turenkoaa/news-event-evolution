import datetime
import json

import community
import networkx as nx
import pandas as pd
import numpy as np
from keywords_based.evaluate import num_of_communities_by_threshold_range_plot
from keywords_based.keywords_from_news import extract_keywords_from_news
from read_news import get_dates_between, read_preprocessed_news_for_dates
from similarity import get_jaccard_entities_sim
from story_clustering import create_events_graph, enrich_events_with_keywords_intersection_with_param, \
    calculate_events_clusters, enrich_events_with_date
import matplotlib.pyplot as plt

from visualization import draw_graph3


def calculate_event_similarity_by_keywords(events):
    matrix_len = len(events)
    matrix = np.zeros((len(events), len(events)))

    for i in range(0, matrix_len):
        for j in range(i + 1, matrix_len):
            a = set(events[i]['keywords'])
            b = set(events[j]['keywords'])
            c = a.intersection(b)

            if events[i]['start_time'] < events[j]['start_time']:
                matrix[i][j] = len(c)
            else:
                matrix[j][i] = len(c)

    return matrix


def calculate_event_similarity_by_keywords_Jaccard(events):
    keys = list(map(lambda k: set(events[k]['keywords']), events))
    events_sim = get_jaccard_entities_sim(keys)
    for i in range(len(events_sim)):
        for j in range(len(events_sim)):
            if i == j or events[i]['start_time'] >= events[j]['start_time']:
                events_sim[i][j] = 0
    return events_sim


def get_stories_for_news(news, events, dates):
    enrich_events_with_keywords_intersection_with_param(events, news, 0.4)
    events_sim = calculate_event_similarity_by_keywords_Jaccard(events)

    num_of_communities_by_threshold_range_plot(events_sim, dates)

    edges = create_events_graph(0.18, events_sim)

    df = pd.DataFrame({'from': edges[0], 'to': edges[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.Graph())

    partition = community.best_partition(G)
    labels = {}

    single = set(range(len(events))) - set(G.nodes())
    print("news number: " + str(len(news)))
    print("events number: " + str(len(events)))
    print("single number: " + str(len(single)))
    print(list(single))

    for node in G.nodes():
        labels[node] = news[node]['keywords'][1]

    size = float(len(set(partition.values())))
    print("Number of communities: " + str(size))
    pos = nx.spring_layout(G)
    count = 0.
    stories = []
    with open("C:/Users/User/Desktop/diploma/ner/results/stories/stories.json", "w", encoding="utf8") as write_file:
        for com in set(partition.values()):
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys()
                          if partition[nodes] == com]
            nx.draw_networkx_nodes(G, pos, list_nodes, labels=labels, with_labels=True, node_size=25, node_color=str(count / size))

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
        json.dump(stories, write_file, ensure_ascii=False)

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G,pos,labels,font_size=6)
    plt.show()
    draw_graph3(edges[0], edges[1])

    return stories


def get_stories_for_dates(d1, d2):
    dates = get_dates_between(d1, d2)
    w = [0.7, 0.15, 0.15]
    t = 0.3  # 0.1
    tf_idf_keywords_threshold = 0.25

    news = read_preprocessed_news_for_dates(dates)
    extract_keywords_from_news(news, tf_idf_keywords_threshold)
    events = calculate_events_clusters(news, w, t)
    # events = story_to_event_mapping(news)
    enrich_events_with_date(events, news)
    return get_stories_for_news(news, events, dates)