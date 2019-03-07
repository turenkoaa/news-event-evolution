import datetime
import pandas as pd
from keywords_extractor import get_keywords, get_persons, get_locations
from ner import TextFeatures
import json
from pprint import pprint

from read_news import get_russian_news, get_dates_between


d1 = datetime.date(2018, 10, 11)  # start date
d2 = datetime.date(2018, 10, 21)  # end date

dates = get_dates_between(d1, d2)

persons = []
locations = []
for date in dates:
    news = get_russian_news(date)
    for story in news:
        vanilla = story['vanilla']
        new_persons = get_persons(vanilla)
        print(str(len(new_persons)) + " persons were found for story=" + str(story['documentId']))
        persons = persons + new_persons

        new_locations = get_locations(vanilla)
        print(str(len(new_locations)) + " locations were found for story=" + str(story['documentId']))
        locations = locations + new_locations


dfp = pd.DataFrame([t.__dict__ for t in persons])
dfp.to_csv("C:/Users/User/Desktop/diploma/results/persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
dfp.groupby(['full']).size().sort_values(ascending=False).to_csv("C:/Users/User/Desktop/diploma/results/top_persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')

dfl = pd.DataFrame([t.__dict__ for t in locations])
dfl.to_csv("C:/Users/User/Desktop/diploma/results/persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
dfl.groupby(['location']).size().sort_values(ascending=False).to_csv("C:/Users/User/Desktop/diploma/results/top_persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')
