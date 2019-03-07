from natasha import (NamesExtractor, DatesExtractor, MoneyExtractor)
import pymorphy2
import string
from unicodedata import category

text = '''
Простите, еще несколько цитат из приговора. «…Отрицал существование
Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами
ожившего мертвеца — зомби» [и] «качествами больших покемонов —
представителей бестиария японской мифологии, тем самым совершил
преступление, предусмотренное статьей 148 УК РФ 18 января
'''

class Keywords:
    def __init__(self):
        self.verbs = []
        self.nouns = []
        self.adjs = []

class TextFeatures:
    def __init__(self, id):
        self.id = id
        self.persons = []

def exclude_punctuation(string):
    return ''.join(ch for ch in string if category(ch)[0] != 'P')

morph = pymorphy2.MorphAnalyzer()
table = str.maketrans({key: None for key in string.punctuation})

keys = Keywords()
textFeatures = TextFeatures(1)
textFeatures.keywords = keys

extractor = NamesExtractor()
matches = extractor(text)
for name in matches:
    textFeatures.persons.append(name)

for word in text.split():
    parsed = morph.parse(word)
    norm_parsed = set(map(lambda p: p.normalized, parsed))
    for option in norm_parsed:
        if(option.tag.POS == 'INFN'):
            keys.verbs.append((exclude_punctuation(option.word), option.score))
        elif(option.tag.POS == 'NOUN'):
            keys.nouns.append((exclude_punctuation(option.word), option.score))
        elif(option.tag.POS == 'ADJF'):
            keys.adjs.append((exclude_punctuation(option.word), option.score))

print(keys.adjs)
print(keys.nouns)
print(keys.verbs)
print(textFeatures.persons)
