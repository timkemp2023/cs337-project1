import json
from nltk.corpus import stopwords
import spacy
import re
from spacy.lang.en import English
import imdb
#import wikipediaapi

nlp = English()

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
    award_name_set = frozenset([word for word in award_name.split(" ") if word not in stopwords.words("english")])
    match_set = frozenset([word for word in match.split(" ") if word not in stopwords.words("english")])

    #removes stop words and returns true if the overlap in words is 3 or more.
    return len(award_name_set&match_set) >= THRESHOLD


def get_named_entities(text):
    named_entities = []
    doc = nlp(text)

    for entity in doc.ents:
        if entity.label_ == "PERSON":
            named_entities.append(entity.text)
        # else:
        #     if '@' not in entity.text:
        #         print(entity.label_, ": ", entity.text)

    return named_entities

def get_possible_nominees(text):
    pattern = re.compile(r"(?:[A-Z][A-Za-z]*\s)+")
    matches = pattern.findall(text)
    return matches


# if __name__ == "__main__":
#     text = "Leo Dicaprio and Les Miserables, and even #ARGO have been nominated for golden globe"
#     print(get_possible_nominees(text))

def scrapeOfficialAwardsList():
    # used as a benchmark to gather all awards there is avaliable and vote on them based on tweets match to collect the ones seen from 
    # the tweets
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page("Golden_Globe_Awards")
    awardCategoriesWikipedia = page_py.section_by_title("Categories")
    motionPictureAwards = awardCategoriesWikipedia.section_by_title("Motion picture awards")
    televisionAwards = awardCategoriesWikipedia.section_by_title("Television awards")
    motionPictureAwardsList = motionPictureAwards.text.split("\n")
    televisionAwardsList = televisionAwards.text.split("\n")
    awardsList = {}
    for awardName in motionPictureAwardsList:
        awardsList[awardName.split(":")[0].strip()] = 0
    
    for awardName in televisionAwardsList:
        awardsList[awardName.split(":")[0].strip()] = 0
    
    return awardsList

