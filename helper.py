import random
import tweepy
import firebase_admin
import json
import pyrebase
import requests
from firebase_admin import credentials
from firebase_admin.auth import *
from functools import wraps
from flask import abort

def new_user(firebase, username, email, password):
    try:
        user = create_user(email=email, password=password, display_name=username, app=firebase)
    except Exception as e:
        print(e)
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

def post_twitter(auth):
    api = tweepy.API(auth)
    err = ""

    try:
        api.update_status('Updating using OAuth authentication via Tweepy!')
    except Exception as e:
        err = e

    return str(err)

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

def twitter_pictures(status):
    media_files = set()
    media = status.entities.get('media', [])
    print(status)
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])

    return media_files

def moderate(text, key):
    print("Started Moderating...")
    headers = {
        # Request headers
        'Content-Type': 'text/plain',
        'Ocp-Apim-Subscription-Key': key,
    }
    text = text.encode('utf-8')
    request_url = "https://australiaeast.api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/Screen?PII=true&classify=true"
    r = requests.post(request_url, data=text, headers=headers)
    return r.json()
