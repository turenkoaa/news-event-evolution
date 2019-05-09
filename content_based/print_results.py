import datetime

from preprocessing.read_news import read_cluster, get_dates_between, read_preprocessed_news_for_dates
from feature_extractor.similarity import nallapati_sim
from feature_extractor.story_clustering import story_clustering_to_events


def print_number_of_news_clusters_and_texts(news, date):
    f = open("C:/Users/User/Desktop/diploma/ner/data/results/clusters_data/" + date + ".txt", "w+", encoding="utf8")
    cluster_ids = set(map(lambda n: n["clusterId"], news))
    for i in cluster_ids:
        f.write("cluster_id=" + str(i) + "\n")
        cluster = read_cluster(news, i)
        for doc in cluster:
            f.write("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _" + "\n")
            f.write("documentId: " + str(doc["documentId"]) + "\n")
            f.write(doc["vanilla"] + "\n")
        f.write("____________________________________________________________" + "\n")

    f.write("Date: " + date + "\n")
    f.write("number of news: " + str(len(news)) + "\n")
    f.write("number of clusters: " + str(len(cluster_ids)) + "\n")
    f.close()


def print_story_clustering_per_day(news, date):
    # params
    w = [0.7, 0.15, 0.15]
    t = 0.1

    max_events_number = len(set(map(lambda n: n["clusterId"], news))) * 1.5
    sim = nallapati_sim(news, w, 1, 1)  # get_cosine_text_sim(news)
    events = story_clustering_to_events(sim, t, max_events_number)
    f = open("C:/Users/User/Desktop/diploma/ner/data/results/story_clustering/lemms/" + date + ".txt", "w+", encoding="utf8")
    f.write("Parameters: w=" + str(w) + ", t=" + str(t) + "\n")

    for id, docs in events.items():
        f.write("event: " + str(id) + "\n")
        for doc in docs['news']:
            f.write("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _" + "\n")
            f.write(news[doc]['vanilla'] + "\n")

    f.close()


d1 = datetime.date(2018, 10, 16)  # start date
d2 = datetime.date(2018, 10, 18)  # end date
dates = get_dates_between(d1, d2)

# for date in dates:
news = read_preprocessed_news_for_dates(dates)
# print_number_of_news_clusters_and_texts(news, date)
print_story_clustering_per_day(news, "16-18")


# dates = get_dates_between(d1, d2)
# tf_idf_keywords_threshold = 0.2
# news = read_preprocessed_news_for_dates(dates)
# extract_keywords_from_news(news, tf_idf_keywords_threshold)
#
# for tf_idf_keywords_threshold in numpy.arange(0.5, 0.7, 0.05):
#     extract_keywords_from_news(news, tf_idf_keywords_threshold)
#     for story in news:
#         if story['documentId'] == 68681692247385:
#             print('tf-idf: ' + str(story['keywords_t']))
#             print('________________')
#             print(str(len(story['vanilla'].split())))
