from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)
CORS(app)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    user_data = data.get('userData', '')  # User-provided text data
    fields = data.get('fields', [])       # Form fields
    url = data.get('url', '')             # URL of the form

    if not user_data or not fields:
        return jsonify({'error': 'Invalid data'}), 400

    # Prompt for Google Gemini API
    prompt = {
        "prompt": f"Fill the following form with the provided data:\nForm fields: {fields}\nUser data: {user_data}",
        "format": "json"
    }

    # Generate JSON response using Google Gemini AI
    response = model.generate_content(prompt)
    json_response = response.get('data', {})

    return jsonify(json_response), 200

if __name__ == '__main__':
    app.run(debug=True)
