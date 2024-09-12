from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/submit', methods=['POST'])
def submit():
    if request.content_type == 'application/json':
        # Handle JSON data
        data = request.json
        user_data = data.get('userData', {})
        fields = data.get('fields', [])
        url = data.get('url', '')
        
        if not user_data or not fields:
            return jsonify({'error': 'Invalid data'}), 400

    elif request.content_type == 'multipart/form-data':
        # Handle text file data
        uploaded_file = request.files.get('file')
        if uploaded_file:
            user_data = uploaded_file.read().decode('utf-8')
            fields = request.form.getlist('fields[]')  # Extract fields from form data
            url = request.form.get('url', '')

            if not user_data or not fields:
                return jsonify({'error': 'Invalid data'}), 400
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    else:
        return jsonify({'error': 'Unsupported content type'}), 400

    # Prepare prompt for Google Gemini API, handle both JSON and text cases
    prompt = {
        "prompt": f"Fill the following form with the provided data:\nForm fields: {fields}\nUser data: {user_data}",
        "format": "json"
    }

    # Call Google Gemini API to generate the JSON structure for form filling
    response = model.generate_content(prompt)
    
    if 'error' in response:
        return jsonify({'error': 'Gemini API error', 'details': response['error']}), 500

    json_response = response.get('data', {})

    return jsonify(json_response), 200

if __name__ == '__main__':
    app.run(debug=True)
