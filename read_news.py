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

def get_file_for_date(dirname):
    filename = os.listdir(dirname)[0]
    root, ext = os.path.splitext(filename)
    return dirname + filename if ext == '.json' else None

def get_russian_news(date):
    filepath = get_file_for_date("C:/Users/User/Desktop/diploma/datasets/outerTrendsDataset/texts/date=" + date + "/")
    print("processing file: " + filepath)
    with open(filepath, encoding="utf8") as f:
        lines = f.readlines()
        news = list(map(lambda line: json.loads(line), lines))
        russian_news = list(filter(lambda n: is_lang(n['vanilla'], "ru", 0.70), news))
        print(str(len(russian_news)) + "/" + str(len(lines)) + " russian news were found for date=" + date)
        return russian_news

def get_dates_between(d1, d2):
    delta = d2 - d1         # timedelta
    dates = []
    for i in range(delta.days + 1):
        dt = d1 + datetime.timedelta(i)
        dates.append(dt.strftime("%Y-%m-%d"))
    return dates




