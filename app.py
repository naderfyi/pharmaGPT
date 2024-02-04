from flask import Flask, request, jsonify, render_template
from flask import send_from_directory, current_app
from flask_cors import CORS
import os
from pharmaGPT import (extract_prescription_info, get_drug_information, validate_prescription, 
                       check_drug_interactions, search_drug_or_condition)

from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image

app = Flask(__name__)
CORS(app)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"An error occurred while extracting text: {str(e)}"
    
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/upload_and_process_image', methods=['POST'])
def upload_and_process_image():
    action = request.form.get('action') or (request.json and request.json.get('action'))
    if not action:
        return jsonify({'error': 'No action specified'}), 400
    
    request_data = ''
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'No selected file or file type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from the uploaded image
        request_data = extract_text_from_image(file_path)
    elif request.json and 'input' in request.json:
        request_data = request.json['input']

    if not request_data:
        return jsonify({'error': 'No input provided'}), 400

    # Mapping actions to processing functions
    action_mapping = {
        'analyze_prescription': extract_prescription_info,
        'validate_prescription': validate_prescription,
        'get_drug_information': get_drug_information,
        'check_drug_interactions': lambda x: check_drug_interactions(x.split(',')),
        'search_drug_or_condition': search_drug_or_condition
    }

    process_function = action_mapping.get(action)
    if not process_function:
        return jsonify({'error': 'Invalid action'}), 400

    return validate_and_process_request(request_data, process_function)

@app.route('/img/<path:filename>')
def send_img(filename):
    img_directory = os.path.join(current_app.root_path, 'static', 'img')
    return send_from_directory(img_directory, filename)

def validate_and_process_request(request_data, process_function):
    try:
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
