from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from stop_words import get_stop_words

from summa import keywords
from gensim.summarization import keywords


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, T):
    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        if score > T:
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


def get_keywords_for_doc(doc, cv, X, T):
    feature_names = cv.get_feature_names()

    tfidf_transformer=TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)

    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    return extract_topn_from_vector(feature_names, sorted_items, T)


def extract_keywords_from_news_tf_idf(news, T):
    stop_words = get_stop_words('russian')
    corpus = list(map(lambda story: story["normalized"], news))
    cv=CountVectorizer(max_df=0.8, stop_words=stop_words, max_features=10000, ngram_range=(1,1))
    X=cv.fit_transform(corpus)

    for story in news:
        doc = story["normalized"]
        story['keywords_t'] = list(get_keywords_for_doc(doc, cv, X, T)) #(pair of key, score) for k in keywords: print(k, keywords[k])


def extract_keywords_from_story_ranktext(story):
    doc = story["normalized"]
    keys = []
    for k in keywords(doc).split():
        keys = keys + k.split()
    story['keywords_r'] = keys


def extract_keywords_from_news_ranktext(news):
    for story in news:
        extract_keywords_from_story_ranktext(story)


def extract_keywords_from_news_rake(news):
    r = Rake(stopwords=get_stop_words('russian'), min_length=1, max_length=1)
    for story in news:
        doc = story["normalized"]
        keys = []
        for k in r.extract_keywords_from_text(doc):
            keys = keys + k.split()
        story['keywords'] = set(keys)


def extract_keywords_from_news(news, T):
    extract_keywords_from_news_tf_idf(news, T)
    for story in news:
        keywords_t = list(map(lambda w: w.strip(), story['keywords_t']))
        keywords_r = list(map(lambda w: w.strip(), story['keywords_r']))
        persons = list(map(lambda w: w.strip(), story['persons']))
        locations = list(map(lambda w: w.strip(), story['locations']))
        story['keywords'] = list(set(keywords_t + keywords_r + locations) - {'россия', 'украина', 'владимир', "владимир"})