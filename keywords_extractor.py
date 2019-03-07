import pandas as pd

import pymorphy2
from unicodedata import category
from ner import Keywords
from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor, LocationExtractor)


def exclude_punctuation(string):
    return ''.join(ch for ch in string if category(ch)[0] != 'P')

def get_keywords(text):
    morph = pymorphy2.MorphAnalyzer()

    keywords = Keywords()

    for word in text.split():
        parsed = morph.parse(word)
        norm_parsed = set(map(lambda p: p.normalized, parsed))
        for option in norm_parsed:
            if option.tag.POS == 'INFN':
                keywords.verbs.append((exclude_punctuation(option.word), option.score))
            elif option.tag.POS == 'NOUN':
                keywords.nouns.append((exclude_punctuation(option.word), option.score))
            elif option.tag.POS == 'ADJF':
                keywords.adjs.append((exclude_punctuation(option.word), option.score))

    return keywords

def get_persons(text):
    persons = []
    extractor = NamesExtractor()
    matches = extractor(text)
    for name in matches:
        if not (name.first is not None and name.middle is None, name.last is None, name.nick is None):
            persons.append(name)
    return persons

class Name:
    def __init__(self, f, m, l, n):
        self.first, self.middle, self.last, self.nick, self.full = f, m, l, n,\
            (f + " " if f != None else "") + (m + " " if m != None else "") + (l if l != None else "")

def get_names(text):
    extractor = NamesExtractor()
    matches = extractor(text)
    names = []
    for match in matches:
        name = match.fact
        names.append(Name(name.first, name.middle, name.last, name.nick))
    return names

text = '''
Так говорила в июле 1805 года известная Анна Павловна Шерер, фрейлина и приближенная императрицы Марии Феодоровны, встречая важного и чиновного князя Василия, первого приехавшего на ее вечер. Анна Павловна кашляла несколько дней, у нее был грипп, как она говорила (грипп был тогда новое слово, употреблявшееся только редкими).

Предлагаю вернуть прежние границы природного парка №71 на Инженерной улице 2.

По адресу Алтуфьевское шоссе д.51 (основной вид разрешенного использования: производственная деятельность, склады) размещен МПЗ. Жители требуют незамедлительной остановки МПЗ и его вывода из района

Контакты О нас телефон 7 881 574-10-02 Адрес Республика Карелия,г.Петрозаводск,ул.Маршала Мерецкова, д.8 Б,офис 4

Благодарственное письмо   Хочу поблагодарить учителей моего, теперь уже бывшего, одиннадцатиклассника:  Бушуева Вячеслава Владимировича и Бушуеву Веру Константиновну. Они вовлекали сына в интересные внеурочные занятия, связанные с театром и походами.

Вячеслава

По адресу Алтуфьевское шоссе д.51 (основной вид разрешенного использования: производственная деятельность, склады) размещен МПЗ. Жители требуют незамедлительной остановки МПЗ и его вывода из района

Контакты О нас телефон 7 881 574-10-02 Адрес Республика Карелия,г.Петрозаводск,ул.Маршала Мерецкова, д.8 Б,офис 4

Благодарственное письмо   Хочу поблагодарить учителей моего, теперь уже бывшего, одиннадцатиклассника:  Бушуева Вячеслава Владимировича и Бушуеву Веру Константиновну. Они вовлекали сына в интересные внеурочные занятия, связанные с театром и походами.
'''

# names = get_names(text)
# df = pd.DataFrame([t.__dict__ for t in names])
# print(df.groupby(['full']).size().sort_values(ascending=False).head(10))
# df.to_csv("C:/Users/User/Desktop/diploma/ner/result.scv", sep='\t', encoding='utf-8')

