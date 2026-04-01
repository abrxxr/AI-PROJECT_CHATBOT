# cretrential
import db
import json
import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
# Set your OpenAI API key here or use environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

standard_answers = {
    "what is your name?":"My name is Sathvik Bot!"
}
chat_history = []
import logging
import joblib

def generate_llm_response(user_input):
    """Generate a response using OpenAI's GPT model based on user input."""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-api-key-here":
            return "I'm sorry, but the AI service is not configured yet. Please set up your OpenAI API key in the .env file."
        
        # Check if it's a standard question first
        if user_input.lower() in standard_answers:
            return standard_answers[user_input.lower()]
        
        # Use LLM for dynamic responses
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant chatbot. Respond naturally and helpfully to user queries. Keep responses concise but informative."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating LLM response: {e}")
        return "Sorry, I'm having trouble processing your request right now. Please try again later."

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
        ans = generate_llm_response(user_response)
        chat_history.append("You: " + user_response)
        chat_history.append("Me: " + str(ans))

        return render_template("chat.html", messages = chat_history)
app.run(debug=True, threaded=False)
