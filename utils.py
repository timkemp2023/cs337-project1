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
