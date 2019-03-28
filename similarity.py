import re
import numpy as np
from datetime import datetime
from math import exp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from read_news import get_dates_between


def cosine_sim(text):
    vectors = get_vectors(text) # get_tf_idf_vectors(text)
    return cosine_similarity(vectors)


def get_vectors(text):
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

def get_tf_idf_vectors(texts, use_idf = True):
    tfidf = TfidfVectorizer(use_idf=use_idf, analyzer='word', ngram_range=(1, 2),
                            min_df=0, sublinear_tf=True)

    tfidf_matrix = tfidf.fit_transform(texts)
    # if print:
    #     df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names())
    #     print(df)
    return tfidf_matrix


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

            # if matrix[i][j] > 0.7:
            #     print("locs 1: " + str(locations[i]))
            #     print("locs 2: " + str(locations[j]))

    return matrix


def get_cosine_text_sim(news):
    docs = list(map(lambda doc: doc["text"], news))
    texts = []

    for doc in docs:
        result = ""
        for token in doc:
            if not re.match(r".* +.*", token):
                result = result + " " + token
        texts.append(result)

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
