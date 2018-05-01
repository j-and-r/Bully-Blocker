import random
import tweepy

def twitter_feed(auth):

    api = tweepy.API(auth)

    tweets = api.home_timeline()
    return tweets

def rate(tweet, n_words):
    string = tweet.lower()
    meancount = 0
    wordcount = len(tweet.split(" "))
    words = string.split(" ")
    for word in words:
        if word in n_words:
            meancount += 1
    ratio = str(round(meancount/wordcount*100, 1))
    return ratio

def generate_password():
    n = random.randint(48, 122)
    p = chr(n)
    for i in range(10):
        n = random.randint(48, 122)
        p += chr(n)

    return p
