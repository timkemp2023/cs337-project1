from utils import *
from constants import AWARD_NAMES_SET, MOVIES, ACTORS
import re
import spacy



# compiles the winners of all awards
def getWinners(tweets, awards_list):
    """
        aggregate the winners from each award name 
        
    """
    # map award to winners
    awardToWinner = {}
    pattern = re.compile(r"(.*)(won\s|wins\s)(.*)?")
    for award in awards_list:
        awardToWinner[award] = getWinner(tweets, pattern, award)
    
    return awardToWinner


# gets the winner of given award out of all nominees for that award
def getWinner(tweets, pattern, award_name):
    """
        get winner of an award from the list of nominees of that award using the awardToNomineesMap
    """
    award_name_set = AWARD_NAMES_SET[award_name]

    test_award = "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television"

    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1) and matches.group(2):
            if matches.group(3) and contains_award_name(award_name, matches.group(3).lower(), award_name_set):
                possible_winners = get_chunks(matches.group(1))

                if 'actor' in award_name or 'actress' in award_name or 'director' in award_name or 'cecil' in award_name:
                    typed_winners = [possible for possible in possible_winners if possible in ACTORS]
                else:
                    typed_winners = [possible for possible in possible_winners if possible in MOVIES]

                for winner in typed_winners:
                    if winner in voting:
                        voting[winner] += 1
                    else:
                        voting[winner] = 1

    voted_winner = max(voting, key=voting.get)
    return voted_winner


# gets the list of nominees given a single award
def getNominees(tweets, awards_list):
    """
        gets all the nominees of a given an award names
    """
    awardToNominees = {}
    #pattern = re.compile(r"(.*)(didn't win|doesn't win|should have won|should've won|nominate|nominee)(.*)?")

    for award in awards_list:
        awardToNominees[award] = getNominee(tweets, award)

    return awardToNominees
    

def getNominee(tweets, award_name):
    print("AWARD: ", award_name)
    award_name_set = AWARD_NAMES_SET[award_name]

    voting = {}
    for tweet in tweets:

        if contains_award_name(award_name, tweet.lower(), award_name_set):
            possible_nominees = get_chunks(tweet)

            if 'actor' in award_name or 'actress' in award_name or 'director' in award_name or 'cecil' in award_name:
                typed_nominees = [possible for possible in possible_nominees if possible in ACTORS]
            else:
                typed_nominees = [possible for possible in possible_nominees if possible in MOVIES]


            for winner in typed_nominees:
                if winner in voting:
                    voting[winner] += 1
                else:
                    voting[winner] = 1

    sorted_voting = sorted(voting.items(), reverse=True, key=lambda x:x[1])
    voted_nominees = buildNomineeList(sorted_voting)
    print("VOTED NOMINEES", voted_nominees)
    return voted_nominees


def getPresenters(tweets, awards_list):
    awardToPresenters = {}
    pattern = re.compile(r"(.*)(present)(.*)")

    for award in awards_list:
        awardToPresenters[award] = getPresenter(tweets, pattern, award)


def getPresenter(tweets, pattern, award):
    print("AWARD: ", award)
    voting = {}

    for tweet in tweets:
        matches = pattern.match(tweet)

        if matches and matches.group(1):
            if matches.group(3) and contains_award_name(matches.group(3), award, 2):
                presenter_text = matches.group(1).strip()
                possible_presenters = get_possible_entities(presenter_text)

                for presenter in possible_presenters:
                    presenter = presenter.strip()
                    if presenter in voting:
                        voting[presenter] += 1
                    else:
                        voting[presenter] = 1

    print(voting)
    return award


def getAwardCategories(tweets):
    """
        gets all the award categories from given tweets
    """
    pattern = re.compile(r"best(.*)")
    officialAwards = []
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
            # *** GET PEOPLE ***
            possible_hosts = get_chunks(host_text)

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
    tweets = getTweets("gg2013.json", False)

    awardAnswers, _ = getAnswers('2013')

    # winners = getWinners(tweets, awardAnswers)
    # print(winners)

    nominees = getNominees(tweets, awardAnswers)
    print(nominees)
    
    # presenters = getPresenters(tweets, awardAnswers)
    # print(presenters)

    #host = getHosts("gg", tweets)
    #print(host)

    #print(getAwardCategories(lower_case_tweets))

    
    

if __name__ == "__main__":
    main()
