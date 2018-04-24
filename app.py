from flask import Flask, render_template
import tweepy

app = Flask(__name__)
twitter_feed()

wordcount = 0

p_words = set()
n_words = set()
def load_words():
    n_file = open("dicts/negative.txt", "r")
    p_file = open("dicts/positive.txt", "r")

    for line in p_file:
        if line[0] != ";" and line != "":
            p_words.add(line.rstrip("\n"))
    p_file.close()

    for line in n_file:
        if line[0] != ";" and line != "":
            n_words.add(line.rstrip("\n"))
    n_file.close()

def meanDetector(tweet):
    string = tweet.lower()
    meancount = 0
    wordcount = len(tweet.split(" "))
    words = string.split(" ")
    for word in words:
        if word in n_words:
            meancount += 1
    ratio = str(round(meancount/wordcount*100, 1))
    return ratio


consumer_key = "BoWItkr5SlaiUNydLc5mQx9Ub"
consumer_secret = "pwuSvZNLGyZjfm1fBLUBYobzaFpO4bv29TwwagcAvgB2hn8Lfk"
def twitter_feed():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        s = tweet.text

load_words()
print(str(meanDetector(s)) + "%")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign-in")
def signIn():
    return "Sign In"

app.run(host="0.0.0.0", port=5000)
