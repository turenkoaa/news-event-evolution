import datetime
import pandas as pd
from read_news import get_dates_between, read_preprocessed_news
from similarity import cosine_sim, jaccard_sim, get_jaccard_locations_sim, get_jaccard_persons_sim, \
    get_cosine_persons_sim, get_cosine_locations_sim, get_cosine_text_sim

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 17)  # end date
dates = get_dates_between(d1, d2)

for date in dates:
    news = read_preprocessed_news(date)
    jaccard_locations_sim = get_jaccard_locations_sim(news)
    jaccard_persons_sim = get_jaccard_persons_sim(news)
    cosine_persons_sim = get_cosine_persons_sim(news)
    cosine_locations_sim = get_cosine_locations_sim(news)
    cosine_text_sim = get_cosine_text_sim(news)

    texts_count = len(news)

    count_cluster_sim = 0
    count_top_sim = 0
    for i in range(0, texts_count):
        for j in range(i + 1, texts_count):
            if cosine_text_sim[i][j] > 0.5:
                print(str(i) + ": cluster=" + str(news[i]["clusterId"]) + " locations: " + str(news[i]["locations"]) + " persons: " + str(news[i]["persons"]))  # + " text: " + news[i]["vanilla"])
                print(str(j) + ": cluster=" + str(news[j]["clusterId"]) + " locations: " + str(news[j]["locations"]) + " persons: " + str(news[j]["persons"]))  # + " text: " + news[j]["vanilla"])
                print("cosine_text_sim=" + str(cosine_text_sim[i][j]))
                print("jaccard_locations_sim=" + str(jaccard_locations_sim[i][j]))
                print("cosine_locations_sim=" + str(cosine_locations_sim[i][j]))
                print("jaccard_persons_sim=" + str(jaccard_persons_sim[i][j]))
                print("cosine_persons_sim=" + str(cosine_persons_sim[i][j]))
                print("\n")


def get_entities_to_exclude(dates):
    exclude_locations = []
    exclude_persons = []

    for date in dates:
        news = read_preprocessed_news(date)
        jaccard_locations_sim = get_jaccard_locations_sim(news)
        jaccard_persons_sim = get_jaccard_persons_sim(news)
        cosine_persons_sim = get_cosine_persons_sim(news)
        cosine_locations_sim = get_cosine_locations_sim(news)
        cosine_text_sim = get_cosine_text_sim(news)

        texts_count = len(news)
        for i in range(0, len(news)):
            for j in range(i + 1, texts_count):
                if news[i]["clusterId"] != news[j]["clusterId"] and cosine_text_sim[i][j] < 0.3:
                    if cosine_persons_sim[i][j] > 0.8:
                        exclude_persons = exclude_persons + list(
                            set.intersection(set(news[i]["persons"]), set(news[j]["persons"])))

                    if cosine_locations_sim[i][j] > 0.7:
                        exclude_locations = exclude_locations + list(
                            set.intersection(set(news[i]["locations"]), set(news[j]["locations"])))

        return exclude_persons, exclude_locations

exclude_persons, exclude_locations = get_entities_to_exclude(dates)
dfl = pd.DataFrame(exclude_locations, columns=['exclude_locations'])
dfl.groupby(['exclude_locations']).size().sort_values(ascending=False).to_csv("C:/Users/User/Desktop/diploma/results/exclude_locations_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')

dfp = pd.DataFrame(exclude_persons, columns=['exclude_persons'])
dfp.groupby(['exclude_persons']).size().sort_values(ascending=False).to_csv("C:/Users/User/Desktop/diploma/results/exclude_persons_" + d1.strftime('%Y-%m-%d') + "_" + d2.strftime('%Y-%m-%d') + ".csv", sep='\t', encoding='utf-8')



