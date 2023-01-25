from utils import *
import re

# awardToNomineesMap maps award_name to a list of nominees for that award
awardToNomineesMap = {}

# winnerToAwardMap maps award_name to the winner of the award
winnerToAwardMap = {} 

# map award to winners
awardToWinner = {}


# gets the winner of given award out of all nominees for that award
def getWinner(tweets, pattern, award_name, nominees_list):
    """
        get winner of an award from the list of nominees of that award using the awardToNomineesMap
    """
    voting = {nominee : 0 for nominee in nominees_list}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1) and matches.group(1).strip() in nominees_list:
            if matches.group(3) and contains_award_name(matches.group(3), award_name):
                winner = matches.group(1).strip()
                voting[winner] += 1

    voted_winner = max(voting, key=voting.get)
    return voted_winner


# compiles the winners of all awards
def getWinners(tweets, awards_list, nominees_lists):
    """
        aggregate the winners from each award name 
        
    """
    pattern = re.compile(r"(.*)(won\s|wins\s)(.*)?")
    for award in awards_list:
        nominee_list = nominees_lists[award]
        awardToWinner[award] = getWinner(tweets, pattern, award, nominee_list)


# gets the list of nominees given a single award
def getAwardNominees(award_name):
    """
        gets all the nominees of a given an award names
    """
    return ""


def getAwardCategories(awards_ceremony_name, tweets):
    """
        gets all the award categories from given tweets and given the name of awards ceremony
    """
    return ""


# gets all the hosts of the award show
def getHosts(awards_ceremony_name, tweets):
    """
        gets all the hosts for the given awards_ceremony_name from the tweets
    """
    pattern = re.compile(r"(.*)(is hosting|are hosting)(.*)?")

    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1):
            host_text = matches.group(1).strip()
            possible_hosts = get_named_entities(host_text)

            for host in possible_hosts:
                if host in voting:
                    voting[host] += 1
                else:
                    voting[host] = 1

    print(voting)
    voted_host = max(voting, key=voting.get)
    return voted_host


def main():
    lower_case_tweets = getTweets("gg2013.json")
    tweets = getTweets("gg2013.json", False)
    awardAnswers, nomineeAnswers = getAnswers('2013')

    getWinners(lower_case_tweets, awardAnswers, nomineeAnswers)
    host = getHosts("gg", tweets)
    #print(host)
    print(awardToWinner)


if __name__ == "__main__":
    main()
