from flask import Flask, render_template, request, session, redirect, url_for
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient('mongodb+srv://patricknumber2222_db_user:nqLQFbF7BHtxcOSD@clst-site.tv5cix5.mongodb.net/?appName=clst-site')
db = client["clst-site"]

app.secret_key = 'nqLQFbF7BHtxcOSD'


@app.route('/')
def index():
    article_data = list(db['Article'].find({}))
    return render_template('index.html',articles = article_data[::-1])

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        db_users = db['User']
        user = db_users.find_one({'User':request.form['user']})
        if user:
            if request.form['password'] == user['Password']:
                session['user'] = request.form['user']
                return redirect(url_for('index'))
            else:
                return render_template('login.html', erreur="Incorrect Password")
        else:
            return render_template('login.html', erreur="Incorrect User")
    else:
        return render_template("login.html")

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        db_users = db['User']
        if not db_users.find_one({'User':request.form['user']}):
            if  request.form['password']==request.form['confirm_password']:
                db_users.insert_one({
                    'User':request.form['user'],
                    'Password':request.form['password']
                })
                session['user'] = request.form['user']
                return redirect(url_for('index'))
            else:
                return render_template('signup.html', erreur="Passwords not identical")
        else:
            return render_template('signup.html', erreur="User already exists")
    else:
        return render_template('signup.html')

@app.route('/disconnect')
def disconnect():
    session.clear()
    return redirect(url_for('index'))

@app.route('/publish', methods=["POST","GET"])
def publish():
    if 'user' not in session:
        return render_template('signup.html')
    if request.method == 'POST':
        db_articles = db["Article"]
        if request.form['title'] and request.form['description']:
            db_articles.insert_one({
                'Title':request.form['title'],
                'Description':request.form['description'],
                'User':session['user'],
                'Image':request.form['image']
            })
        return redirect(url_for('index'))
    else:
        return render_template('publish.html', erreur="Fill in all mandatory fields")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q','').strip()
    if query == '':
        res = list(db['Article'].find({}))
    else:
        res = list(db['Article'].find({
            "$or":[
                {"Title":{"$regex":query,"$options":"i"}},
                {"Description" : {"$regex":query,"$options":"i"}},
                {"User" : {"$regex":query,"$options":"i"}}
            ]
        }))
    return render_template("search_result.html", articles=res[::-1], query=query)

@app.route('/index/<id_article>')
def open(id_article):
    res = db['Article'].find_one({'_id':ObjectId(id_article)})
    return render_template('open.html',article = res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)