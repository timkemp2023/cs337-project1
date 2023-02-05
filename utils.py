import json
import re
import spacy

nlp = spacy.load("en_core_web_sm")

ENTITY_STOP_WORDS = {"i", "you", "u", "we", "he", "she", "a", "an", "they", "this", "anyone", "it", 'the', 'that', 'us', 'what', 'folks'}

AWARD_STOP_WORDS = {'golden', 'globes', 'globe', 'golden globes', 'goldenglobes', 'oscar', 'oscars', 'congrats', 'congratulations', 
'winner', 'best', 'actor', 'actress', 'performance', 'motion', 'picture', 'movie', 'film', 'screenplay', 'animated', 'feature', 'globes', 'award', 'awards', 
'comedy', 'drama', 'musical', 'tv', 'song', 'television', 'original', 'original score', 'original song', 'foreign language film', 'foreign', 'foreign language', 'language',
'mini', 'miniseries', 'oh my god', 'wtf', 'lol', 'awesome'}

STOP_WORDS = nlp.Defaults.stop_words

ALL_STOP_WORDS = set().union(ENTITY_STOP_WORDS).union(AWARD_STOP_WORDS)


def getTweetsTexts(tweets, lower_case=True):
    """
        getTweetsTexts: returns the list of texts from each tweet and creates a list of them
        This is particulary useful since we will be reading texts every time in each function

    """
    texts = []
    for tweet in tweets:
        tweet = tweet['text']
        tweet = re.sub('[,!?\.\"\']', '', tweet)
        if lower_case:
            texts.append(tweet.lower())
        else:
            texts.append(tweet)
    return texts


def getTweets (file_name, lower_case=True):
    file = open(file_name)
    tweets = json.load(file)
    return getTweetsTexts(tweets, lower_case)


def removeAwardStopWords(tweet):
    split_tweet = [word for word in tweet.split(" ") if word.lower() not in AWARD_STOP_WORDS]
    return " ".join(split_tweet)


def contains_award_name(award_name, match, award_name_set, df=0):
    """
        contains_award_name: returns True if award name matches
    """
    #trying the set method because it is O(n+m), while this current method is O(m^2)
    match_set = frozenset([word for word in match.lower().split(" ") if word not in STOP_WORDS])

    #removes stop words and returns true if the overlap in words is 3 or more.
    return len(award_name_set&match_set) >= (len(award_name_set) - df)


def get_people(text):
    people = []
    doc = nlp(text)

    for token in doc.ents:
        if token.label_ == "PERSON":
            people.append(token.text)

    return people

def get_people_first_names(text):
    people = []
    doc = nlp(text)

    for token in doc.ents:
        if token.label_ == "PERSON":
            #print("first name: ", token.text.split(" ")[0])
            people.append(token.text.split(" ")[0])
    
    # print("first name list: ", people)
    return people

def is_person(token):
    if token.label_ == "PERSON":
        return True
    return False
    

def get_chunks(text):
    filtered_text = removeAwardStopWords(text)
    doc = nlp(filtered_text)
    chunks = []
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text
        if "RT" not in chunk_text and "#" not in chunk_text and "@" not in chunk_text:
            if chunk_text.lower() not in ENTITY_STOP_WORDS and chunk_text.lower() not in AWARD_STOP_WORDS:
                chunks.append(chunk_text)
    return chunks


def buildVotedList(voting, threshold, ignore_first=False):
    if len(voting) == 0:
        return []
    
    voted = []
    if ignore_first:
        voting = voting[1:]
    return_num = min(threshold, len(voting))

    for i in range(return_num):
        voted.append(voting[i][0])
    return voted

# def capitalize_name(text):
#     words = [word.capitalize() for word in text.split(" ")]
#     return " ".join(words)


if __name__ == "__main__":
    text = 'tim kemp'
    print(text.capitalize())
