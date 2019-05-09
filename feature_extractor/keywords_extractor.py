import pandas as pd

import pymorphy2
from unicodedata import category
from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor, LocationExtractor)
import string


class TextFeatures:
    def __init__(self, id):
        self.id = id
        self.persons = []


class Keywords:
    def __init__(self):
        self.verbs = []
        self.nouns = []
        self.adjs = []


class Name:
    def __init__(self, f, m, l, n):
        self.first, self.middle, self.last, self.nick, self.full = f, m, l, n, \
                                                                   (f + " " if f != None else "") + (
                                                                       m + " " if m != None else "") + (
                                                                       l if l != None else "")


class Location:
    def __init__(self, n):
        self.location = n


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


def get_Persons(text):
    extractor = NamesExtractor()
    matches = extractor(text)
    names = []
    for match in matches:
        name = match.fact
        if not (name.first is not None and name.middle is None and name.last is None and name.nick is None):
            names.append(Name(name.first, name.middle, name.last, name.nick))
    return names


def get_persons(text):
    extractor = NamesExtractor()
    matches = extractor(text)
    persons = list(map(lambda name: (name.fact.first + " " if name.fact.first != None else "")
                         + (name.fact.middle + " " if name.fact.middle != None else "")
                         + (name.fact.last if name.fact.last != None else ""),
                    matches))
    uniq = []
    for k in persons:
        uniq = uniq + k.split()
    return list(set(uniq))


def get_Locations(text):
    extractor = LocationExtractor()
    matches = extractor(text)
    return list(map(lambda m: Location(m.fact.name), matches))


def get_locations(text):
    extractor = LocationExtractor()
    matches = list(filter(lambda m: m.fact.name != "россия", extractor(text)))
    locations = list(map(lambda m: m.fact.name, matches))
    uniq = []
    for k in locations:
        uniq = uniq + k.split()
    return list(set(uniq))



