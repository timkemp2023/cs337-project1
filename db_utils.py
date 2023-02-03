import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client['cs337project1DB']
Movies = db['Movies']
Actors = db['Actors']


def checkMovie(text):
    movies = Movies.find_one({"primaryTitle": text})
    if movies:
        return True
    else:
        return False


def checkActor(text):
    actors = Actors.find_one({"primaryName": text})
    

    if actors:
        return True
    else:
        return False


if __name__ == "__main__":
    text = "Golden Globes"
    print(checkActor(text))