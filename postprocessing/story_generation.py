import datetime
import json

from content_based.main import get_stories_for_dates_content
from keywords_based.newslen_clustering import get_stories_for_dates
from preprocessing.read_news import get_dates_between


def get_intersection_percentage_of_clusters(cluster1, cluster2):
    if not len(cluster1) == 0 and not len(cluster2) == 0:
        return float(len(set(cluster1).intersection(set(cluster2)))) / len(cluster2)
    else:
        return 0.


def map_clusters_to_ids(data, dates):
    clusters = {}
    for cluster in data:
        ids = []
        for date in dates:
            for story in cluster['events'][date]:
                ids.append(story['documentId'])
        clusters[cluster['storyId']] = {
            'ids': ids,
            'cluster': cluster['events']
        }
    return clusters


d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 17)
end_date = datetime.date(2018, 10, 17)
step = 7
window = 6
old_clusters = get_stories_for_dates_content(d1, d2)['stories']


while True:
    d1_window = d1 + datetime.timedelta(step)
    d2_window = d1_window + datetime.timedelta(window)

    if d2_window > end_date:
        break

    dates_intersect = get_dates_between(d1_window, d2)
    dates_union = get_dates_between(d1_window, d2_window)

    new_clusters = get_stories_for_dates(d1_window, d2_window)['stories']

    for old_cluster in old_clusters:
        for date in dates_union:
            if not date in old_cluster['events'].keys():
                old_cluster['events'][date] = []

    old_clusters_index = map_clusters_to_ids(old_clusters, dates_intersect)
    new_clusters_index = map_clusters_to_ids(new_clusters, dates_intersect)

    to_link = {}
    for old_id in old_clusters_index:
        for new_id in new_clusters_index:
            intersection = get_intersection_percentage_of_clusters(old_clusters_index[old_id]['ids'], new_clusters_index[new_id]['ids'])
            if intersection > 0.5:
                if old_id in to_link.keys():
                    to_link[old_id].append(new_id)
                else:
                    to_link[old_id] = [new_id]

    for to_merge_id, from_merge_ids in to_link.items():
        to_merge_cluster = old_clusters_index[to_merge_id]['cluster']

        from_merge_clusters = list(map(lambda id: new_clusters_index[id]['cluster'], from_merge_ids))

        for date in dates_union:
            docs = to_merge_cluster[date]
            docsIds = list(map(lambda doc: doc['documentId'], docs))

            for from_merge_cluster in from_merge_clusters:
                for mergeDoc in from_merge_cluster[date]:
                    if not mergeDoc['documentId'] in docsIds:
                        to_merge_cluster[date].append(mergeDoc)

    merged = []
    for storiesIds in to_link.values():
        merged = merged + storiesIds
    for key in new_clusters_index:
        if key not in merged:
            old_clusters.append({
                'storyId': key,
                'events': new_clusters_index[key]['cluster']
            })

    d1 = d1_window
    d2 = d2_window


with open("C:/Users/User/Desktop/diploma/ner/data/results/keywords_based/stories/fu.json", "w", encoding="utf8") as write_file:
    json.dump(old_clusters, write_file, ensure_ascii=False)







