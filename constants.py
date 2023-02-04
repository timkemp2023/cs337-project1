import pandas as pd


def get_movie_data():
    movie_df = pd.read_csv("movies.csv")
    movie_set = set(movie_df['primaryTitle'])
    return movie_set

def get_actor_data():
    actor_df = pd.read_csv("actors.csv")
    actor_set = set(actor_df['primaryName'])
    return actor_set


ACTORS = get_actor_data()
MOVIES = get_movie_data().difference(ACTORS)

AWARD_NAMES_SET = {
    "best screenplay - motion picture": set({"best", "screenplay", "motion", "picture"}),
    "best director - motion picture": set({"best", "director"}),
    "best performance by an actress in a television series - comedy or musical": set({"best", "actress", "tv", "comedy", "musical"}),
    "best foreign language film": set({"best", "foreign", "film"}),
    "best performance by an actor in a supporting role in a motion picture": set({"best", "actor", "supporting", "picture"}),
    "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television": set({"best", "actress", "supporting", "tv"}),
    "best motion picture - comedy or musical": set({"best", "picture", "comedy", "musical"}),
    "best performance by an actress in a motion picture - comedy or musical": set({"best", "actress", "picture", "comedy", "musical"}),
    "best mini-series or motion picture made for television": set({"best", "tv", "movie", "mini-series"}),
    "best original score - motion picture": set({"best", "original", "score"}),
    "best performance by an actress in a television series - drama": set({"best", "actress", "tv", "drama"}),
    "best performance by an actress in a motion picture - drama": set({"best", "actress", "picture", "drama"}),
    "cecil b. demille award": set({"cecil", "demille"}),
    "best performance by an actor in a motion picture - comedy or musical": set({"best", "actor", "picture", "comedy", "musical"}),
    "best motion picture - drama": set({"best", "picture", "drama"}),
    "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television": set({"best", "supporting", "actor", "tv"}),
    "best performance by an actress in a supporting role in a motion picture": set({"best", "supporting", "actress", "picture"}),
    "best television series - drama": set({"best", "tv", "drama"}),
    "best performance by an actor in a mini-series or motion picture made for television": set({"best", "actor", "tv", "movie"}),
    "best performance by an actress in a mini-series or motion picture made for television": set({"best", "actress", "tv", "movie"}),
    "best animated feature film": set({"best", "animated", "film"}),
    "best original song - motion picture": set({"best", "original", "song"}),
    "best performance by an actor in a motion picture - drama": set({"best", "actor", "picture", "drama"}),
    "best television series - comedy or musical": set({"best", "tv", "series", "comedy", "musical"}),
    "best performance by an actor in a television series - drama": set({"best", "actor", "tv", "drama"}),
    "best performance by an actor in a television series - comedy or musical": set({"best", "tv", "actor", "comedy", "musical"})
}

OFFICIAL_AWARDS = AWARD_NAMES_SET.keys()

