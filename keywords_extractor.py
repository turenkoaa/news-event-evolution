import pandas as pd

import pymorphy2
from unicodedata import category
from ner import Keywords, Name, Location
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
    return list(map(lambda name: (name.fact.first + " " if name.fact.first != None else "")
                         + (name.fact.middle + " " if name.fact.middle != None else "")
                         + (name.fact.last if name.fact.last != None else ""),
                    matches))

def get_Locations(text):
    extractor = LocationExtractor()
    matches = extractor(text)
    return list(map(lambda m: Location(m.fact.name), matches))

def get_locations(text):
    extractor = LocationExtractor()
    matches = list(filter(lambda m: m.fact.name != "россия", extractor(text)))
    return list(map(lambda m: m.fact.name, matches))



