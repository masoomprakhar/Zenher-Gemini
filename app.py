from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

with open("qa_data.json", encoding="utf-8") as f:
    qa_data = json.load(f)

def search_static_qa(query):
    for qa in qa_data:
        if query.lower() in qa["question"].lower():
            return qa["answer"]
    return None

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

@app.route("/ask", methods=["POST"])
def ask():
    user_q = request.json.get("question", "")
    static = search_static_qa(user_q)
    if static:
        return jsonify({"answer": static})
    try:
        ai_reply = ask_gemini(user_q)
    except Exception as e:
        ai_reply = "Sorry, Gemini is unavailable right now."
    return jsonify({"answer": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
