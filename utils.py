import json
# from nltk.corpus import stopwords
import spacy
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


# def contains_award_name(match, award_name):
#     counter = 0
#     #award_name_set = award_name.split(" ")
    
#     #trying the set method because it is O(n+m), while this current method is O(m^2)
#     award_name_set = frozenset([word for word in award_name.split(" ") if word not in stopwords.words("english")])
#     match_set = frozenset([word for word in match.split(" ") if word not in stopwords.words("english")])

#     #removes stop words and returns true if the overlap in words is 3 or more.
#     return len(award_name_set&match_set) >= 3
    """
    for word in set(award_name_set):
        if word in match:
            counter +=1

    if counter >= 1:
        return True
    else:
        return False
    """
    
def get_named_entities(text):
    named_entities = []
    doc = nlp(text)

    for entity in doc.ents:
        if entity.label_ == "PERSON":
            named_entities.append(entity.text)

    return named_entities

