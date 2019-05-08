import datetime
import json
import os
import re

from langdetect import detect_langs

from keywords_based.keywords_from_news import extract_keywords_from_news, extract_keywords_from_story_ranktext
from keywords_extractor import get_persons, get_locations
from normalize_word import prepocess_string


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


def read_cluster(news, cluster_id):
    return list(filter(lambda n: n["clusterId"] == cluster_id, news))


def get_filtered_news_file(date):
    return "C:/Users/User/Desktop/diploma/ner/data/filtered_news_" + date


def get_preprocessed_data_file(date):
    return "C:/Users/User/Desktop/diploma/ner/preprocessed_data/" + date


def get_preprocessed_officialGroup_data_file(date):
    return "C:/Users/User/Desktop/diploma/ner/preprocessed_official_group_1/" + date


def extract_nornalized_texts(news):
    for story in news:
        story['normalized'] = prepocess_string(story['vanilla'])
        extract_keywords_from_story_ranktext(story)


def preprocess_news(date):
    spam = get_spam_clusters(date, 0.5)
    filepath = get_file_for_date("C:/Users/User/Desktop/diploma/datasets/outerTrendsDataset/texts/date=" + date + "/")
    print("processing file: " + filepath)
    with open(filepath, encoding="utf8") as f:
        lines = f.readlines()
        news = []
        for line in lines:
            story = json.loads(line)
            if filter_doc(story, spam):
                story["date"] = date
                story["persons"] = get_persons(story["vanilla"])
                story["locations"] = get_locations(story["vanilla"])
                story['normalized'] = prepocess_string(story['vanilla'])
                extract_keywords_from_story_ranktext(story)
                news.append(story)

        print(str(len(news)) + "/" + str(len(lines)) + " filtered news were found for date=" + date)
    return news


def read_preprocessed_news(date):
    with open(get_preprocessed_officialGroup_data_file(date), 'r', encoding="utf8") as fp:
        news = json.load(fp)
        return news


def clear_common_news(news):
    extract_keywords_from_news(news, 0.246)
    news_to_ignore = []
    for story in news:
        if len(story['keywords_t']) == 0 and len(story['persons'] + story['locations']) > 3:
            news_to_ignore.append(story['documentId'])
    for doc in news:
        if doc['documentId'] in news_to_ignore:
            news.remove(doc)
            # print(doc['vanilla'])
            # print("_______")


def read_preprocessed_news_for_dates(dates):
    result = []
    for date in dates:
        result = result + read_preprocessed_news(date)

    for i, story in enumerate(result):
        result[i]['index'] = i

    if len(dates) > 6:
        clear_common_news(result)
    return result


def read_news_for_dates(dates):
    result = {}
    for date in dates:
        result[date] = read_preprocessed_news(date)

    # for k in result.items():
    #     for story in result[k]:
    #         story['index'] = i

    return result


def write_preprocessed_news(date):
    news = read_preprocessed_news(date)
    for story in news:
        story['normalized'] = prepocess_string(story['vanilla'])
        uniq = []
        for k in story['persons']:
            uniq = uniq + k.split()
        story['persons'] = list(set(uniq))

        uniq = []
        for k in story['locations']:
            uniq = uniq + k.split()
        story['locations'] = list(set(uniq))

        extract_keywords_from_story_ranktext(story)

    with open("C:/Users/User/Desktop/diploma/ner/preprocessed_1/" + date, 'w', encoding="utf8") as fp:
        json.dump(news, fp, ensure_ascii=False)


# d1 = datetime.date(2018, 10, 10)
# d2 = datetime.date(2018, 12, 31)
# dates = get_dates_between(d1, d2)
# for date in dates:
#     print("date: " + str(date))
#     write_preprocessed_news(date)





