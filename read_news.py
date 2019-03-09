import datetime
import json
import os
from langdetect import detect_langs


def is_lang(text, lang, prob): # print(is_lang("Smth", "ru", 0.75))
    try:
        list_of_languages = detect_langs(text)
        return len(list_of_languages) > 0 and list_of_languages[0].lang == lang and list_of_languages[0].prob > prob
    except Exception:
        print("error in detecting language for text: \"" + text + "\"")
        return False

def filter_doc(doc, spam):
    return doc["clusterId"] not in spam and is_lang(doc["vanilla"], "ru", 0.70)
    # return doc["officialGroup"] and doc["clusterId"] not in spam and is_lang(doc["vanilla"], "ru", 0.70)

def get_file_for_date(dirname):
    filename = os.listdir(dirname)[0]
    root, ext = os.path.splitext(filename)
    return dirname + filename if ext == '.json' else None

def get_spam_clusters(date, threshold):
    trends_path = get_file_for_date("C:/Users/User/Desktop/diploma/datasets/outerTrendsDataset/trends/date=" + date + "/")
    print("processing for spam file: " + trends_path)
    with open(trends_path, encoding="utf8") as trends:
        spam = []
        trends_lines = trends.readlines()
        for trends_line in trends_lines:
            trends_json = json.loads(trends_line)
            if trends_json["percentIsSpam"] > threshold:
                spam.append(trends_json["clusterId"])
        print(str(len(spam)) + " spam clusters were found")
        return spam

def get_dates_between(d1, d2):
    delta = d2 - d1         # timedelta
    dates = []
    for i in range(delta.days + 1):
        dt = d1 + datetime.timedelta(i)
        dates.append(dt.strftime("%Y-%m-%d"))
    return dates

def get_filtered_news(date):
    spam = get_spam_clusters(date, 0.5)
    filepath = get_file_for_date("C:/Users/User/Desktop/diploma/datasets/outerTrendsDataset/texts/date=" + date + "/")
    print("processing file: " + filepath)
    with open(filepath, encoding="utf8") as f:
        lines = f.readlines()
        news = list(map(lambda line: json.loads(line), lines))
        filtered_news = list(filter(lambda n: filter_doc(n, spam), news))
        print(str(len(filtered_news)) + "/" + str(len(lines)) + " filtered news were found for date=" + date)
        return filtered_news

def read_cluster(news, cluster_id):
    return list(filter(lambda n: n["clusterId"] == cluster_id, news))


def get_filtered_news_file(date):
    return "C:/Users/User/Desktop/diploma/ner/data/filtered_news_" + date


def write_filtered_news_to_file(date):
    news = get_filtered_news(date)
    with open(get_filtered_news_file(date), 'w', encoding="utf8") as fp:
        json.dump(news, fp, ensure_ascii=False)


def read_filtered_news_from_file(date):
    with open(get_filtered_news_file(date), 'r', encoding="utf8") as fp:
        return json.load(fp)

# d1 = datetime.date(2018, 10, 10)  # start date
# d2 = datetime.date(2018, 12, 31)  # end date
# dates = get_dates_between(d1, d2)


# news = read_filtered_news_from_file(d1)
# for i in range(1,5):
#     cluster = read_cluster(news, i)
#     for doc in cluster:
#         print(doc["vanilla"])
#         print("// cluster_id=" + str(doc["clusterId"]))
#     print("____________________________________________________________")




