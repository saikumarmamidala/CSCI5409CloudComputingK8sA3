from flask import Flask, request, jsonify
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

PV_DIR = "/mnt/data/" 

@app.route('/calculate', methods=['POST'])
def calculate():
    logger.info("Received request to calculate product sum")
    data = request.json
    filename = data.get('file')
    product = data.get('product')

    if not filename or not product:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    try:
        with open(PV_DIR + filename, "r") as f:
            lines = f.readlines()

        if not lines[0].strip() == "product, amount":
            return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400

        total = sum(int(line.split(",")[1]) for line in lines[1:] if line.split(",")[0] == product)
        return jsonify({"file": filename, "sum": total})
    except FileNotFoundError:
        return jsonify({"file": filename, "error": "File not found."}), 404
    except Exception:
        return jsonify({"file": filename, "error": "Error processing file."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6001)
