from utils import *
import re

# awardToNomineesMap maps award_name to a list of nominees for that award
awardToNomineesMap = {}

# winnerToAwardMap maps award_name to the winner of the award
winnerToAwardMap = {} 

# map award to winners
awardToWinner = {}

def getWinner(tweets, pattern, award_name, nominees_list):
    """
        get winner of an award from the list of nominees of that award using the awardToNomineesMap
    """
    voting = {nominee : 0 for nominee in nominees_list}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1) and matches.group(1).strip() in nominees_list:
            # if matches.group(3) and contains_award_name(matches.group(3), award_name):
                winner = matches.group(1).strip()
                voting[winner] += 1

    if voting:
        voted_winner = max(voting, key=voting.get)
    else:
        voted_winner = "NO NOMINEES?"

    #print(voting)
    return voted_winner

def getWinners(tweets, awards_list, nominees_lists):
    """
        aggregate the winners from each award name 
        
    """
    pattern = re.compile(r"(.*)(won\s|wins\s)(.*)?")
    for award in awards_list:
        nominee_list = nominees_lists[award]
        awardToWinner[award] = getWinner(tweets, pattern, award, nominee_list)


def getAwardNominees(award_name):
    """
        gets all the nominees of a given an award names
    """
    return ""


def getAwardCategories(tweets):
    """
        gets all the award categories from given tweets
    """
    pattern = re.compile(r"best(.*)")
    for tweet in tweets:
        taggedTweet = list(nlp(tweet))
        textBeforeVerb = ""
        textAfterVerb = ""
        for token in taggedTweet:
            if token.pos != "VERB":
                textBeforeVerb += token.text + " "
        for token in taggedTweet[::-1]:
            if token.pos != "VERB":
                textAfterVerb += token.text + " "
        matches1 = pattern.match(textBeforeVerb)
        matches2 = pattern.match(textAfterVerb)
        if matches1:
            print("match 1, ", matches1, "\n\n")
        if matches2:
            print("match 2, ", matches2, "\n\n")
    # return matches1, matches2

def getHosts(awards_ceremony_name, tweets):
    """
        gets all the hosts for the given awards_ceremony_name from the tweets
    """
    pattern = re.compile(r"(.*)(hosts|is hosting)(.*)?")

    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1):
            host = matches.group(1).strip()
            if host in voting:
                voting[host] += 1
            else:
                voting[host] = 1

    voted_host = max(voting, key=voting.get)
    return voted_host


def main():
    tweets = getTweets("gg2013.json")
    # awardAnswers, nomineeAnswers = getAnswers('2013')

    # getWinners(tweets, awardAnswers, nomineeAnswers)
    # print(awardToWinner)
    print(getAwardCategories(tweets))


if __name__ == "__main__":
    main()
