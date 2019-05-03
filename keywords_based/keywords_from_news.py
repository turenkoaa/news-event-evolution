from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from stop_words import get_stop_words

from normalize_word import prepocess_string


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


def extract_keywords_from_news(news, T):
    stop_words = get_stop_words('russian')
    corpus = list(map(lambda story: prepocess_string(story["vanilla"]), news))
    cv=CountVectorizer(max_df=0.8, stop_words=stop_words, max_features=10000, ngram_range=(1,1))
    X=cv.fit_transform(corpus)

    for story in news:
        doc = prepocess_string(story["vanilla"])
        story['keywords'] = get_keywords_for_doc(doc, cv, X, T) #(pair of key, score) for k in keywords: print(k, keywords[k])

