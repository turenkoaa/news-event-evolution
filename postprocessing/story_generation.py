import datetime
from keywords_based.newslen_clustering import get_stories_for_dates
from preprocessing.read_news import get_dates_between


def get_intersection_percentage_of_clusters(cluster1, cluster2):
    if not len(cluster1) == 0 and not len(cluster2) == 0:
        return float(len(set(cluster1).intersection(set(cluster2)))) / len(cluster2)
    else:
        return 0.


def map_clusters_to_ids(data, dates):
    clusters = {}
    for cluster in data['stories']:
        ids = []
        for date in dates:
            for event in cluster['events'][date]:
                for story in event['event']:
                    ids.append(story['documentId'])
        clusters[cluster['storyId']] = {
            'ids': ids,
            'cluster': cluster
        }
    return clusters



d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 16)
step = 3
window = 5

d1_window = d1 + datetime.timedelta(step)
d2_window = d1_window + datetime.timedelta(window)
dates_intersect = get_dates_between(d1_window, d2)

old_clusters = get_stories_for_dates(d1, d2)
new_clusters = get_stories_for_dates(d1_window, d2_window)


old_stories = map_clusters_to_ids(old_clusters, dates_intersect)
new_stories = map_clusters_to_ids(new_clusters, dates_intersect)

to_link = {}
for old_id in old_stories:
    for new_id in new_stories:
        intersection = get_intersection_percentage_of_clusters(old_stories[old_id]['ids'], new_stories[new_id]['ids'])
        if intersection > 0.5:
            if old_id in to_link.keys():
                to_link[old_id].append(new_id)
            else:
                to_link[old_id] = [new_id]

print(to_link)


def merge(old_cluster, to_merge):
    print(to_merge)


for old_cluster in old_clusters['stories']:
    storyId = old_cluster['storyId']
    if old_cluster['storyId'] in to_link.keys():
        merge(old_cluster, map(lambda id: new_stories[id]['cluster'], to_link[storyId]))







