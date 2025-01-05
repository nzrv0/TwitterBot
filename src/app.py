from flask import Flask
import os

os.chdir("/code")
app = Flask(__name__)


@app.route("/")
def hello():
    resoult = []
    with open("logs/cron.log", "r") as fs:
        for i in fs:
            resoult.append(i)
    return resoult
