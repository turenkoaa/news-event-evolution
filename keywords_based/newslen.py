import datetime

import numpy as np

from keywords_based.keywords_from_news import extract_keywords_from_news
from read_news import get_dates_between, read_preprocessed_news_for_dates
from story_clustering import calculate_events_clusters, enrich_events_with_date, enrich_events_with_keywords

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 10)  # end date
dates = get_dates_between(d1, d2)
news = read_preprocessed_news_for_dates(dates)

extract_keywords_from_news(news, 0.17)

w = [0.7, 0.15, 0.15]
t = 0.2 # 0.1
events = calculate_events_clusters(news, w, t)

enrich_events_with_date(events, news)
enrich_events_with_keywords(events, news)

for key in events:
    print(">>>> " + str(key))
    print(events[key]['keywords'])
    print(events[key]['start_time'])
    for doc in events[key]['news']:
        print("documentId = " + str(news[doc]['documentId']) + ":" + "(" + news[doc]["date"] + ")")
        print(news[doc]['vanilla'])
        print('_________________')


def create_events_graph(threshold, news, events):
    events_sim = np.zeros(len(events), len(events),)

    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            if ()

            if events[i]['start_time'] >= events[j]['start_time']:
                events_sim[i][j] = 0

    story_vectors = get_tf_idf(list(map(lambda doc: doc["vanilla"], news)), False)
    event_term_vectors = get_event_term_vectors1(events, story_vectors)
    events_sim = cosine_similarity(event_term_vectors)

    for i in range(len(events_sim)):
        for j in range(len(events_sim)):
            if i == j or events[i]['start_time'] >= events[j]['start_time']:
                events_sim[i][j] = 0

    result = np.argwhere(events_sim > threshold)
    return result.T