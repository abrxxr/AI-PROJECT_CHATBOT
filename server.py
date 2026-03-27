# cretrential
import db
import json

from flask import Flask, render_template, request
app = Flask(__name__)
standard_answers = {
    "what is your name?":"My name is Sathvik Bot!"
}
chat_history = []
import logging
import joblib

@app.route('/', methods = ['GET', 'POST'])
def view():
    return render_template("index.html")

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    return render_template("signin.html")





@app.route('/register', methods = ['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/home", methods=['GET',"POST"])
def home():
    if request.method == "GET":
        name = request.args.get("username","Anonymous")
        msg = f"Me: Hello {name}! How can i help you?"
        chat_history.append(msg)
        return render_template("chat.html", messages=chat_history)
    else:
        user_response = request.form.get("input")
        ans = standard_answers.get(user_response.lower(), "Sorry, I could not understand")
        chat_history.append("You: " + user_response)
        chat_history.append("Me: " + str(ans))

        return render_template("chat.html", messages = chat_history)
app.run(debug=True, threaded=False)
