from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)
CORS(app)
model = genai.GenerativeModel('gemini-1.5-flash')

def process_data(data):
  user_data = data.get('userData', '')
  fields = data.get('fields', [])
  url = data.get('url', '')

  if not user_data or not fields:
    return jsonify({'error': 'Invalid data'}), 400

  prompt = {
    "prompt": f"Fill the following form with the provided data:\nForm fields: {fields}\nUser data: {user_data}",
    "format": "json"
  }

  response = model.generate_content(prompt)
  json_response = response.get('data', {})

  return jsonify(json_response), 200

@app.route('/submit', methods=['POST'])
def submit():
  data = request.json
  return process_data(data)

if __name__ == '__main__':
  app.run(debug=True)
