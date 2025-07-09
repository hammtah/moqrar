from flask import Flask, request, jsonify
import json
import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all domains by default

# ... your routes ...
DATA_FILE = 'data.json'

@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({'error': 'data.json not found'}), 404
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            records = json.load(f)
        except Exception:
            return jsonify({'error': 'Failed to read data.json'}), 500
    return jsonify(records)

@app.route('/save_progress', methods=['POST'])
def save_progress():
    data = request.json
    date = data.get('date')
    progress = data.get('progress')
    if date is None or progress is None:
        return jsonify({'error': 'Missing data'}), 400

    # Read existing data
    if not os.path.exists(DATA_FILE):
        return jsonify({'error': 'data.json not found'}), 404
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            records = json.load(f)
        except Exception:
            return jsonify({'error': 'Failed to read data.json'}), 500

    # Update the record
    updated = False
    for record in records:
        if record.get('date') == date:
            record['progress'] = progress
            updated = True
            break
    if not updated:
        return jsonify({'error': 'Date not found'}), 404

    # Write back
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # app.run(debug=True) 
    app.run(host="0.0.0.0", port=5000)