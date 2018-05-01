from flask import Flask, render_template, redirect, session, request
from flask_session import Session
import tweepy
from helper import *
import os
import redis
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# WARNING: Setting up Redis session:
# SESSION_REDIS = redis.StrictRedis(host='redis-10468.c1.us-east1-2.gce.cloud.redislabs.com', port=10468, password="Tih68ZitsoXZxXe27Ps9YR7HdzXWGGDh")
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

# WARNING: Setting up dictionaries
p_words = set()
n_words = set()

# WARNING: Fetching env vars
consumer_key = os.environ['TWITTER_KEY']
consumer_secret = os.environ['TWITTER_SECRET']
port = int(os.environ.get('PORT', 5000))

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

# WARNING: Pages that don't require users to have account:

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_in")
def test():
    return render_template("sign-in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign-up.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/generate-password")
def gen_pword():
    return generate_password()

@app.route("/title")
def title():
    return render_template("steering.html")

# WARNING: Twitter:

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

# WARNING: Front end for logged in users:

@app.route("/feed")
def feed():
    if not 'access_token' in session or not 'access_secret' in session:
        return redirect('/twitter_auth')
    key = session['access_token']
    secret = session['access_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    feed = twitter_feed(auth)
    tweets = []
    for tweet in feed:
        date = tweet.created_at.strftime('%A, %b %Y')
        username = tweet.user.name
        profile_pic = tweet.user.profile_image_url
        body = tweet.text
        tweets.append({
            "date": date,
            "username": username,
            "profile_pic": profile_pic,
            "body": body
        })
    return render_template("feed.html", tweets=tweets)

app.run(host="0.0.0.0", port=port)

# @app.route("/get_feed")
# def get_feed():
#     if not 'access_token' in session or not 'access_secret' in session:
#         return redirect('/twitter_auth')
#     key = session['access_token']
#     secret = session['access_secret']
#
#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(key, secret)
#
#     feed = twitter_feed(auth)
#     tweets = []
#     for tweet in feed:
#         tweets.append(tweet.text)
#     return str(tweet)
