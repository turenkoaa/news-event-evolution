import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from feature_extractor.similarity import nallapati_sim, get_tf_idf


def story_clustering_to_events(sim_matrix, t, max_events_number):  # 100 mb, 13% cpu, 534 story - 40 sec
    events = {}
    for i in range(len(sim_matrix)):
        events[i] = {'news': [i]}

    if max_events_number > len(sim_matrix):
        return events

    max = 1
    events_count = len(events)
    while events_count > max_events_number and max > t:
        sims = np.zeros([events_count, events_count])
        for uId, uDocs in events.items():
            for vId, vDocs in events.items():
                if uId < vId:
                    sum = 0
                    for uStory in uDocs['news']:
                        for vStory in vDocs['news']:
                            sum = sum + sim_matrix[uStory][vStory]
                    sims[uId][vId] = sum / (len(uDocs['news']) * len(vDocs['news']))

        max_idx = np.unravel_index(sims.argmax(), sims.shape)
        max = sims[max_idx[0]][max_idx[1]]
        if max > t:
            events_count = len(events)
            events[max_idx[0]]['news'] = events[max_idx[0]]['news'] + events[max_idx[1]]['news']
            events[max_idx[1]]['news'] = events[events_count - 1]['news']
            del events[events_count - 1]
            events_count = len(events)

    return events


def get_event_term_vectors1(events, news):
    story_vectors = get_tf_idf(list(map(lambda doc: doc["normalized"], news)), False)
        # get_vectors(list(map(lambda doc: doc["normalized"], news)))  # todo use cache
    vocabulary_len = len(story_vectors[0])

    event_term_vectors = np.empty((0, vocabulary_len), np.float64)
    for key, event in events.items():
        v = np.array(np.zeros(vocabulary_len))
        for doc in event['news']:
            v = v + np.array(story_vectors[doc])
        v = v / len(event['news'])

        event_term_vectors = np.append(event_term_vectors, np.array([v]), axis=0)

    return event_term_vectors


def calculate_events_data(news, w, t):
    events_data = {}
    events = calculate_events_clusters(news, w, t)

    print("Start computation of event term vectors...")
    events_data['events'] = events
    for key in events:
        events[key]['date'] = news[events[key]['news'][0]]['date']
    events_data['event_term_vectors'] = get_event_term_vectors1(events, news)

    return events_data


def calculate_events_clusters(news, w, t):
    max_events_number = len(set(map(lambda n: n["clusterId"], news))) * 1.5
    sim = nallapati_sim(news, w, 1, 1)  # get_cosine_text_sim(news)
    print("Start story clustering...")
    events = story_clustering_to_events(sim, t, max_events_number)
    return events


def story_to_event_mapping(sim_matrix):  # 100 mb, 13% cpu, 534 story - 40 sec
    events = {}
    for i in range(len(sim_matrix)):
        events[i] = {'news': [i]}
    return events


def get_min_date(news, docs):
    dates = list(map(lambda i: news[i]['documentId'], docs))
    return min(dates)


def calculate_events_similarity(events, news):
    event_term_vectors = get_event_term_vectors1(events, news)
    events_sim = cosine_similarity(event_term_vectors)

    for i in range(len(events_sim)):
        for j in range(len(events_sim)):
            if i == j or events[i]['start_time'] >= events[j]['start_time']:
                events_sim[i][j] = 0

    return events_sim


def calculate_edges(threshold, events_sim):
    result = np.argwhere(events_sim > threshold)
    return result.T


def enrich_events_with_date(events, news):
    for key in events:
        events[key]['start_time'] = get_min_date(news, events[key]['news'])


def enrich_events_with_keywords_union(events, news):
    for key in events:
        keys = []
        for doc in events[key]['news']:
            keys = keys + list(news[doc]['keywords'])

        events[key]['keywords'] = set(keys)


def enrich_events_with_keywords_intersection(events, news):
    for key in events:
        keys = news[events[key]['news'][0]]['keywords']
        for doc in events[key]['news']:
            keys = set.intersection(set(news[doc]['keywords']), keys)

        events[key]['keywords'] = keys


def enrich_events_with_keywords_intersection_with_param(events, news, threshold):
    for key in events:
        events[key]['keywords'] = []
        keys = []
        for doc in events[key]['news']:
            keys = keys + list(news[doc]['keywords'])

        amount = len(events[key]['news'])
        for keyword in set(keys):
            count = 0
            for doc in events[key]['news']:
                if keyword in list(news[doc]['keywords']):
                    count = count + 1
            if float(count) / amount > threshold:
                events[key]['keywords'].append(keyword)


def enrich_events_with_top_n_keywords(events, news, n):
    for key in events:
        corpus = list(map(lambda i: news[i]["normalized"], events[key]['news']))
        vec = CountVectorizer().fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in
                      vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1],
                            reverse=True)
        events[key]['keywords'] = words_freq[:n]

