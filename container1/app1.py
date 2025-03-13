from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Persistent volume directory
PV_DIR = "/saikumar_PV_dir/"

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.json
    filename = data.get('file')
    file_data = data.get('data')

    if not filename:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    try:
        with open(PV_DIR + filename, "w") as f:
            f.write(file_data)
        return jsonify({"file": filename, "message": "Success."})
    except Exception as e:
        return jsonify({"file": filename, "error": "Error while storing the file."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    filename = data.get('file')
    product = data.get('product')

    if not filename or not product:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    try:
        response = requests.post("http://container2-service:6001/calculate", json={"file": filename, "product": product})
        return response.json()
    except Exception:
        return jsonify({"file": filename, "error": "Error processing file."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)