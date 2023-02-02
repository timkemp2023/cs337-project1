import json
from nltk.corpus import stopwords
import spacy
import re


nlp = spacy.load("en_core_web_sm")


def getTweetsTexts(tweets, lower_case=True):
    """
        getTweetsTexts returns the list of texts from each tweet and creates a list of them
        This is particulary useful since we will be reading texts every time in each function

    """
    texts = []
    for tweet in tweets:
        if lower_case:
            texts.append(tweet["text"].lower())
        else:
            texts.append(tweet["text"])
    return texts


def getTweets (file_name, lower_case=True):
    file = open(file_name)
    tweets = json.load(file)
    return getTweetsTexts(tweets, lower_case)


def getAnswers(year):
    awardsToNominees = {}
    awardsList = []

    file_name = "gg" + str(year) + "answers.json"
    file = open(file_name)
    answers = json.load(file)
    awardAnswers = answers['award_data']

    for award in awardAnswers:
        awardsList.append(award)
        nominees = awardAnswers[award]['nominees']
        nominees.append(awardAnswers[award]['winner'])
        awardsToNominees[award] = nominees

    return awardsList, awardsToNominees


def contains_award_name(match, award_name, THRESHOLD):
    counter = 0
    #award_name_set = award_name.split(" ")
    
    #trying the set method because it is O(n+m), while this current method is O(m^2)
    award_name_set = frozenset([word for word in award_name.split(" ") if word not in set(stopwords.words("english"))])
    match_set = frozenset([word for word in match.split(" ") if word not in set(stopwords.words("english"))])

    #removes stop words and returns true if the overlap in words is 3 or more.
    return len(award_name_set&match_set) >= THRESHOLD


def get_people(text):
    named_entities = []
    doc = nlp(text)

    for entity in doc.ents:
        if entity.label_ == "PERSON":
            named_entities.append(entity.text)
        # else:
        #     if '@' not in entity.text:
        #         print(entity.label_, ": ", entity.text)

    return named_entities

def get_possible_entities(text):
    pattern = re.compile(r"(?:[A-Z][A-Za-z]*\s)+")
    matches = pattern.findall(text)
    return matches


def get_chunks(text):
    doc = nlp(text)
    return [chunk for chunk in doc.noun_chunks]


if __name__ == '__main__':

    text = "Movie Director wins best director of a motion picture"
    print(get_chunks(text))

