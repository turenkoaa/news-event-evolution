import datetime
from keywords_based.keywords_from_news import extract_keywords_from_news
from keywords_based.newslen_clustering import get_stories_for_news
from read_news import get_dates_between, read_preprocessed_news_for_dates
from story_clustering import calculate_events_clusters, enrich_events_with_date

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 16)  # end date
dates = get_dates_between(d1, d2)
w = [0.7, 0.15, 0.15]
t = 0.3 # 0.1

news = read_preprocessed_news_for_dates(dates)
extract_keywords_from_news(news, 0.25)
events = calculate_events_clusters(news, w, t)
# events = story_to_event_mapping(news)
enrich_events_with_date(events, news)
get_stories_for_news(news, events, dates)


