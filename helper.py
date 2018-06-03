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

def new_user(firebase, email, password):
    err = ""
    try:
        user = create_user(email=email, password=password, app=firebase)
    except Exception as e:
        err = json.loads(": ".join(str(e).split(": ")[1:]))["error"]["message"]
        err = err.replace("_", " ").lower()
        err = err.capitalize()
        if err == "Email exists":
            err = "Email already in use"
        print(e)
    return err

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

def post_twitter(auth, body):
    api = tweepy.API(auth)
    err = ""

    try:
        api.update_status(body)
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
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])

    return media_files

def moderate(text, key, thresh, return_type="basic", input_type="user"):
    try:
        headers = {
            'Content-Type': 'text/plain',
            'Ocp-Apim-Subscription-Key': key,
        }
        text = text.encode('utf-8')
        request_url = "https://australiaeast.api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/Screen?PII=true&classify=true"
        result = requests.post(request_url, data=text, headers=headers).json()
        if not "Classification" in result:
            if return_type is "basic":
                return "is fine to post."
            return {
                "rating": "is fine to post.",
                "error": "too small to moderate."
            }
        review = result["Classification"]["ReviewRecommended"]
        offensive = result["Classification"]["Category3"]["Score"]
        suggestive = result["Classification"]["Category2"]["Score"]
        sexual = result["Classification"]["Category1"]["Score"]
        terms = result["Terms"]

        rating = ""
        if input_type is "user":
            rating = "is fine to post."

        if offensive > thresh:
            if terms is None and review:
                rating = "could be offensive to some people"
            elif terms is None:
                rating = "slightly offensive"
            elif terms and not review:
                rating = "contains explicit language"
            elif terms and review:
                rating = "is offensive and or inappropriate"
            else:
                rating = "Unknown"

        if suggestive > thresh and sexual < thresh:
            rating += " and could be sexually suggestive."
        elif suggestive > thresh and sexual > thresh:
            rating += " and could be sexually explicit and suggestive or adult."
        elif sexual > thresh:
            rating += " and could be sexually explicit or adult."
        else:
            rating += "."


        data = {
            "rating": rating,
            "offensive": offensive,
            "suggestive": suggestive,
            "sexual": sexual
        }

        if return_type is "basic":
            return rating
        elif return_type is "detailed":
            return data
        else:
            return "Invalid return type"
    except e as Exception:
        print(e)
        if return_type is "basic":
            return "is fine to post."
        else:
            return {"error": "An error has occured"}
