import datetime
import json

import community
import networkx as nx
import pandas as pd

import numpy as np

from keywords_based.keywords_from_news import extract_keywords_from_news_tf_idf, \
    extract_keywords_from_news_rake, extract_keywords_from_news_ranktext, extract_keywords_from_news
from read_news import get_dates_between, read_preprocessed_news_for_dates
from similarity import get_jaccard_entities_sim
from story_clustering import calculate_events_clusters, enrich_events_with_date, \
    create_events_graph, enrich_events_with_keywords_union, enrich_events_with_keywords_intersection, \
    enrich_events_with_top_n_keywords, \
    enrich_events_with_keywords_intersection_with_param
from visualization import draw_graph, draw_graph3
import matplotlib.pyplot as plt


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


d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 10)  # end date
dates = get_dates_between(d1, d2)
w = [0.7, 0.15, 0.15]
t = 0.3 # 0.1

news = read_preprocessed_news_for_dates(dates)
extract_keywords_from_news(news, 0.25)

# for story in news:
#     # print(story['keywords'])
#     print(story['keywords_r'])
#     print(story['keywords_t'])
#     # print(story['persons'] + story['persons'])
#     print('________________')

events = calculate_events_clusters(news, w, t)
enrich_events_with_date(events, news)
enrich_events_with_keywords_intersection_with_param(events, news, 0.4)

events_sim = calculate_event_similarity_by_keywords_Jaccard(events)
edges = create_events_graph(0.1, events_sim)

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
    labels[node] = node # news[node]['documentId']

size = float(len(set(partition.values())))
print("Number of communities: " + str(size))
pos = nx.spring_layout(G)
count = 0.
with open("C:/Users/User/Desktop/diploma/ner/results/stories/stories.json", "w", encoding="utf8") as write_file:
    stories = []
    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, labels=labels, with_labels=True, node_size=20,
                               node_color=str(count / size))

        events_from_story = []
        for node in list_nodes:
            events_from_story.append(
                {'event': {
                    # 'id': node,
                    'news': [news[doc]['vanilla'] for doc in events[node]['news']],
                    'keywords': events[node]['keywords']
                    }
                }
            )


        stories.append({
                    # 'id': node,
                    'events': events_from_story
                })
    json.dump(stories, write_file, ensure_ascii=False)

nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G,pos,labels,font_size=16,font_color='r')
plt.show()

draw_graph3(edges[0], edges[1])
#
# for key in events:
#     print(">>>> " + str(key))
#     print(events[key]['keywords'])
#     print(">>>> ")
#     print(events[key]['start_time'])
#     for doc in events[key]['news']:
#         print(news[doc]['keywords'])
#         print("documentId = " + str(news[doc]['documentId']) + ":" + "(" + news[doc]["date"] + ")")
#         print(news[doc]['vanilla'])
#         print('_________________')

