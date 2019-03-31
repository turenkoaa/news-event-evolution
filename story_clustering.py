import numpy as np

from similarity import nallapati_sim, get_tf_idf, get_event_term_vectors
from normalize_word import get_tf_idf, get_vectors


def story_clustering_to_events(sim_matrix, t, max_events_number):  # 100 mb, 13% cpu, 534 story - 40 sec
    events = {}
    for i in range(len(sim_matrix)):
        events[i] = [i]

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


def calculate_events_data(news, w, t):
    events_data = {}
    max_events_number = len(set(map(lambda n: n["clusterId"], news)))
    sim = nallapati_sim(news, w, 1, 1)  # get_cosine_text_sim(news)
    events = story_clustering_to_events(sim, t, max_events_number)
    story_vectors = get_vectors(list(map(lambda doc: doc["normalized_text"], news)))  # todo use cache

    events_data['news'] = news
    events_data['events'] = events
    events_data['event_term_vectors'] = get_event_term_vectors(events, story_vectors)

    return events_data
