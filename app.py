from flask import Flask, request, jsonify, render_template
from flask import send_from_directory, current_app
from flask_cors import CORS
import os
from pharmaGPT import (extract_prescription_info, get_drug_information, validate_prescription, 
                       check_drug_interactions, search_drug_or_condition)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/img/<path:filename>')
def send_img(filename):
    # Assuming images are stored in 'static/img'
    img_directory = os.path.join(current_app.root_path, 'static', 'img')
    return send_from_directory(img_directory, filename)

def validate_and_process_request(request_data, process_function):
    try:
        # Validate request data here if needed
        response = process_function(request_data)
        return jsonify(success=True, response=response)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 400

@app.route('/analyze_prescription', methods=['POST'])
def analyzeprescription():
    return validate_and_process_request(request.json['prescription_text'], extract_prescription_info)

@app.route('/get_drug_information', methods=['POST'])
def getdruginformation():
    drug_name = request.json.get('drug_name')
    if not drug_name:
        return jsonify({'error': 'No drug name provided'}), 400
    return validate_and_process_request(drug_name, get_drug_information)

@app.route('/validate_prescription', methods=['POST'])
def validateprescription():
    return validate_and_process_request(request.json['prescription_text'], validate_prescription)

@app.route('/check_drug_interactions', methods=['POST'])
def checkdruginteractions():
    return validate_and_process_request(request.json['drug_list'], check_drug_interactions)

@app.route('/search_drug_or_condition', methods=['POST'])
def searchdrugorcondition():
    return validate_and_process_request(request.json['query'], search_drug_or_condition)

if __name__ == '__main__':
    app.run(debug=False)
