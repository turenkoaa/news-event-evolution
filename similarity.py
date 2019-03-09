import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cosine_sim(text):
    vectors = get_vectors(text)
    return cosine_similarity(vectors)


def get_vectors(text):
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


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
    texts = list(map(lambda doc: "" + ' '.join(doc["text"]), news))
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
