import json
import re
import spacy

nlp = spacy.load("en_core_web_sm")

ENTITY_STOP_WORDS = ["RT", "Golden Globes"]
STOP_WORDS = nlp.Defaults.stop_words

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


def contains_award_name(match, award_name_set, THRESHOLD):
    #trying the set method because it is O(n+m), while this current method is O(m^2)
    match_set = frozenset([word for word in match.split(" ") if word not in STOP_WORDS])

    #removes stop words and returns true if the overlap in words is 3 or more.
    return len(award_name_set&match_set) >= THRESHOLD


def check_for_award(award_name, chunks):
    for chunk in chunks:
        if chunk.text in award_name:
            return True
        else:
            return False


def get_propnouns(text):
    prop_nouns = []
    doc = nlp(text)

    for token in doc:
        if token.pos_ == "PROPN":
            prop_nouns.append(token.text)
        # else:
        #     if '@' not in entity.text:
        #         print(entity.label_, ": ", entity.text)

    return prop_nouns


def get_possible_entities(text):
    entities = set()
    pattern = re.compile(r"(?:[A-Z][A-Za-z]*\s)+")



    matches = pattern.findall(text)
    entities = [match.strip() for match in matches if match.strip() not in ENTITY_STOP_WORDS]
    return entities


def get_chunks(text):
    doc = nlp(text)
    return [chunk for chunk in doc.noun_chunks if "RT" not in chunk.text and "#" not in chunk.text]


def check_award_type(award):
    if "actor" in award or "actress" in award or "director" in award:
        return "person"
    else:
        return "movie"


if __name__ == '__main__':

    text = "RT @nbcbayarea: Adele's Skyfall wins for best original song - motion picture. #GoldenGlobes http://t.co/N2LbbLQQ"
    print(get_chunks(text))

