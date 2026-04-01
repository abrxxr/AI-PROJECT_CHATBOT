# cretrential
import db
import json
import os
import difflib
from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Google Gemini will be initialized inside the generate_llm_response function
standard_answers = {
    "what is your name?":"My name is CIT Assistant Chatbot!"
}
known_answers = {
    "intro": "Hello there 👋🏻, I am the CIT Assistant Chatbot. I represent Chennai Institute of Technology (CIT) 👨🏻‍💻📚 I am here to help answer any questions you have about our college, courses, transport, fees, and more. Send 'help' to know what I can do.",
    "help": "Send a keyword like skills, resume, education, contact, projects. I also answer free-text questions.",
    "skills": "I can code in Python, JavaScript, C, and build web/mobile apps.",
    "resume": "<img src='images/resume_thumbnail.png' class='resumeThumbnail'><div class='downloadSpace'><div class='pdfname'><img src='images/pdf.png'><label>CIT_College_Brochure.pdf</label></div><a href='assets/CIT_College_Brochure.pdf' download='CIT_College_Brochure.pdf'><img class='download' src='images/downloadIcon.svg'></a></div>",
    "education": "I am studying B.E. in Computer Science Engineering.",
    "chatbot": "I am your AI chatbot assistant built with GPT. You can ask me anything about your college, courses, and more.",
    "who are you": "I am an AI assistant for Chennai Institute of Technology (CIT).",
    "contact": "<div class='social'> <a target='_blank' href='tel:+914427152000'> <div class='socialItem' id='call'><img class='socialItemI' src='images/phone.svg'/><label class='number'></label></label></div> </a> <a href='mailto:info@citchennai.net'> <div class='socialItem'><img class='socialItemI' src='images/gmail.svg' alt=''></div> </a> <a target='_blank' href='https://www.citchennai.edu.in/'> <div class='socialItem'><img class='socialItemI' src='images/github.svg' alt=''></div> </a> </div>",
    "address": "<div class='mapview'><iframe src='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3887.828693892705!2d80.040176!3d12.982845!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a52f4d07355bab5%3A0xbb6063169c4ed4d9!2sChennai%20Institute%20of%20Technology!5e0!3m2!1sen!2sin!4v1712213197678!5m2!1sen!2sin' class='map'></iframe></div><label class='add'><address>Sarathy Nagar, Kundrathur<br>Chennai, Tamil Nadu 600069<br>INDIA</address>",
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
    "who are you": ["who are you", "what are you", "your identity"],
    "address": ["address", "location", "where are you", "map"]
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
    """Generate a response using Google Gemini model based on user input."""
    user_input = (user_input or "").strip()
    if not user_input:
        return "Please type something so I can help you."

    keyword_response = extract_keyword_response(user_input)
    if keyword_response:
        return keyword_response

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        # Check if API key is missing or set to the default placeholder in .env
        if not api_key or api_key in ["your-gemini-key-here", ""]:
            return '🤖 **AI Not Configured:** I need a "brain" to understand that! Please get your **free** Gemini API key from <a href="https://aistudio.google.com/app/apikey" target="_blank" class="alink">Google AI Studio</a> and add it as `GEMINI_API_KEY` to the `.env` file!'

        from google import genai
        client = genai.Client(api_key=api_key)
        
        prompt = f"You are the official AI assistant representing Chennai Institute of Technology (CIT), an engineering college. You are helping visitors on the college website. Respond naturally and helpfully. Keep responses concise but informative.\n\nUser Question: {user_input}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
        return "I understood your question, but I couldn't generate a response. Please try again."
    except Exception as e:
        logging.error(f"Error generating LLM response: {e}")
        error_msg = str(e).lower()
        if "api key" in error_msg or "authentication" in error_msg or "unauthorized" in error_msg or "400" in error_msg:
            return "🤖 **Authentication Error:** The Gemini API key provided in the `.env` file is invalid. Please verify it at Google AI Studio."
        
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
