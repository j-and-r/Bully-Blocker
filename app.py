from flask import Flask, render_template

tweet = "i hate you"
words = open("mean-words.txt", "r").read().splitlines()
print (words)
wordcount = 0

app = Flask(__name__)

def meanDetector():
    meancount = 0
    wordcount = len(tweet.split(" "))
    for word in words:
        if word in tweet:
            meancount += 1
    ratio = str(round(meancount/wordcount*100, 2))
    return ratio

print(str(meanDetector()) + "%")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign-in")
def signIn():
    return "Sign In"


app.run(host="0.0.0.0", port=5000)
