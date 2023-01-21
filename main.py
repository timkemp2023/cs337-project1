import utils as u
import re

# awardToNomineesMap maps award_name to a list of nominees for that award
awardToNomineesMap = {}

# winnerToAwardMap maps award_name to the winner of the award
winnerToAwardMap = {} 

# map award to winners
awardToWinner = {}

def getWinner(tweets, pattern, award_name):
    """
        get winner of an award from the list of nominees of that award using the awardToNomineesMap
    """
    nominees = awardToNomineesMap[award_name]
    voting = {nominee : 0 for nominee in nominees}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1) in nominees and award_name in matches.group(2):
            winner = matches.group(1)
            voting[winner] += 1

    voted_winner = max(voting, key=voting.get)
    return voted_winner

def getWinners(tweets, awards_list):
    """
        aggregate the winners from each award name 
        
    """
    pattern = re.compile(r"(.*)[won|wins](.*)?")
    for award in awards_list:
        awardToWinner[award] = getWinner(tweets, pattern, award)


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
    keywords = [] # list of words that can identify the purpose
    return ""




def main():
    tweets = u.getTweets("gg2013.json")
    
    
    return 0

if __name__ == "__main__":
    main()
