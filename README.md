# PharmaGPT

PharmaGPT is a Flask-based web service designed to assist pharmacists and healthcare professionals by providing an easy-to-use interface for analyzing prescriptions, retrieving drug information, validating prescriptions, checking drug interactions, and searching for drugs or conditions using AI technology.

## Features

- **Analyze Prescriptions:** Extracts key information from prescription texts.
- **Prescription Upload:** Allows users to upload an image of a prescription, which is then processed using OCR and AI to extract and clean text data.
- **Drug Information:** Retrieves detailed information about drugs.
- **Prescription Validation:** Checks prescriptions for potential errors.
- **Drug Interaction Check:** Identifies interactions between multiple drugs.
- **Drug or Condition Search:** Searches for drugs or medical conditions.

## Installation

To set up PharmaGPT on your local machine, follow these steps:

1. Clone this repository to your local machine.
2. Ensure you have Python 3.x installed.
3. Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

4. Set your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY='your_openai_api_key_here'
    ```

5. Run the Flask application:

    ```bash
    flask run
    ```

## Usage

The web interface provides easy access to upload prescriptions and input text for analysis. The API also provides several endpoints:

- `POST /upload_and_process_image`: Uploads a prescription image for text extraction and processing.
- `POST /analyze_prescription`: Analyzes the given prescription text.
- `POST /get_drug_information`: Retrieves information for a specified drug.
- `POST /validate_prescription`: Validates the given prescription text.
- `POST /check_drug_interactions`: Checks for interactions between a list of drugs.
- `POST /search_drug_or_condition`: Searches for information on a drug or medical condition.

When uploading a prescription image, the service uses OCR technology to extract the text and then leverages AI to preprocess this text, ensuring that it is clear and structured, ready for further analysis.

## Development

To contribute to PharmaGPT or to build on top of it, clone the repository and make sure to follow the best practices for Flask and RESTful API development. Feel free to submit pull requests.