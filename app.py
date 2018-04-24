from flask import Flask, render_template
import tweepy

app = Flask(__name__)

s = "I HATE YOU"
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

load_words()
print(str(meanDetector(s)) + "%")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign-in")
def signIn():
    return "Sign In"

app.run(host="0.0.0.0", port=5000)
