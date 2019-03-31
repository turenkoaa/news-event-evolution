from __future__ import print_function
import scipy.stats as st
from pylab import *

from read_news import read_cluster, read_preprocessed_news, get_dates_between
from similarity import get_cosine_text_sim


d1 = datetime.date(2018, 10, 11)  # start date
d2 = datetime.date(2018, 10, 11)  # end date
dates = get_dates_between(d1, d2)

news = read_preprocessed_news(dates[0])
clusterIds = list(set(map(lambda s: s["clusterId"], news)))
for clusterId in clusterIds[0:1]:
    cluster = read_cluster(news, clusterId)
    m = get_cosine_text_sim(cluster)
    ar = []
    for i in range(0, len(cluster)):
        for j in range(i + 1, len(cluster)):
            ar.append(m[i][j])
    sample = sorted(ar)
    print(sample)

    # отрисовка гистограммы с 20-ю разбиениями интервала значений выборки
    # bins - это число столбцов гистограммы, включая столбцы нулевой высоты
    figure()
    hist(sample, bins=20)

    # # Вычисление важных показателей
    # n, m, minmax, s, cv, perct, mode, skew, kurt, kde = descriptive1d(sample)
    #
    # print('Число элементов выборки: {0:d}'.format(n))
    # print('Среднее значение: {0:.4f}'.format(m))
    # print('Минимальное и максимальное значения: ({0:.4f}, {1:.4f})'.format(*minmax))
    # print('Стандартное отклонение: {0:.4f}'.format(s))
    # print('Коэффициент вариации (Пирсона): {0:.4f}'.format(cv))
    # print('Квартили: (25%) = {0:.4f}, (50%) = {1:.4f}, (75%) = {2:.4f}'.format(*perct))
    # print('Коэффициент асимметрии: {0:.4f}'.format(skew))
    # print('Коэффициент эксцесса: {0:.4f}'.format(kurt))
    #
    # # Отрисовка оценки плотности распределения
    # figure()
    # plot(kde[0], kde[1])
    # title('pdf-estimation')
    # show()

    # matrix = nallapati_sim(news, [w1, w2/2, w2/2], alpha, time_delta)

# Нахождение базовых статистических показателей (описательная статистика)
def descriptive1d(x):
    _x = x  # Для возможности предобработки данных (например, исключения нечисловых значений)
    result = []
    result.append(len(x)) # Чисо элементов выборки
    result.append(np.mean(_x)) # среднее
    result.append((np.min(_x), np.max(_x))) # (min, max)
    result.append(np.std(_x)) # стандартное отклонение
    result.append(100.0 * result[-1]/result[0]) # коэффициент вариации (Пирсона)
    result.append((np.percentile(_x, 25), np.percentile(_x, 50), np.percentile(_x, 75))) # квартили
    result.append(st.mode(_x))  # мода
    result.append(st.skew(_x))  # асимметрия
    result.append(st.kurtosis(_x))  # эксцесс
    _range = np.linspace(0.9 * np.min(_x), 1.1 * np.max(_x), 100) # область определения для оценки плотности
    result.append((_range, st.gaussian_kde(_x)(_range)))  # оценка плотности распределения
    return tuple(result)



# # формирование двухвершинного (двумодового) распределени из пары нормальных
# sample = np.hstack((1.5 * np.random.rand(200).ravel(), 2 + 1.2 * np.random.rand(300)))

# отрисовка гистограммы с 20-ю разбиениями интервала значений выборки
# bins - это число столбцов гистограммы, включая столбцы нулевой высоты
figure()
# hist(sample, bins=20)

# Вычисление важных показателей
n, m, minmax, s, cv, perct, mode, skew, kurt, kde = descriptive1d(sample)

print('Число элементов выборки: {0:d}'.format(n))
print('Среднее значение: {0:.4f}'.format(m))
print('Минимальное и максимальное значения: ({0:.4f}, {1:.4f})'.format(*minmax))
print('Стандартное отклонение: {0:.4f}'.format(s))
print('Коэффициент вариации (Пирсона): {0:.4f}'.format(cv))
print('Квартили: (25%) = {0:.4f}, (50%) = {1:.4f}, (75%) = {2:.4f}'.format(*perct))
print('Коэффициент асимметрии: {0:.4f}'.format(skew))
print('Коэффициент эксцесса: {0:.4f}'.format(kurt))

# Отрисовка оценки плотности распределения
figure()
plot(kde[0], kde[1])
title('pdf-estimation')
show()


# print(get_cosine_text_sim(news))

# feature_names = tfidf.get_feature_names()
# corpus_index = [n for n in corpus]
# rows, cols = tfs.nonzero()
# for row, col in zip(rows, cols):
#     print((feature_names[col], corpus_index[row]), tfs[row, col])

# alpha = 1
# time_delta = len(dates)
# news = read_preprocessed_news_for_dates(dates)
#
# for i in range(0, len(news)):
#     for j in range(i + 1, len(news)):
#         print(news[i]["date"] + "/" + news[j]["date"] + ": " + str(time_decay(alpha, news[i], news[j], time_delta)))

# news = read_preprocessed_news(d1.strftime('%Y-%m-%d'))
# texts_count = len(news)
# w1, w2 = 0.9, 0.1
# alpha = 0
# time_delta = len(dates)
# matrix = nallapati_sim(news, [w1, w2/2, w2/2], alpha, time_delta)

# for i in range(0, texts_count):
#     for j in range(i + 1, texts_count):
#         if news[i]["clusterId"] == news[j]["clusterId"]:
#             print(matrix[i][j])
#             print(str(news[i]["documentId"]) + ": " + news[i]["vanilla"][0:150])
#             print(str(news[j]["documentId"]) + ": " + news[j]["vanilla"][0:150])
#             print("\n")



# for i in range(1,5):
#     cluster = read_cluster(news, i)
#     for doc in cluster:
#         print(doc["vanilla"])
#         print("// cluster_id=" + str(doc["clusterId"]))
#     print("____________________________________________________________")