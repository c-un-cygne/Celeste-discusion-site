from flask import Flask, render_template, request, session, redirect, url_for
import pymongo
import os

app = Flask(__name__)

client = pymongo.MongoClient('mongodb+srv://patricknumber2222_db_user:nqLQFbF7BHtxcOSD@clst-site.tv5cix5.mongodb.net/?appName=clst-site')
db = client["clst-site"]

app.secret_key = 'nqLQFbF7BHtxcOSD'


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)