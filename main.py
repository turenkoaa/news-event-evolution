import datetime
import pandas as pd
import numpy as np
from keywords_extractor import get_keywords, get_Persons, get_locations, get_Locations
from read_news import filter_news, get_dates_between, read_filtered_news
from similarity import cosine_sim, jaccard_sim, get_jaccard_locations_sim, get_jaccard_persons_sim, \
    get_cosine_persons_sim

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 10)  # end date
dates = get_dates_between(d1, d2)

exclude_words = []

# date = d1.strftime("%Y-%m-%d"))
for date in dates:

    news = read_filtered_news(date)
    sim, entities = get_jaccard_locations_sim(news)

    texts_count = len(news)

    count_cluster_sim = 0
    count_top_sim = 0
    for i in range(0, texts_count):
        for j in range(i + 1, texts_count):
            if news[i]["clusterId"] != news[j]["clusterId"]:
                exclude_words = exclude_words + list(set.intersection(entities[i], entities[j]))

    #         if sim[i][j] > 0.7:
    #             count_top_sim += 1
    #             if news[i]["clusterId"] == news[j]["clusterId"]:
    #                 count_cluster_sim += 1
    #
    #             print(sim[i][j])
    #             print(str(i) + ": cluster=" + str(news[i]["clusterId"]) + " persons: " + str(entities[i])) # + " text: " + news[i]["vanilla"])
    #             print(str(j) + ": cluster=" + str(news[j]["clusterId"]) + " persons: " + str(entities[j])) # + " text: " + news[j]["vanilla"])
    #             print("\n")
    #
    # print(date + ": cluster sim=" + str(count_cluster_sim/count_top_sim))

dfp = pd.DataFrame(exclude_words, columns=['exclude_words'])
dfp.groupby(['exclude_words']).size().sort_values(ascending=False).to_csv("C:/Users/User/Desktop/diploma/results/exclude_locations_jaccard_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')



