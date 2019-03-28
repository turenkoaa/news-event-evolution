import numpy as np
from similarity import nallapati_sim

def story_clustering_to_events(news, w, t):
    sim = nallapati_sim(news, w, 1, 1)  # get_cosine_text_sim(news)
    cluster_ids = set(map(lambda n: n["clusterId"], news))

    events = {}
    for i in range(len(news)):
        events[i] = [i]

    max = 1
    eventsCount = len(events)
    while eventsCount >= len(cluster_ids) / 2 and max > t:
        sims = np.zeros([eventsCount, eventsCount])
        for uId, uDocs in events.items():
            for vId, vDocs in events.items():
                if uId < vId:
                    sum = 0
                    for uStory in uDocs:
                        for vStory in vDocs:
                            sum = sum + sim[uStory][vStory]
                    if uId == 0 and vId == 167:
                        print()
                    sims[uId][vId] = sum / (len(uDocs) * len(vDocs))

        max_idx = np.unravel_index(sims.argmax(), sims.shape)
        max = sims[max_idx[0]][max_idx[1]]
        eventsCount = len(events)
        events[max_idx[0]] = events[max_idx[0]] + events[max_idx[1]]
        events[max_idx[1]] = events[eventsCount - 1]
        del events[eventsCount - 1]

    return events



