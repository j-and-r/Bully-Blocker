from flask import Flask, render_template, redirect, session, request
from flask_session import Session
import tweepy
from helper import *
import os
import redis
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

SESSION_REDIS = redis.StrictRedis(host='redis-10468.c1.us-east1-2.gce.cloud.redislabs.com', port=10468, password="Tih68ZitsoXZxXe27Ps9YR7HdzXWGGDh")
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

wordcount = 0
p_words = set()
n_words = set()

consumer_key = os.environ['TWITTER_KEY']
consumer_secret = os.environ['TWITTER_SECRET']
port = int(os.environ.get('PORT', 5000))

print(consumer_key)
print(consumer_secret)

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/twitter_auth")
def sign_in():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        return 'Error! Failed to get request token.'

    session['request_token'] = auth.request_token
    return redirect(redirect_url, code=302)

@app.route("/twitter_callback")
def twitter_callback():
    if not 'request_token' in session:
        return redirect('/twitter_auth')

    verifier = request.args.get('oauth_verifier')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    token = session.get('request_token')
    session.pop('request_token')
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        return "error"

    session['access_token'] = auth.access_token
    session['access_secret'] = auth.access_token_secret

    return redirect("/feed")

@app.route("/get_feed")
def get_feed():
    if not 'access_token' in session or not 'access_secret' in session:
        return redirect('/twitter_auth')
    key = session['access_token']
    secret = session['access_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    feed = twitter_feed(auth)
    tweets = []
    for tweet in feed:
        tweets.append(tweet.text)
    return str(tweet)

@app.route("/sign_in")
def test():
    return render_template("sign-in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign-up.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feed")
def feed():
    if not 'access_token' in session or not 'access_secret' in session:
        return redirect('/twitter_auth')
    key = session['access_token']
    secret = session['access_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    feed = twitter_feed(auth)
    tweet = feed[0]
    date = tweet.created_at
    date = date.strftime('%A, %b %Y')
    return render_template("feed.html", name=tweet.user.name, body=tweet.text, profile_pic=tweet.user.profile_image_url, date=date)

@app.route("/generate-password")
def gen_pword():
    return generate_password()

app.run(host="0.0.0.0", port=port)
