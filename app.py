from flask import Flask, render_template, redirect, session, request
from flask_session import Session
import tweepy
from helper import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

wordcount = 0
p_words = set()
n_words = set()

secret_file = open("twitter.txt", "r")
secret = secret_file.read().splitlines()
secret_file.close()

consumer_key = secret[0]
consumer_secret = secret[1]

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

@app.route("/Twitter-auth")
def sign_in():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        return 'Error! Failed to get request token.'

    session['request_token'] = auth.request_token
    return redirect(redirect_url, code=302)

@app.route("/twitter-callback")
def twitter_callback():
    if not 'request_token' in session:
        return redirect('/sign-in')

    verifier = request.args.get('oauth_verifier')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    token = session.get('request_token')
    session.delete('request_token')
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        return "error"

    session['access_token'] = auth.access_token
    session['access_secret'] = auth.access_token_secret

    return redirect("/feed")

@app.route("/feed")
def feed():
    token = session['access_token']
    secret = session['access_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    feed = twitter_feed(auth)
    return str(feed)

@app.route("/sign_in")
def test():
    return render_template("sign-in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign-up.html")

app.run(host="0.0.0.0", port=5000)
