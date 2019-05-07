import datetime
from keywords_based.newslen_clustering import get_stories_for_dates
from read_news import get_dates_between


def get_intersection_percentage_of_clusters(cluster1, cluster2):
    return float(len(set(cluster1).intersection(set(cluster2)))) / len(cluster2)


def get_news_ids_for_dates_from_cluster(story_cluster, d1, d2):
    dates = get_dates_between(d1, d2)
    ids = []
    for date in dates:
        ids = ids + list(map(lambda story: story['documentId'], story_cluster['events'][date]))
    return ids


d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 16)
step = 3
window = 5

d1_window = d1 + datetime.timedelta(step)
d2_window = d1_window + datetime.timedelta(window)

clusters1 = get_stories_for_dates(d1, d2)
clusters2 = get_stories_for_dates(d1_window, d2_window)

d1_intersect = d1_window
d2_intersect = d2_window


for cluster1 in clusters1:
    ids1 = get_news_ids_for_dates_from_cluster(clusters1, d1_intersect, d2_intersect)
    for cluster2 in clusters2:
        ids2 = get_news_ids_for_dates_from_cluster(clusters2, d1_intersect, d2_intersect)
        intersection = get_intersection_percentage_of_clusters(ids1, ids2)
        if intersection > 0.5:
            link






