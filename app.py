# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from rule_engine import evaluate

app = Flask(__name__)
CORS(app)

@app.route("/fire-rule", methods=["POST"])
def fire_rule():
    data = request.get_json()
    result = evaluate(data)  # Replace with your actual method
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)