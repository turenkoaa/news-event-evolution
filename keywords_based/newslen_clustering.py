import json

import community
import networkx as nx
import numpy
import pandas as pd
import numpy as np
from feature_extractor.keywords_from_news import extract_keywords_from_news
from keywords_based.evaluate import num_of_communities_by_threshold_range_plot, edges_distribution_plot, \
    number_of_nodes_and_edges
from preprocessing.read_news import get_dates_between, read_news_for_dates
from feature_extractor.similarity import get_jaccard_entities_sim
from feature_extractor.story_clustering import calculate_edges, enrich_events_with_keywords_intersection_with_param, \
    calculate_events_clusters, enrich_events_with_date
import matplotlib.pyplot as plt
from postprocessing.visualization import show_graph_communities, get_stories_by_partition, to_json


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
    dir = "C:/Users/User/Desktop/diploma/ner/data/results/keywords_based/"
    enrich_events_with_keywords_intersection_with_param(events, news, keywords_threshold)
    events_sim = calculate_event_similarity_by_keywords_Jaccard(events)

    edges = calculate_edges(edges_threshold, events_sim)
    # weighted_edges = [(edge[0], edge[1], dict(weight=events_sim[edge[0]][edge[1]])) for edge in edges.T]
    # G = nx.Graph(weighted_edges)
    # partition = community.best_partition(G, weight='weight')

    df = pd.DataFrame({'from': edges[0], 'to': edges[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.Graph())
    diG = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())

    partition = community.best_partition(G)
    stories, toloka = get_stories_by_partition(G, partition, news, events, dates)

    to_json(stories, dir + "stories/" + dates[0] + "_" + dates[-1] + ".json")
    to_json(toloka, dir + "stories/toloka/" + dates[0] + "_" + dates[-1] + ".json")

    show_graph_communities(news, G, partition, events, dir + "/graph/communities_" + dates[0] + "_" + dates[-1] + ".png")
    # draw_graph3(edges[0], edges[1])
    avg = edges_distribution_plot(events_sim, dir + "evaluate/distribution_edge_weights_" + str(len(news)) + "_" + dates[0] + '_' + dates[-1] + ".png")
    num_of_communities_by_threshold_range_plot(events_sim, avg, dir + "evaluate/number_of_communities_" + str(len(news)) + "_" + dates[0] + '_' + dates[-1] + ".png")
    number_of_nodes_and_edges(events_sim, avg, dir + "evaluate/nodes_ans_edges_" + str(len(news)) + "_" + dates[0] + '_' + dates[-1] + ".png")

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
    print("Getting stories for " + d1.strftime("%Y-%m-%d") + ' - ' + d2.strftime("%Y-%m-%d") + "...")
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
