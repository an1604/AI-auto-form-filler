from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    html_content = data.get('htmlContent', '')
    user_data = data.get('userData', '')
    url = data.get('url', '')

    if not html_content:
        return jsonify({'error': 'Invalid HTML content'}), 400

    # Prepare prompt for Google Gemini API
    prompt = f"""
    Analyze the following HTML content and identify form fields. 
    Return a JSON structure where each form field is mapped to the corresponding value from the provided user data.
    
    HTML Content: {html_content}
    User Data: {user_data}
    """

    # Generate JSON structure for form filling
    response = model.generate_content({"prompt": prompt, "format": "json"})
    json_response = response.get('data', {})

    return jsonify(json_response), 200

if __name__ == '__main__':
    app.run(debug=True)
