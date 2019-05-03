import datetime

import community
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from normalize_word import get_tf_idf
from read_news import read_preprocessed_news_for_dates, get_dates_between
from similarity import nallapati_sim, fresh_look_sim
from story_clustering import create_events_graph, get_min_date, calculate_events_similarity, enrich_events_with_date
from visualization import draw_graph

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 12)  # end date
dates = get_dates_between(d1, d2)
w = [0.7, 0.15, 0.15]
t = 0.2

news = read_preprocessed_news_for_dates(dates)
sim = fresh_look_sim(news, 1, 1)


for i in range(len(sim)):
    for j in range(0, i + 1):
        sim[i][j] = 0

result = np.argwhere(sim > t)

weighted_edges = [(edge[0], edge[1], dict(weight=sim[edge[0]][edge[1]])) for edge in result]


G = nx.Graph(weighted_edges)
labels = {}
for node in G.nodes():
    labels[node] = node  # news[node]['documentId']

partition = community.best_partition(G, weight='weight')

size = float(len(set(partition.values())))
print("topics count: " + str(size))
pos = nx.spring_layout(G)
count = 0
events = {}

for com in set(partition.values()):
    count = count + 1
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    # nx.draw_networkx_nodes(G, pos, list_nodes, labels=labels, node_size=20, node_color=str(count / size))
    events[count - 1] = {'news': []}
    for node in list_nodes:
        events[count - 1]['news'].append(news[node]['index'])
    events[count - 1]['start_time'] = get_min_date(news, events[count - 1]['news'])

for key in events:
    print(">>>> " + str(key))
    for doc in events[key]['news']:
        print("documentId = " + str(news[doc]['documentId']) + ":" + "(" + news[doc]["date"] + ")")
        print(news[doc]['vanilla'])
    print('_________________')


threshold = 0.3
events_sim = calculate_events_similarity(events, news)
result = create_events_graph(threshold, events_sim)
draw_graph(result[0], result[1])
#
#
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color='r')
# plt.show()