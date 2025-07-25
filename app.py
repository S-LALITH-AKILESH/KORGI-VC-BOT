from flask import Flask,request,render_template,jsonify
import google.generativeai as genai
import os
from difflib import SequenceMatcher

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-2.5-flash")

conversation_history = []

def voice_assistant(user_input):
    global conversation_history
    prompt = f"""
        You are a helpful, conversational AI assistant named KORGI. Respond clearly and naturally to the user's message below.
        
        User: {user_input}
        
        Your response should be direct, informative, and friendly. If the user asks a factual question (like the time, date, or general knowledge), provide a concise and accurate answer. If the question is vague, use your best judgment to interpret and answer appropriately.
        Moreover, if you have not received a response from the user acknowledge your presence to the user and that you are awaiting for a response.
        """
    response = model.generate_content(prompt).text
    response = response.replace("**", "")
    response = response.replace("*", "")
    # conversation_history.append({
    #     'USER': user_input,
    #     'BOT': response
    # })
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process_voice", methods = ['POST'])
def process_voice():
    user_input = request.json.get('user_input')
    if not user_input:
        user_input = "(no input)"
        response = "Don't be KORGI. I'm waiting for your response."
    else:
        response = voice_assistant(user_input)

    conversation_history.append({
        'USER': user_input,
        'BOT': response
    })

    return jsonify({'response': response, 'conversation_history': conversation_history})

if __name__ == "__main__":
    app.run(debug = True)
