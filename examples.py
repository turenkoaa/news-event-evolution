import datetime
import pandas as pd

from read_news import get_dates_between, read_preprocessed_news
from similarity import get_cosine_text_sim
from keywords_extractor import get_keywords, get_Persons, get_locations, get_Locations

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 10)  # end date
dates = get_dates_between(d1, d2)

news = read_preprocessed_news(dates[0])

###############################################################################
# cosine sim example

# text = ["AI is our friend and it has been friendly",
# "AI and humans have always been friendly",
# "AI and humans have always been friendly"]
#
# cosine_sim = get_cosine_sim(text)
# print(cosine_sim)
# i, j = 0, 2
# print(text[i] + " && " + text[j] + " have sim=" + str(cosine_sim[i][j]))

###############################################################################
# extract entities example

# text = '''
# Так говорила в июле 1805 года известная Анна Павловна Шерер, фрейлина и приближенная императрицы Марии Феодоровны, встречая важного и чиновного князя Василия, первого приехавшего на ее вечер. Анна Павловна кашляла несколько дней, у нее был грипп, как она говорила (грипп был тогда новое слово, употреблявшееся только редкими).
#
# Предлагаю вернуть прежние границы природного парка №71 на Инженерной улице 2.
#
# По адресу Алтуфьевское шоссе д.51 (основной вид разрешенного использования: производственная деятельность, склады) размещен МПЗ. Жители требуют незамедлительной остановки МПЗ и его вывода из района
#
# Контакты О нас телефон 7 881 574-10-02 Адрес Республика Карелия,г.Петрозаводск,ул.Маршала Мерецкова, д.8 Б,офис 4
#
# Благодарственное письмо   Хочу поблагодарить учителей моего, теперь уже бывшего, одиннадцатиклассника:  Бушуева Вячеслава Владимировича и Бушуеву Веру Константиновну. Они вовлекали сына в интересные внеурочные занятия, связанные с театром и походами.
#
# Вячеслава
#
# По адресу Алтуфьевское шоссе д.51 (основной вид разрешенного использования: производственная деятельность, склады) размещен МПЗ. Жители требуют незамедлительной остановки МПЗ и его вывода из района
#
# Контакты О нас телефон 7 881 574-10-02 Адрес Республика Карелия,г.Петрозаводск,ул.Маршала Мерецкова, д.8 Б,офис 4
#
# Благодарственное письмо   Хочу поблагодарить учителей моего, теперь уже бывшего, одиннадцатиклассника:  Бушуева Вячеслава Владимировича и Бушуеву Веру Константиновну. Они вовлекали сына в интересные внеурочные занятия, связанные с театром и походами.
# '''
# names = get_Persons(text)
# df = pd.DataFrame([t.__dict__ for t in names])
# print(df.groupby(['full']).size().sort_values(ascending=False).head(10))
# df.to_csv("C:/Users/User/Desktop/diploma/ner/result.scv", sep='\t', encoding='utf-8')
#
# df = pd.DataFrame([t.__dict__ for t in get_locations(text)])
# print(df.groupby(['location']).size().sort_values(ascending=False).head(10))
# df.to_csv("C:/Users/User/Desktop/diploma/ner/result.scv", sep='\t', encoding='utf-8')

###############################################################################
# rewrite filtered news

# for date in dates:
#     write_filtered_news_to_file(date)

###############################################################################
# get top locations and named entities

# persons = []
# locations = []
# for date in dates:
#     news = filter_news(date)
#     for story in news:
#         vanilla = story['vanilla']
#         new_persons = get_Persons(vanilla)
#         print(str(len(new_persons)) + " persons were found for story=" + str(story['documentId']))
#         persons = persons + new_persons
#
#         new_locations = get_Locations(vanilla)
#         print(str(len(new_locations)) + " locations were found for story=" + str(story['documentId']))
#         locations = locations + new_locations
#
#
# dfp = pd.DataFrame([t.__dict__ for t in persons])
# dfp.to_csv("C:/Users/User/Desktop/diploma/results/persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
# dfp.groupby(['full']).size().sort_values(ascending=False).to_csv("C:/Users/User/Desktop/diploma/results/top_persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
#
# dfl = pd.DataFrame([t.__dict__ for t in locations])
# dfl.to_csv("C:/Users/User/Desktop/diploma/results/persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
# dfl.groupby(['location']).size().sort_values(ascending=False).to_csv("C:/Users/User/Desktop/diploma/results/top_persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')

#############################################################
# sort entities to exclude from lists for story

# def get_entities_to_exclude(dates):
#     exclude_locations = []
#     exclude_persons = []
#
#     for date in dates:
#         news = read_preprocessed_news(date)
#         jaccard_locations_sim = get_jaccard_locations_sim(news)
#         jaccard_persons_sim = get_jaccard_persons_sim(news)
#         cosine_persons_sim = get_cosine_persons_sim(news)
#         cosine_locations_sim = get_cosine_locations_sim(news)
#         cosine_text_sim = get_cosine_text_sim(news)
#
#         texts_count = len(news)
#         for i in range(0, len(news)):
#             for j in range(i + 1, texts_count):
#                 if news[i]["clusterId"] != news[j]["clusterId"] and cosine_text_sim[i][j] < 0.3:
#                     if cosine_persons_sim[i][j] > 0.8:
#                         exclude_persons = exclude_persons + list(
#                             set.intersection(set(news[i]["persons"]), set(news[j]["persons"])))
#
#                     if cosine_locations_sim[i][j] > 0.7:
#                         exclude_locations = exclude_locations + list(
#                             set.intersection(set(news[i]["locations"]), set(news[j]["locations"])))
#
#         dfl = pd.DataFrame(exclude_locations, columns=['exclude_locations'])
#         dfl.groupby(['exclude_locations']).size().sort_values(ascending=False).to_csv(
#             "C:/Users/User/Desktop/diploma/results/exclude_locations_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime(
#                 '%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
#
#         dfp = pd.DataFrame(exclude_persons, columns=['exclude_persons'])
#         dfp.groupby(['exclude_persons']).size().sort_values(ascending=False).to_csv(
#             "C:/Users/User/Desktop/diploma/results/exclude_persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime(
#                 '%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
#
#         return exclude_persons, exclude_locations


###############################################################
# calculate similarities for two stories (with comparing their clusters ids)
# def count_sims(news):
#     texts_count = len(news)
#
#     # jaccard_locations_sim = get_jaccard_locations_sim(news)
#     # jaccard_persons_sim = get_jaccard_persons_sim(news)
#     # cosine_persons_sim = get_cosine_persons_sim(news)
#     # cosine_locations_sim = get_cosine_locations_sim(news)
#     cosine_text_sim = get_cosine_text_sim(news)
#
#     count_cluster_sim = 0
#     count_top_sim = 0
#     for i in range(0, texts_count):
#         for j in range(i + 1, texts_count):
#             if cosine_text_sim[i][j] > 0.5:
#                 print(str(i) + ": cluster=" + str(news[i]["clusterId"]) + " text: " + news[i]["vanilla"]) # + " locations: " + str(news[i]["locations"]) + " persons: " + str(news[i]["persons"]))
#                 print(str(j) + ": cluster=" + str(news[j]["clusterId"]) + " text: " + news[j]["vanilla"]) # + " locations: " + str(news[j]["locations"]) + " persons: " + str(news[j]["persons"]))
#                 print("cosine_text_sim=" + str(cosine_text_sim[i][j]))
#                 # print("jaccard_locations_sim=" + str(jaccard_locations_sim[i][j]))
#                 # print("cosine_locations_sim=" + str(cosine_locations_sim[i][j]))
#                 # print("jaccard_persons_sim=" + str(jaccard_persons_sim[i][j]))
#                 # print("cosine_persons_sim=" + str(cosine_persons_sim[i][j]))
#                 print("\n")
#
# count_sims(news)