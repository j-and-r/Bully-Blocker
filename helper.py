import random
import tweepy
import firebase_admin
import json
import pyrebase
from firebase_admin import credentials
from firebase_admin.auth import *

def new_user(firebase, username, email, password):
    user = create_user(email=email, password=password, display_name=username, app=firebase)
    print("Created User!")

def sign_in_user(email, password):
    firebase = None
    with open("pyrebase.json") as data:
        config = json.load(data)
        firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(email, password)
    return user

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
