import datetime

from read_news import get_dates_between, read_preprocessed_news_for_dates
from similarity import nallapati_sim
from story_clustering import calculate_events_data, story_clustering_to_events

dates = get_dates_between(datetime.date(2018, 10, 17), datetime.date(2018, 10, 23))
w = [1, 0, 0]
t = 0.35 # 0.1

news = read_preprocessed_news_for_dates(dates)
print("amount of news:" + str(len(news)))
max_events_number = len(set(map(lambda n: n["clusterId"], news))) * 1.5
sim = nallapati_sim(news, w, 1, 1)  # get_cosine_text_sim(news)
print("Start story clustering...")

events = story_clustering_to_events(sim, t, max_events_number)
for key in events:
    print(">>>> " + str(key))
    for doc in events[key]:
        print(news[doc]['vanilla'])
        print('_________________')