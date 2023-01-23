import utils as u
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

        if matches and matches.group(1) in nominees_list and award_name in matches.group(3):
            winner = matches.group(1)
            print(winner)
            voting[winner] += 1

    if voting:
        voted_winner = max(voting, key=voting.get)
    else:
        voted_winner = "NO NOMINEES?"

    return voted_winner

def getWinners(tweets, awards_list, nominees_list):
    """
        aggregate the winners from each award name 
        
    """
    pattern = re.compile(r"(.*)(won|wins)(.*)?")
    for award in awards_list:
        nominees = nominees_list[award]
        awardToWinner[award] = getWinner(tweets, pattern, award, nominees)


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

def getHosts(awards_ceremony_name, tweets):
    """
        gets all the hosts for the given awards_ceremony_name from the tweets
    """
    pattern = re.compile(r"(.*)(hosts|is hosting)(.*)?")

    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1):
            host = matches.group(1)
            if host in voting:
                voting[host] += 1
            else:
                voting[host] = 1

    voted_host = max(voting, key=voting.get)
    return voted_host


def main():
    tweets = u.getTweets("gg2013.json")
    awardAnswers, nomineeAnswers = u.getAnswers('2013')

    getWinners(tweets, awardAnswers, nomineeAnswers)
    #print(awardToWinner)

if __name__ == "__main__":
    main()
