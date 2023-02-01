from utils import *
import re
#import imdb
from spacy.lang.en.stop_words import STOP_WORDS

#ia = imdb.Cinemagoer()

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
    pattern = re.compile(r"(.*)(won\s|wins\s|receive\s|get\s|got)(.*)?")
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
            if matches.group(3) and contains_award_name(matches.group(3), award_name, 3):
                winner = matches.group(1).strip()
                voting[winner] += 1

    voted_winner = max(voting, key=voting.get)
    return voted_winner


# gets the list of nominees given a single award
def getNominees(tweets, awards_list):
    """
        gets all the nominees of a given an award names
    """
    pattern = re.compile(r"(.*)(deserve\s\d|won|didn't win|doesn't win|win\s|should have won|should've won|nomin|nominee\s|is nominated\s|are nominated\s|was nominated\s|for \s)(.*)?")
    for award in awards_list:
        awardToNomineesMap[award] = getNominee(tweets, pattern, award)
    

def getNominee(tweets, pattern, award):
    print("AWARD: ", award)
    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1):
            if matches.group(3) and contains_award_name(matches.group(3), award, 1):
                nominee_text = matches.group(1).strip()
                possible_nominees = get_possible_nominees(nominee_text)
                print(possible_nominees)

                for nominee in possible_nominees:
                    if 'actor' or 'actress' or 'director' in award:
                        pass
                    else:
                        movie = ia.get_movie(nominee)
                        print(movie)
                for nominee in possible_nominees:
                    nominee = nominee.strip()
                    if nominee in voting:
                        voting[nominee] += 1
                    else:
                        voting[nominee] = 1

    #print(dict(sorted(voting.items(), reverse=True, key=lambda x:x[1])))
    #voted_nominee = max(voting, key=voting.get)
    print(voting)
    return award


def getAwardCategories(tweets):
    """
        gets all the award categories from given tweets
    """
    pattern = re.compile(r"best(.*)")
    officialAwards = scrapeOfficialAwardsList()
    for tweet in tweets:
        
        my_doc = nlp(tweet)
        taggedTweet = []
        for token in my_doc:
            taggedTweet.append(token)
        textBeforeVerb = ""
        textAfterVerb = ""
        for token in taggedTweet:
            lexeme = nlp.vocab[token.text]
            if token.pos != "VERB" and lexeme.is_stop == False:
                textBeforeVerb += token.text
        for token in taggedTweet[::-1]:
            lexeme = nlp.vocab[token.text]
            if token.pos != "VERB" and lexeme.is_stop == False:
                textAfterVerb += token.text + "  "

        
        matches1 = pattern.match(textBeforeVerb)
        matches2 = pattern.match(textAfterVerb)
        # if matches2:
        #     print("Text After is ", textAfterVerb, "\n")
        #     print("tweet is ", tweet, "\n")
        #     print("match is ", matches2, "\n\n")
        
        # if matches1:
        #     print("Text Before is ", textBeforeVerb, "\n")
        #     print("tweet is ", tweet, "\n ")
        #     print("match is ", matches1, "\n\n")
        match = None
        if matches1:
            match = matches1
        if matches2:
            match = matches2
        # for officialName, count in officialAwards.items():
        #     matches1FrozenSet = frozenset([word for word in matches2.group(0).split(" ")])
        #     tweetFrozenSet = frozenset(officialName.split(" "))
        #     if len(matches1FrozenSet&tweetFrozenSet) >= 2:
        #         count += 1
        # print("Map is ", officialAwards, "\n\n")
    


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

    # print("Host Viting")
    # print(voting)
    voted_host = max(voting, key=voting.get)
    return voted_host


def main():
    lower_case_tweets = getTweets("gg2013.json")
    # scrapeOfficialAwardsList()
    tweets = getTweets("gg2013.json", False)
    awardAnswers, nomineeAnswers = getAnswers('2013')

    # for tweet in tweets:
    #     if "presenter" in tweet or "presenting" in tweet or "presented" in tweet:
    #         print(tweet)

    # getWinners(lower_case_tweets, awardAnswers, nomineeAnswers)
    # print(awardToWinner)

    getNominees(tweets, awardAnswers)
    print(awardToNomineesMap)

    #host = getHosts("gg", tweets)
    #print(host)

    #awardAnswers, nomineeAnswers = getAnswers('2013')
    #print(getAwardCategories(lower_case_tweets))
    

if __name__ == "__main__":
    main()
