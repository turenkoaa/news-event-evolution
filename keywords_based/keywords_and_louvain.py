import datetime

import community
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from normalize_word import get_tf_idf
from read_news import read_preprocessed_news_for_dates, get_dates_between
from similarity import nallapati_sim, fresh_look_sim, text_and_keywords_sim
from story_clustering import create_events_graph, get_min_date, calculate_events_similarity, enrich_events_with_date
from visualization import draw_graph

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 10)  # end date
dates = get_dates_between(d1, d2)
w = [0.7, 0.15, 0.15]
t = 0.2

news = read_preprocessed_news_for_dates(dates)
w = [0.7, 0.15, 0.15]
sim_t = 0 # 0.1
sim = fresh_look_sim(news, 1, 1)
# sim = nallapati_sim(news, w, 1, 1)



# for i in range(len(sim)):
#     for j in range(len(sim)):
#         if i == j or news[i]['documentId'] >= news[j]['documentId']:
#             sim[i][j] = 0
#         else:
#             sim[j][i] = 0

result = np.argwhere(sim > sim_t)
weighted_edges = [(edge[0], edge[1], dict(weight=sim[edge[0]][edge[1]])) for edge in result]
G = nx.Graph(weighted_edges)
labels = {}
for node in G.nodes():
    labels[node] = node  # news[node]['documentId']


betweenness = nx.betweenness_centrality(G, weight='weight')
for k, v in betweenness.items():
    if v > 0.2:
        print(news[k]['vanilla'])
        print("_______")


# threshold = 0.3
# events_sim = calculate_events_similarity(events, news)
# result = create_events_graph(threshold, events_sim)
# draw_graph(result[0], result[1])
#
#
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color='r')
# plt.show()