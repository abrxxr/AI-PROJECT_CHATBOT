# cretrential
import db
import json
import os
import difflib
from flask import Flask, render_template, request, jsonify
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
known_answers = {
    "intro": "Hello there 👋🏻, I am your AI assistant. Send 'help' to know more.",
    "help": "Send a keyword like skills, resume, education, contact, projects. I also answer free-text questions.",
    "skills": "I can code in Python, JavaScript, C, and build web/mobile apps.",
    "resume": "You can download my resume from the link in the response.",
    "education": "I am studying B.E. in Computer Science Engineering.",
    "chatbot": "I am your AI chatbot assistant built with GPT. You can ask me anything about your college, courses, and more.",
    "who are you": "I am a chatbot assistant that provides info about your institution and can answer general questions with OpenAI GPT.",
    "contact": "Email, phone, and GitHub links are available on the website.",
    "projects": "I have projects on GitHub including AI chatbot, web apps, and mobile apps.",
    "department": "CSE, AIML, AIDS, CYBER SECURITY, MECHANICAL, MECHATRONICS, ACT, CIVIL, EEE, BIO MEDICAL ENGINEERING, CSBS, IT.",
    "lab available": "Computer lab, Communication lab, Electrical & Electronics Lab, Manufacturing Technology lab, Electrical Circuit Lab, etc.",
    "about hostel": "Hostel details: comfortable cots, wardrobe, study table, safe environment.",
    "about transport": "A fleet of buses operates across the city with safe routes and incharges.",
    "placements": "Placement categories: Marquee >20 LPA, Super Dream 10-20 LPA, Dream 6-10 LPA.",
    "coe": "Centres of Excellence include CAIR, Additive Manufacturing, Industrial Automation, VLSI, Materials, Nanotech, etc.",
    "curriculum delivery": "Curriculum delivery stays through planning, development, implementation, and evaluation.",
    "value added course": "Value added courses: Java, .NET, Full Stack, Oracle, BPM, Web, Mobile, IoT, VLSI, etc.",
    "training methods": "Training methods include problem solving, communication, domain skills, mock interviews, internships.",
    "sports": "Sports facilities include gym, yoga, volleyball, basketball, cricket, football, table tennis and more.",
    "auditorium": "Main auditoriums: Shri Parthasarathy, Cauvery, Pennay hall.",
    "ict": "ICT features 2 Gbps internet, 1200+ computers, intranet with schedules and campus info.",
    "library": "Library is well equipped with international standard collection and security systems.",
    "health centre": "Health centre has separate male/female inpatient facility, medical officer and assistant.",
    "time": "Use JavaScript to get current local time on the client side.",
    "date": "Use JavaScript to get today's date on the client side."
}

intent_synonyms = {
    "department": ["department", "departments", "departmnt", "dept"],
    "lab available": ["lab available", "labs", "lab", "available lab"],
    "about hostel": ["about hostel", "hostel", "hostel details"],
    "about transport": ["about transport", "transport", "bus", "travel"],
    "placements": ["placements", "placement", "job placement"],
    "coe": ["coe", "centre of excellence", "center of excellence"],
    "curriculum delivery": ["curriculum delivery", "syllabus", "curriculum"],
    "value added course": ["value added course", "extra course"],
    "training methods": ["training methods", "training"],
    "sports": ["sports", "sport"],
    "auditorium": ["auditorium", "auditoriums"],
    "ict": ["ict", "information and communication technology"],
    "library": ["library", "book"],
    "health centre": ["health centre", "health center", "medical"],
    "hi": ["hi", "he", "h", "hey", "hello"],
    "help": ["help", "support", "assist"],
    "chatbot": ["chatbot", "bot", "assistant", "ai assistant"],
    "who are you": ["who are you", "what are you", "your identity"]
}

chat_history = []
import logging
import joblib

def extract_keyword_response(user_input):
    normalized = user_input.lower().strip()
    if normalized in standard_answers:
        return standard_answers[normalized]

    # direct known answer by key
    if normalized in known_answers:
        return known_answers[normalized]

    # try synonyms map
    for canonical, variants in intent_synonyms.items():
        for variant in variants:
            if variant in normalized:
                if canonical in known_answers:
                    return known_answers[canonical]
                break

    # partial match on known_answers
    for key, value in known_answers.items():
        if key in normalized:
            return value

    # closest known intent by string similarity
    close = difflib.get_close_matches(normalized, list(known_answers.keys()), n=1, cutoff=0.5)
    if close:
        return known_answers[close[0]]

    return None


def generate_llm_response(user_input):
    """Generate a response using OpenAI's GPT model based on user input."""
    user_input = (user_input or "").strip()
    if not user_input:
        return "Please type something so I can help you."

    keyword_response = extract_keyword_response(user_input)
    if keyword_response:
        return keyword_response

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        # Check if API key is missing or set to the default placeholder in .env
        if not api_key or api_key in ["your-api-key-here", "your-openai-api-key-here", ""]:
            return "🤖 **AI Not Configured:** I'm a chatbot assistant, but my AI brain (OpenAI GPT) isn't connected yet! Please add a valid `OPENAI_API_KEY` in the `.env` file to enable smart responses."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant chatbot for a college. Respond naturally and helpfully to user queries. Keep responses concise but informative."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        if response and response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        return "I understood your question, but I couldn't generate a response. Please try again."
    except Exception as e:
        logging.error(f"Error generating LLM response: {e}")
        # When OpenAI API fails (like incorrect key), tell the user explicitly
        if "Incorrect API key" in str(e) or "AuthenticationError" in str(type(e).__name__):
            return "🤖 **Authentication Error:** The OpenAI API key provided in the `.env` file is invalid. Please double check it."
        
        return "Sorry, I'm having trouble connecting to my AI servers right now. Please try again later."
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
        return render_template("chat.html", messages=chat_history)


@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.get_json(silent=True) or {}
        user_input = data.get('input', '').strip()
        if user_input == '':
            return jsonify({'error': 'No input provided.'}), 400

        answer = generate_llm_response(user_input)
        chat_history.append('You: ' + user_input)
        chat_history.append('Me: ' + answer)
        return jsonify({'response': answer})
    except Exception as e:
        logging.exception('Unhandled exception in api_chat')
        return jsonify({'error': 'Internal server error. Check server logs for details.'}), 500


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
