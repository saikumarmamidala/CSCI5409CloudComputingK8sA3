from flask import Flask, request, jsonify
import os
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Persistent volume directory
PV_DIR = "/mnt/data/" 

@app.route('/store-file', methods=['POST'])
def store_file():
    logger.info("Received request to store file")
    data = request.json

    filename = data.get('file')
    file_data = data.get('data')

    if not filename:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    try:
        with open(os.path.join(PV_DIR, filename), "w") as f:
            f.write(file_data)
        return jsonify({"file": filename, "message": "Success."})
    except Exception as e:
        logger.error(f"Error storing file: {str(e)}")
        return jsonify({"file": filename, "error": "Error while storing the file."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    logger.info("Received request to calculate")
    data = request.json
    filename = data.get('file')
    product = data.get('product')

    if not filename or not product:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    try:
        response = requests.post("http://container2-service:6001/calculate", json={"file": filename, "product": product})
        return response.json()
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({"file": filename, "error": "Error processing file."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)
