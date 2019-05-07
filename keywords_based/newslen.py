import datetime
from keywords_based.keywords_from_news import extract_keywords_from_news
from keywords_based.newslen_clustering import get_stories_for_news
from read_news import get_dates_between, read_preprocessed_news_for_dates
from story_clustering import calculate_events_clusters, enrich_events_with_date

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 16)  # end date



