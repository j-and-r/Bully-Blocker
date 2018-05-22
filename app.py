from flask import Flask, render_template, redirect, session, request, jsonify
from flask_session import Session
import tweepy
from helper import *
import os
import redis
import datetime
import json
import facebook

app = Flask(__name__)
app.secret_key = os.urandom(24)

# WARNING: Setup files
with open("creds.json", "w+") as f:
    f.write(os.environ['CREDS'])
    f.close()

with open("pyrebase.json", "w+") as f:
    f.write(os.environ['PYREBASE'])
    f.close()

cred = credentials.Certificate("creds.json")
firebase = firebase_admin.initialize_app(cred, name="bully-blocker")

# WARNING: Fetching env vars
consumer_key = os.environ['TWITTER_KEY']
consumer_secret = os.environ['TWITTER_SECRET']
port = int(os.environ.get('PORT', 5000))
redis_password = os.environ.get('REDIS_PASSWORD')

# WARNING: Setting up Redis session:
SESSION_REDIS = redis.StrictRedis(host='redis-10468.c1.us-east1-2.gce.cloud.redislabs.com', port=10468, password=redis_password)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

# WARNING: Setting up dictionaries
p_words = set()
n_words = set()

def load_words():
    n_file = open("./static/dicts/negative-words.txt", "r")
    p_file = open("./static/dicts/positive-words.txt", "r")

    for line in p_file:
        if line[0] != ";" and line != "":
            p_words.add(line.rstrip("\n"))
    p_file.close()

    for line in n_file:
        if line[0] != ";" and line != "":
            n_words.add(line.rstrip("\n"))
    n_file.close()

load_words()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'user' in session or session['user'] is None:
            return redirect("/sign-in")
        return f(*args, **kws)
    return decorated_function

# WARNING: Pages that don't require users to have account:

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("sign-in.html")
    else:
        email = request.form['email']
        password = request.form['password']
        user = sign_in_user(email, password)
        session['user'] = user
        return redirect('/twitter-feed')

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign-up.html")
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user(firebase, username, email, password)
        user = sign_in_user(email, password)
        session['user'] = user
        return redirect("/setup")

@app.route("/logout")
def logout():
    if 'user' in session and session['user'] is not None:
        session['user'] = None
    return redirect("/sign-in")

# WARNING: Front end for logged in users:

@app.route("/setup")
def setup():
    return render_template("setup.html")

@app.route("/twitter-auth")
def twitter_auth():
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
        return redirect('/twitter-auth')

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

    return redirect("/twitter-feed")

@app.route("/feed")
@login_required
def feed():
    if not 'access_token' in session or not 'access_secret' in session:
        return redirect('/setup')
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
        rating = rate(body, n_words, p_words)
        if float(rating) > 0:
            overall = "pos"
        else:
            overall = "neg"
        tweets.append({
            "date": date,
            "username": username,
            "profile_pic": profile_pic,
            "body": body,
            "rating": abs(float(rating)),
            "overall": overall
        })
    return render_template("twitter-feed.html", tweets=tweets)

@app.route("/settings")
def settings():
    return render_template("settings.html")

# TODO: Tests
@app.route("/generate-password")
def gen_pword():
    return generate_password()

@app.route("/password-strength")
def pwd_strength():
    return render_template("password-strength.html")

@app.route("/feed-test")
@login_required
def feed_test():
    feed = json.loads(open("feed.txt", "r").read())
    tweets = []
    for tweet in feed:
        date = tweet["created_at"]
        username = tweet["user"]["name"]
        profile_pic = tweet["user"]["profile_image_url"]
        body = tweet["text"]
        rating = rate(body, n_words, p_words)
        if float(rating) > 0:
            overall = "pos"
        else:
            overall = "neg"
        tweets.append({
            "date": date,
            "username": username,
            "profile_pic": profile_pic,
            "body": body,
            "rating": abs(float(rating)),
            "overall": overall
        })
    return render_template("twitter-feed.html", tweets=tweets)

app.run(host="0.0.0.0", port=port)


# @app.route("/facebook-auth")
# def facebook_auth():
#     client_id = "465011457266482"
#     redirect_uri = "https://bully-blocker.herokuapp.com/get-access-token"
#     # TODO: Change these to random strings
#     state = "{st=123456789, ds=987654321}"
#
#     return redirect("https://www.facebook.com/v3.0/dialog/oauth?client_id=" + client_id+ "&redirect_uri=" + redirect_uri + "&state='" + state + "'")
#
# @app.route("/get-access-token")
# def get_access_token():
#     code = request.args['code']
#     url = "https://graph.facebook.com/oauth/access_token?client_id=" + app_id + "&redirect_uri=" + redirect_uri + "&client_secret=" + app_secret + "&code=" + code
#
# @app.route("/facebook-callback")
# def facebook_callback():
#     access_token = request.args['access_token']
#     graph = facebook.GraphAPI(access_token=access_token, version="2.7")
#     session['graph'] = graph
#     return str(graph.get_object(id='115046399369073'))
