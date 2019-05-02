from sklearn.metrics.pairwise import cosine_similarity

from read_news import get_dates_between, read_preprocessed_news_for_dates
from pylab import *
from story_clustering import calculate_events_data
from visualization import draw_graph

d1 = datetime.date(2018, 10, 17)  # start date
d2 = datetime.date(2018, 10, 19)  # end date
dates = get_dates_between(d1, d2)
w = [0.7, 0.15, 0.15]
t = 0.2 # 0.1

news = read_preprocessed_news_for_dates(dates)
print("amount of news:" + str(len(news)))
events_data = calculate_events_data(news, w, t)

threshold = 0.3
events_sim = cosine_similarity(events_data['event_term_vectors'])

for i in range(len(events_sim)):
    for j in range(0, i):
        events_sim[i][j] = 0

result = np.argwhere(events_sim > threshold)

events = events_data['events']
for key in events:
    print(">>>> " + str(key))
    for doc in events[key]:
        print(news[doc]['vanilla'])
        print('_________________')


draw_graph(result.T[0], result.T[1])


# for pair in result:
#     for storyNum in events_data['events'][pair[0]]:
#         print(news[storyNum]['vanilla'])
#         print("_ _ _ _ _ _ _ _ _ _ _ _")
#     print("_______________________")
#     for storyNum in events_data['events'][pair[1]]:
#         print(news[storyNum]['vanilla'])
#         print("_ _ _ _ _ _ _ _ _ _ _ _")
#     print(news[pair[1]]['vanilla'])
#     print("_______________________")
#     print("_______________________")


