import datetime

from keywords_based.newslen_clustering import get_stories_for_dates

d1 = datetime.date(2018, 10, 10)  # start date
d2 = datetime.date(2018, 10, 16)
end_date = datetime.date(2018, 11, 10)

clusters = get_stories_for_dates(d1, d2)['stories']