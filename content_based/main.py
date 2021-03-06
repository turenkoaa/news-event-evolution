import json

import networkx as nx
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from keywords_based.evaluate import edges_distribution_plot, number_of_nodes_and_edges
from keywords_based.newslen_clustering import calculate_events
from preprocessing.read_news import get_dates_between, read_preprocessed_news_for_dates
from pylab import *
from feature_extractor.story_clustering import calculate_events_data, calculate_events_clusters, \
    get_event_term_vectors1, enrich_events_with_date
from postprocessing.visualization import draw_graph, get_stories_by_components, to_json, get_toloka


def get_stories_for_dates_content(d1, d2):
    dir = "C:/Users/User/Desktop/diploma/ner/data/results/content_based/"
    dates = get_dates_between(d1, d2)
    w = [0.7, 0.15, 0.15]
    t = 0.2 # 0.1

    news = read_preprocessed_news_for_dates(dates)
    print("amount of news:" + str(len(news)))
    events_data = calculate_events_data(news, w, t)
    events = events_data['events']
    events_sim = cosine_similarity(events_data['event_term_vectors'])
    enrich_events_with_date(events, news)

    threshold = 0.3

    for i in range(len(events_sim)):
        for j in range(len(events_sim)):
            if i == j or events[i]['start_time'] >= events[j]['start_time']:
                events_sim[i][j] = 0

    edges = np.argwhere(events_sim > threshold)

    df = pd.DataFrame({'from': edges.T[0], 'to': edges.T[1]})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())
    # draw_graph(G)

    stories, toloka = get_stories_by_components(G, news, events, dates)
    to_json(stories, dir + "stories/" + dates[0] + "_" + dates[-1] + ".json")
    to_json(toloka, dir + "stories/toloka/" + dates[0] + "_" + dates[-1] + ".json")
    avg = edges_distribution_plot(events_sim, dir + "evaluate/distribution_edge_weights_" + str(len(news)) + "_" + dates[0] + '_' + dates[-1] + ".png")
    number_of_nodes_and_edges(events_sim, avg, dir + "evaluate/nodes_ans_edges_" + str(len(news)) + "_" + dates[0] + '_' + dates[
                                  -1] + ".png")
    return stories


