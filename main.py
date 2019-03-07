import datetime
import pandas as pd
from keywords_extractor import get_keywords, get_names
from ner import TextFeatures
import json
from pprint import pprint

from read_news import get_russian_news, get_dates_between


d1 = datetime.date(2018, 10, 11)  # start date
d2 = datetime.date(2018, 10, 21)  # end date

dates = get_dates_between(d1, d2)

names = []
for date in dates:
    news = get_russian_news(date)
    for story in news:
        new_names = get_names(story['vanilla'])
        print(str(len(new_names)) + " persons were found for story=" + str(story['documentId']))
        names = names + new_names

df = pd.DataFrame([t.__dict__ for t in names])
df.to_csv("C:/Users/User/Desktop/diploma/ner/result.csv", sep='\t', encoding='utf-8')
df.groupby(['full']).size().sort_values(ascending=False).head(100).to_csv("C:/Users/User/Desktop/diploma/ner/result2.csv", sep='\t', encoding='utf-8')
