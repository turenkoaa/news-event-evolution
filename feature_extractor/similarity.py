import numpy as np
from datetime import datetime
from math import exp
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing.read_news import get_dates_between
from preprocessing.normalize_word import get_tf_idf


def cosine_sim(text):
    vectors = get_tf_idf(text, True)
    return cosine_similarity(vectors)


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
    texts = list(map(lambda doc: doc["normalized"], news))  # list(map(lambda doc: doc["normalized"], news))
    return cosine_sim(texts)


def get_jaccard_locations_sim(news):
    locations = list(map(lambda s: set(s["locations"]), news))  # news -> [[locations]]
    return get_jaccard_entities_sim(locations)


def get_jaccard_persons_sim(news):
    persons = list(map(lambda s: set(s["persons"]), news))  # news -> [[persons]]
    return get_jaccard_entities_sim(persons)


def get_jaccard_persons_and_locations_sim(news):
    persons_and_locations = list(map(lambda s: set(s["persons"] + s["locations"]), news))  # news -> [[persons]]
    return get_jaccard_entities_sim(persons_and_locations)


def get_jaccard_keywords_sim(news):
    persons_and_locations = list(map(lambda s: set(s['keywords']), news))  # news -> [[persons]]
    return get_jaccard_entities_sim(persons_and_locations)


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


def fresh_look_sim(news, alpha, time_delta):
    return get_cosine_text_sim(news) * get_jaccard_persons_and_locations_sim(news) # * get_time_decay(alpha, news, time_delta)


def text_and_keywords_sim(news, alpha, time_delta):
    return get_cosine_text_sim(news) * get_jaccard_keywords_sim(news) # * get_time_decay(alpha, news, time_delta)

# def use_date_for_sim(sim, news):
#     for i in range(len(sim)):
#         for j in range(len(sim)):
#             if news[i]['documentId'] < events[j]['documentId']:
#                 events_sim[j][i] = 0
