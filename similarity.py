import numpy as np
from datetime import datetime
from math import exp
from sklearn.metrics.pairwise import cosine_similarity
from read_news import get_dates_between
from normalize_word import get_tf_idf


def cosine_sim(text):
    vectors = get_tf_idf(text, True) # get_tf_idf_vectors(text)
    return cosine_similarity(vectors)


def get_event_term_vectors(events, story_vectors):
    vocabulary_len = len(story_vectors[0])

    event_term_vectors = np.empty((0, vocabulary_len), np.float64)
    for key, docs in events.items():
        v = np.array(np.zeros(vocabulary_len))
        for doc in docs:
            v = v + np.array(story_vectors[doc])
        v = v / len(docs)

        event_term_vectors = np.append(event_term_vectors, np.array([v]), axis=0)
    return event_term_vectors


def jaccard_sim(words1, words2):
    a = set(words1)
    b = set(words2)
    c = a.intersection(b)
    union_len = (len(a) + len(b) - len(c))
    return union_len if union_len == 0 else float(len(c)) / (len(a) + len(b) - len(c))


def get_jaccard_entities_sim(entities):
    matrix_len = len(entities)
    matrix = np.eye(matrix_len)

    for i in range(0, matrix_len):
        for j in range(i + 1, matrix_len):
            sim = jaccard_sim(entities[i], entities[j])
            matrix[i][j] = sim
            matrix[j][i] = sim

    return matrix


def get_cosine_text_sim(news):
    texts = list(map(lambda doc: doc["vanilla"], news))  # list(map(lambda doc: doc["normalized_text"], news))
    return cosine_sim(texts)


def get_jaccard_locations_sim(news):
    locations = list(map(lambda s: set(s["locations"]), news))  # news -> [[locations]]
    return get_jaccard_entities_sim(locations)


def get_jaccard_persons_sim(news):
    persons = list(map(lambda s: set(s["persons"]), news))  # news -> [[persons]]
    return get_jaccard_entities_sim(persons)


def get_cosine_locations_sim(news):
    locations = list(map(lambda story: "" + ' '.join(story["locations"]), news))
    return cosine_sim(locations)


def get_cosine_persons_sim(news):
    persons = list(map(lambda story: "" + ' '.join(story["persons"]), news))
    return cosine_sim(persons)


def time_decay(alpha, story1, story2, time_delta):
    d1 = datetime.strptime(story1["date"], '%Y-%m-%d')
    d2 = datetime.strptime(story2["date"], '%Y-%m-%d')
    local_delta = len(get_dates_between(d1, d2)) if d1 < d2 else len(get_dates_between(d2, d1))
    return exp(-alpha*local_delta/time_delta)


def get_time_decay(alpha, news, time_delta):
    matrix_len = len(news)
    matrix = np.eye(matrix_len)
    for i in range(0, matrix_len):
        for j in range(i + 1, matrix_len):
            sim = time_decay(alpha, news[i], news[j], time_delta)
            matrix[i][j] = sim
            matrix[j][i] = sim


def nallapati_sim(news, w, alpha, time_delta):
    return (w[0] * get_cosine_text_sim(news) + w[1] * get_jaccard_locations_sim(news) + w[2] * get_jaccard_persons_sim(news)) # * get_time_decay(alpha, news, time_delta)
