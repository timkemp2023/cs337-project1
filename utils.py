import json
import re
import spacy

nlp = spacy.load("en_core_web_sm")

ENTITY_STOP_WORDS = {"RT", "Golden Globes", "GoldenGlobes", "And", "I", "You", "We"}
AWARD_STOP_WORDS = {'Congrats', 'Congratulations', 'Best', 'Actor', 'Actress', 'Motion', 'Picture', 'Movie', 'Film', 'Screenplay', 'Globes', 'Award', 'Awards', 'Comedy', 'Drama', 'Musical'}
STOP_WORDS = nlp.Defaults.stop_words

ALL_STOP_WORDS = set().union(ENTITY_STOP_WORDS).union(AWARD_STOP_WORDS).union(STOP_WORDS)



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


def removeStopWords(tweet):
    split_tweet = [word for word in tweet.split(" ") if word not in ALL_STOP_WORDS]
    return " ".join(split_tweet)



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


def contains_award_name(award_name, match, award_name_set):
    #trying the set method because it is O(n+m), while this current method is O(m^2)
    match_set = frozenset([word.replace(",", "") for word in match.lower().split(" ") if word not in STOP_WORDS])

    #removes stop words and returns true if the overlap in words is 3 or more.
    return len(award_name_set&match_set) >= len(award_name_set)


def check_for_award(award_name, chunks):
    for chunk in chunks:
        if chunk.text in award_name:
            return True
        else:
            return False


def get_people(text):
    prop_nouns = []
    doc = nlp(text)

    for token in doc.ents:
        if token.label_ == "PERSON":
            prop_nouns.append(token.text)

    return prop_nouns


def get_chunks(text):
    doc = nlp(text)
    chunks = []
    for chunk in doc.noun_chunks:
        text = chunk.text
        if "RT" not in chunk.text and "#" not in chunk.text and "@" not in chunk.text:
            if text not in ALL_STOP_WORDS:
                chunks.append(text.replace('"', ''))
    return chunks

def buildNomineeList(nominee_voting):
    if len(nominee_voting) == 0:
        return []
    
    nominees = []
    nominee_voting = nominee_voting[1:]
    num_noms = min(4, len(nominee_voting))

    for i in range(num_noms):
        nominees.append(nominee_voting[i][0])
    return nominees


