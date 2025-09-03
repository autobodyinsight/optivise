# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from rule_engine import run_rules  # ✅ This matches your actual function

app = Flask(__name__)
CORS(app)

@app.route('/fire', methods=["POST"])
def fire_rule():
    data = request.get_json()
    result = run_rules(data)  # ✅ Call the correct function
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)