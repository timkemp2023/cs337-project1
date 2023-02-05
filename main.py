from utils import *
from constants import AWARD_NAMES_SET, OFFICIAL_AWARDS, MOVIES, ACTORS
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

    if voting:
        voted_winner = max(voting, key=voting.get)
    else:
        voted_winner = None

    return voted_winner


# gets the list of nominees given a single award
def getNominees(tweets, awards_list):
    """
        gets all the nominees of a given an award names
    """
    awardToNominees = {}
    pattern = re.compile(r"(.*)(win|won|nom|should|lost|defeated|congrats|goes|went|robbed|deserved)(.*)?")

    for award in awards_list:
        awardToNominees[award] = getNominee(pattern, tweets, award)

    return awardToNominees
    

def getNominee(pattern, tweets, award_name):
    print("AWARD: ", award_name)
    award_name_set = AWARD_NAMES_SET[award_name]
    voting = {}

    for tweet in tweets:
        #matches = pattern.match(tweet)

        if 'comedy' in award_name or 'musical' in award_name:
            df = 1
        else:
            df = 0

        if contains_award_name(award_name, tweet.lower(), award_name_set, df) and 'present' not in tweet.lower():
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
    voted_nominees = buildVotedList(sorted_voting, 4, True)
    return voted_nominees


def getPresenters(tweets, awards_list):
    """
    getPresenters: return a list of presenters for each award
    """
    awardToPresenters = {}
    pattern = re.compile(r"(.*)(presenting|presented|present)(.*)")

    for award in awards_list:
        awardToPresenters[award] = getPresenter(tweets, pattern, award)


def getPresenter(tweets, pattern, award_name):
    award_name_set = AWARD_NAMES_SET[award_name]

    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1) and matches.group(2):
            if matches.group(3) and contains_award_name(award_name, matches.group(3).lower(), award_name_set):
                possible_presenters = get_people(matches.group(1))

                # if 'actor' in award_name or 'actress' in award_name or 'director' in award_name or 'cecil' in award_name:
                #     typed_winners = [possible for possible in possible_winners if possible in ACTORS]
                # else:
                #     typed_winners = [possible for possible in possible_winners if possible in MOVIES]

                for winner in possible_presenters:
                    if winner in voting:
                        voting[winner] += 1
                    else:
                        voting[winner] = 1

        
    sorted_voting = sorted(voting.items(), reverse=True, key=lambda x:x[1])
    voted_presenters = buildVotedList(sorted_voting, 2, False)
    return voted_presenters


def getAwardCategories(tweets):
    """
        getAwardCategories: returns all the award categories from given tweets
    """
    voting = {}
    pattern = re.compile(r"(.*)best(.*)\s-\s(.*)")
    THRESHOLD = 3

    for tweet in tweets:
        matches = pattern.match(tweet)
        if matches:
            award_name = ""

            txt =  matches.group(2)
    
            if "#" in txt:
                txt = txt.split("#")[0]
            if ":" in txt:
                txt = txt.split(":")[0]

            processed_text = nlp(txt)
            numWords = 0
            for i in range(len(processed_text)):
                word = processed_text[i]

                if numWords > THRESHOLD:# or word.text in people:
                    break
                if word.pos_ == "NOUN":
                    numWords += 1
                if word.text == "tv":
                     award_name += "television "
                else:
                    award_name += word.text + " "
            if 1 <= award_name.count("-") < 2:
                
                award_name = "best " + award_name.strip()

                name_pattern = re.compile(r"(.*)\s-\s([/A-Za-z\s]*)")
                name_matches = name_pattern.match(award_name)

                if name_matches and name_matches.group(2):
                    name = str.title(name_matches.group(2).strip())

                    if name in MOVIES or name in ACTORS:
                        award_name = award_name.split("-")[0].strip()

                if award_name in voting:
                    voting[award_name] += 1
                else:
                    voting[award_name] = 1
    
    sorted_voting = sorted(voting.items(), reverse=True, key=lambda x:x[1])
    voted_awards = buildVotedList(sorted_voting, 17, False)
    # for voted_award in voted_awards:
    #     print(voted_award)
    return voted_awards


def getHosts(tweets):
    """
        getHosts: returns all the hosts of the ceremony from the tweets
    """
    pattern = re.compile(r"(.*)(is hosting|are hosting)(.*)?")

    voting = {}
    for tweet in tweets:
        matches =  pattern.match(tweet)

        if matches and matches.group(1):
            host_text = matches.group(1).strip()
            # *** GET PEOPLE ***
            possible_hosts = get_people(host_text)

            for host in possible_hosts:
                if host in voting:
                    voting[host] += 1
                else:
                    voting[host] = 1

    sorted_voting = sorted(voting.items(), reverse=True, key=lambda x:x[1])
    voted_host = buildVotedList(sorted_voting, 2, False)
    return {"hosts": voted_host}


def main():
    lower_case_tweets = getTweets("gg2013.json")
    tweets = getTweets("gg2013.json", False)
    # tweet = "rt @goldenglobes: best actress in a motion picture - drama - jessica chastain - zero dark thirty - #goldenglobes"
    # tweet2 = "rt @goldenglobes: best actor in a motion picture - comedy or musical - hugh jackman (@realhughjackman) - les miserables - #goldenglob"
    # tweet3 = "rt @goldenglobes: best supporting actress in a tv movie series or miniseries - maggie smith - downtown abbey: season 2 - #goldenglobe"
    
    # print(get_chunks(tweet))
    # print(get_chunks(tweet2))
    # print(get_chunks(tweet3))

    # winners = getWinners(tweets, OFFICIAL_AWARDS)
    # print(winners)

    # nominees = getNominees(tweets, OFFICIAL_AWARDS)
    # print(nominees)
    
    # presenters = getPresenters(tweets, OFFICIAL_AWARDS)
    # print(presenters)

    # hosts = getHosts(tweets)
    # print(hosts)

    print(getAwardCategories(lower_case_tweets))

    

if __name__ == "__main__":
    main()
