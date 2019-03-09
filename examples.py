import datetime
import pandas as pd

from read_news import get_dates_between
from similarity import get_cosine_text_sim
from keywords_extractor import get_keywords, get_Persons, get_locations, get_Locations

d1 = datetime.date(2018, 10, 11)  # start date
d2 = datetime.date(2018, 12, 31)  # end date
dates = get_dates_between(d1, d2)

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
