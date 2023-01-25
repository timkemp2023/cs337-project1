from utils import *
import re

# awardToNomineesMap maps award_name to a list of nominees for that award
awardToNomineesMap = {}

# winnerToAwardMap maps award_name to the winner of the award
winnerToAwardMap = {} 

# map award to winners
awardToWinner = {}


# compiles the winners of all awards
def getWinners(tweets, awards_list, nominees_lists):
    """
        aggregate the winners from each award name 
        
    """
    pattern = re.compile(r"(.*)(won\s|wins\s)(.*)?")
    for award in awards_list:
        nominee_list = nominees_lists[award]
        awardToWinner[award] = getWinner(tweets, pattern, award, nominee_list)


# gets the winner of given award out of all nominees for that award
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

    voted_winner = max(voting, key=voting.get)
    return voted_winner


# gets the list of nominees given a single award
def getNominees(tweets, awards_list):
    """
        gets all the nominees of a given an award names
    """
    pattern = re.compile(r"(.*)(is nominated\s|are nominated\s|have been nominated\s|was nominated\s)(.*)?")
    for award in awards_list:
        awardToNomineesMap[award] = getNominee(tweets, pattern, award)
    

def getNominee(tweets, pattern, award):
    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1):
            nominee_text = matches.group(1).strip()
            possible_nominees = get_named_entities(nominee_text)

            for nominee in possible_nominees:
                if nominee in voting:
                    voting[nominee] += 1
                else:
                    voting[nominee] = 1

    voted_nominee = max(voting, key=voting.get)
    return voted_nominee


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

    print("Host Viting")
    print(voting)
    voted_host = max(voting, key=voting.get)
    return voted_host


def main():
    lower_case_tweets = getTweets("gg2013.json")
    tweets = getTweets("gg2013.json", False)
    awardAnswers, nomineeAnswers = getAnswers('2013')

    getWinners(lower_case_tweets, awardAnswers, nomineeAnswers)
    print(awardToWinner)

    # getNominees(tweets, awardAnswers)
    # print(awardToNomineesMap)

    host = getHosts("gg", tweets)
    print(host)

    #awardAnswers, nomineeAnswers = getAnswers('2013')
    #print(getAwardCategories(tweets))


if __name__ == "__main__":
    main()
