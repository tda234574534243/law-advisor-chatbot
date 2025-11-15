# file: backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from bot import answer_question, learn_from_feedback
from database import load_data

app = Flask(__name__, static_folder="../frontend")
load_data()

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    user_id = data.get("user_id", "default_user")
    if not question:
        return jsonify({"error": "Question required"}), 400
    try:
        answer, related = answer_question(user_id, question)
        return jsonify({"answer": answer, "related_questions": related})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    question = data.get("question", "")
    answer_text = data.get("answer", "")
    if not question or not answer_text:
        return jsonify({"error": "Question and answer required"}), 400
    learn_from_feedback(question, answer_text)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
