import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from similarity import nallapati_sim, get_tf_idf
from normalize_word import get_vectors


def story_clustering_to_events(sim_matrix, t, max_events_number):  # 100 mb, 13% cpu, 534 story - 40 sec
    events = {}
    for i in range(len(sim_matrix)):
        events[i] = [i]

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
                    for uStory in uDocs:
                        for vStory in vDocs:
                            sum = sum + sim_matrix[uStory][vStory]
                    sims[uId][vId] = sum / (len(uDocs) * len(vDocs))

        max_idx = np.unravel_index(sims.argmax(), sims.shape)
        max = sims[max_idx[0]][max_idx[1]]
        if max > t:
            events_count = len(events)
            events[max_idx[0]] = events[max_idx[0]] + events[max_idx[1]]
            events[max_idx[1]] = events[events_count - 1]
            del events[events_count - 1]
            events_count = len(events)

    return events


def get_event_term_vectors(events, story_vectors):
    vocabulary_len = len(story_vectors[0])

    event_term_vectors = np.empty((0, vocabulary_len), np.float64)
    for key, event in events.items():
        v = np.array(np.zeros(vocabulary_len))
        for doc in event:
            v = v + np.array(story_vectors[doc])
        v = v / len(event)

        event_term_vectors = np.append(event_term_vectors, np.array([v]), axis=0)

    return event_term_vectors


def get_event_term_vectors1(events, story_vectors):
    vocabulary_len = len(story_vectors[0])

    event_term_vectors = np.empty((0, vocabulary_len), np.float64)
    for key, event in events.items():
        v = np.array(np.zeros(vocabulary_len))
        for doc in event['news']:
            v = v + np.array(story_vectors[doc])
        v = v / len(event)

        event_term_vectors = np.append(event_term_vectors, np.array([v]), axis=0)

    return event_term_vectors


def calculate_events_data(news, w, t):
    events_data = {}
    max_events_number = len(set(map(lambda n: n["clusterId"], news))) * 1.5
    sim = nallapati_sim(news, w, 1, 1)  # get_cosine_text_sim(news)
    print("Start story clustering...")
    events = story_clustering_to_events(sim, t, max_events_number)

    print("Start computation of event term vectors...")
    story_vectors = get_tf_idf(list(map(lambda doc: doc["vanilla"], news)), False)
        # get_vectors(list(map(lambda doc: doc["normalized_text"], news)))  # todo use cache

    events_data['news'] = news
    events_data['events'] = events
    events_data['event_term_vectors'] = get_event_term_vectors(events, story_vectors)

    return events_data


def create_events_graph(threshold, news, events):
    story_vectors = get_tf_idf(list(map(lambda doc: doc["vanilla"], news)), False)
    event_term_vectors = get_event_term_vectors(events, story_vectors)
    events_sim = cosine_similarity(event_term_vectors)

    for i in range(len(events_sim)):
        for j in range(0, i + 1):
            events_sim[i][j] = 0

    result = np.argwhere(events_sim > threshold)
    return result.T