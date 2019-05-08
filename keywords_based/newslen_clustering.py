import datetime
import json

import community
import networkx as nx
import pandas as pd
import numpy as np
from keywords_based.evaluate import num_of_communities_by_threshold_range_plot, get_communities_from_graph, \
    get_components_from_graph
from keywords_based.keywords_from_news import extract_keywords_from_news
from read_news import get_dates_between, read_preprocessed_news_for_dates, read_news_for_dates
from similarity import get_jaccard_entities_sim
from story_clustering import calculate_edges, enrich_events_with_keywords_intersection_with_param, \
    calculate_events_clusters, enrich_events_with_date

from visualization import draw_graph3, communities_to_stories, show_graph_communities, communities_to_stories


def calculate_event_similarity_by_keywords_intersection(events):
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


def get_stories_for_news(news, events, dates, keywords_threshold, edges_threshold):
    enrich_events_with_keywords_intersection_with_param(events, news, keywords_threshold)
    events_sim = calculate_event_similarity_by_keywords_Jaccard(events)

    edges = calculate_edges(edges_threshold, events_sim)

    df = pd.DataFrame({'from': edges[0], 'to': edges[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.Graph())
    diG = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())

    partition = community.best_partition(G)
    stories = communities_to_stories(G, partition, news, events, dates)

    with open("C:/Users/User/Desktop/diploma/ner/results/stories/" + dates[0] + "_" + dates[-1] + ".json", "w", encoding="utf8") as write_file:
        json.dump(stories, write_file, ensure_ascii=False)

    show_graph_communities(G, partition, events)

    # draw_graph3(edges[0], edges[1])

    communities = get_communities_from_graph(partition)
    components = get_components_from_graph(diG)
    # num_of_communities_by_threshold_range_plot(events_sim, dates)

    # for key in events:
    #     print(">>>> " + str(key))
    #     for doc in events[key]['news']:
    #         print(news[doc]['vanilla'])
    #         print('_________________')

    return stories


def calculate_events(news_by_dates, w, t):
    events = {}
    news = {}

    index_accumulator = 0
    for date in news_by_dates:
        events_by_date = calculate_events_clusters(news_by_dates[date], w, t)  # events = story_to_event_mapping(news)
        for key in events_by_date:
            events_by_date[key]['date'] = date

            new_value = []
            for story_idx in events_by_date[key]['news']:
                new_value.append(news_by_dates[date][story_idx]['documentId'])
            events_by_date[key]['news'] = new_value
            events[key + index_accumulator] = events_by_date[key]
        index_accumulator = index_accumulator + len(events_by_date.items())

        for story in news_by_dates[date]:
            news[story["documentId"]] = story

    return news, events


def get_stories_for_dates(d1, d2):
    dates = get_dates_between(d1, d2)
    w = [0.7, 0.15, 0.15]
    t = 0.3  # 0.1
    tf_idf_keywords_threshold = 0.25
    keywords_threshold = 0.4
    edges_threshold = 0.2

    news, events = calculate_events(read_news_for_dates(dates), w, t)
    extract_keywords_from_news(list(news.values()), tf_idf_keywords_threshold)
    enrich_events_with_date(events, news)

    return get_stories_for_news(news, events, dates, keywords_threshold, edges_threshold)
