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

table = str.maketrans({key: None for key in string.punctuation})

# textFeatures = TextFeatures(1)
# textFeatures.keywords = get_keywords(text)
# textFeatures.persons = get_persons(text)
#
# print(textFeatures.persons[0])