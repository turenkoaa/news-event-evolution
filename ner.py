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

table = str.maketrans({key: None for key in string.punctuation})

# textFeatures = TextFeatures(1)
# textFeatures.keywords = get_keywords(text)
# textFeatures.persons = get_persons(text)
#
# print(textFeatures.persons[0])