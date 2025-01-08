import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import pdb

from exceptions import AppliedSuccessfullyException
from search_engine import SearchEngine
from utils import fill_form_json, parse_response_to_formfields, get_response_to_forms, run_with_timeout

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
engine = SearchEngine()


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        'action': "pong"
    })


@app.route('/submit', methods=['POST'])
def submit():
    timeout_seconds = 200
    data = request.json

    htmlContent = data['htmlContent']
    user_data = data['userData']
    url = data['url']
    try:
        # pdb.set_trace()
        forms = engine.extract_forms_from_url(url, htmlContent)
        if not forms:
            return jsonify({'error': 'Invalid HTML content'}), 400
        response = run_with_timeout(get_response_to_forms, timeout_seconds, forms, "analyze")
        # response = get_response_to_forms(forms, "analyze")
        if response is not None:
            fill_form_json(response)
        else:
            fill_form_json(forms)
        pdb.set_trace()
        return jsonify(json.dumps(response)), 200
    except AppliedSuccessfullyException:
        return jsonify({
            'status': "Job applied from manually server!"
        }), 200
    except Exception as e:
        print(f"Exception in main --> {e}")
        return jsonify({'error': 'Exception occur'}), 400


if __name__ == '__main__':
    app.run(debug=True)
