import json

def getTweetsTexts(tweets):
    """
        getTweetsTexts returns the list of texts from each tweet and creates a list of them
        This is particulary useful since we will be reading texts every time in each function

    """
    texts = []
    for tweet in tweets:
        texts.append(tweet["text"].lower())
    return texts

def getTweets (file_name):
    file = open(file_name)
    tweets = json.load(file)
    return getTweetsTexts(tweets)


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


#def extract_entities(text):


    

