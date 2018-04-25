def twitter_feed(auth):

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    tweets = []
    for tweet in public_tweets:
        s = tweet.text
        tweets.append(s)
    return tweets

def meanDetector(tweet, n_words):
    string = tweet.lower()
    meancount = 0
    wordcount = len(tweet.split(" "))
    words = string.split(" ")
    for word in words:
        if word in n_words:
            meancount += 1
    ratio = str(round(meancount/wordcount*100, 1))
    return ratio
