import re
from pprint import pprint

import pandas as pd

import pymorphy2
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from stop_words import get_stop_words


url_regexp = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'


def prepocess_string(string):
    res = ""
    morph = pymorphy2.MorphAnalyzer()
    for word in string.split():
        if not re.match(url_regexp, word):
            res = res + " " + morph.parse(word)[0].normalized.normal_form
    return res


def get_tf_idf(texts, use_idf):
    texts = list(map(lambda t: prepocess_string(t), texts))
    ru_stop_words = get_stop_words('russian')
    vectorizer = TfidfVectorizer(use_idf=use_idf,
                        stop_words=ru_stop_words,
                        analyzer='word',
                        ngram_range=(1, 1),
                        min_df=0)

    vectorizer.fit(texts)
    return vectorizer.transform(texts).toarray()


def get_vectors(text):
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()