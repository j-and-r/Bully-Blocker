import random
import tweepy

def twitter_feed(auth):

    api = tweepy.API(auth)

    tweets = api.home_timeline()
    return tweets

def rate(tweet, n_words, p_words):
    string = tweet.lower()
    n_count = 0
    p_count = 0
    total = len(tweet.split(" "))
    words = string.split(" ")
    for word in words:
        if word in n_words:
            n_count += 1
    for word in words:
        if word in p_words:
            p_count += 1
    sentiment = p_count - n_count
    ratio = str(round(sentiment/total*100, 1))
    print(ratio)
    return ratio

def generate_password():
    n = random.randint(48, 122)
    p = chr(n)
    for i in range(10):
        n = random.randint(48, 122)
        p += chr(n)

    return p
