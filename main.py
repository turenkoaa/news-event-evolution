import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from print_results import print_number_of_news_clusters_and_texts, print_story_clustering_per_day
from read_news import get_dates_between, read_preprocessed_news, read_cluster, read_preprocessed_news_for_dates


import scipy.stats as st
from pylab import *

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 17)  # end date
dates = get_dates_between(d1, d2)

for date in dates:
    news = read_preprocessed_news(date)
    print_story_clustering_per_day(news)



# print(get_cosine_text_sim(news))

# feature_names = tfidf.get_feature_names()
# corpus_index = [n for n in corpus]
# rows, cols = tfs.nonzero()
# for row, col in zip(rows, cols):
#     print((feature_names[col], corpus_index[row]), tfs[row, col])

# alpha = 1
# time_delta = len(dates)
# news = read_preprocessed_news_for_dates(dates)
#
# for i in range(0, len(news)):
#     for j in range(i + 1, len(news)):
#         print(news[i]["date"] + "/" + news[j]["date"] + ": " + str(time_decay(alpha, news[i], news[j], time_delta)))

# news = read_preprocessed_news(d1.strftime('%Y-%m-%d'))
# texts_count = len(news)
# w1, w2 = 0.9, 0.1
# alpha = 0
# time_delta = len(dates)
# matrix = nallapati_sim(news, [w1, w2/2, w2/2], alpha, time_delta)

# for i in range(0, texts_count):
#     for j in range(i + 1, texts_count):
#         if news[i]["clusterId"] == news[j]["clusterId"]:
#             print(matrix[i][j])
#             print(str(news[i]["documentId"]) + ": " + news[i]["vanilla"][0:150])
#             print(str(news[j]["documentId"]) + ": " + news[j]["vanilla"][0:150])
#             print("\n")



# for i in range(1,5):
#     cluster = read_cluster(news, i)
#     for doc in cluster:
#         print(doc["vanilla"])
#         print("// cluster_id=" + str(doc["clusterId"]))
#     print("____________________________________________________________")
