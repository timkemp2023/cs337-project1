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
    pattern = re.compile(r"(.*)(didn't win|doesn't win|should have won|should've won|nominate|nominee|-|for\s|deserve)(.*)?")

    for award in awards_list:
        awardToNominees[award] = getNominee(pattern, tweets, award)

    return awardToNominees
    

def getNominee(pattern, tweets, award_name):
    print("AWARD: ", award_name)
    award_name_set = AWARD_NAMES_SET[award_name]
    voting = {}

    for tweet in tweets:

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
    #print("SORTED VOTING: ", sorted_voting)
    voted_nominees = buildVotedList(sorted_voting, 4, True)
    print("VOTED NOMINEES", voted_nominees)
    return voted_nominees


def getPresenters(tweets, awards_list):
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
        gets all the award categories from given tweets
    """
    pattern = re.compile(r"(.*)best(.*)-(.*)")
    THRESHOLD = 3
    award_patterns = ["NNP, NNP, HYPH, NNP, CC, NNP"]
    for tweet in tweets:
        matches = pattern.match(tweet)
        if matches:
            award_name = ""
            #print(matches.group(2))
            txt =  matches.group(2)
            # if "christoph waltz" in txt:
            #     print(tweet)
            #print( matches.group(2))
            if "#" in txt:
                txt = txt.split("#")[0]
            if ":" in txt:
                txt = txt.split(":")[0]
            #people = get_people(txt)
            #print("people: ", people)
            # print("text: ", txt)
            processed_text = nlp(txt)
            numWords = 0
            for i in range(len(processed_text)):
                word = processed_text[i]
                if i+2 < len(processed_text):
                    #print("fuck waltz ", word.text + " " + processed_text[i+1].text)
                    if processed_text[i+1].text.capitalize() + " " + processed_text[i+2].text.capitalize() in ACTORS:
                        break
                if numWords > THRESHOLD:# or word.text in people:
                    break
                if word.pos_ == "NOUN":
                    numWords += 1
                if word.text == "tv":
                     award_name += "television "
                else:
                    award_name += word.text + " "
            if 1 <= award_name.count("-") < 2:
                if len(award_name.split(" ")) == 5:
                    print("award name: ", "best" + award_name)
                    doc = nlp(award_name)
                    i = 0
                    matchPattern = True
                    while (i < 4):
                        if doc[i].tag_ == award_patterns[i]:
                            continue
                        else:
                            matchPattern = False
                        i += 1
                    if matchPattern:
                        print("award name: ", "best" + award_name)


        

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
    """


# gets all the hosts of the award show
def getHosts(tweets):
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

    # for tweet in tweets:
    #     if ("jessica" in tweet.lower() or 'kiefer' in tweet.lower()) and 'actor' in tweet:
    #         print(tweet)

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
