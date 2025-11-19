from flask import Flask, request, jsonify, send_from_directory
from bot import answer_question, learn_from_feedback
from database import load_data, list_feedback, promote_feedback
import os, json

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="../frontend"
)

# ===== Load dữ liệu =====
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LAW_DB_FILE = os.path.join(DATA_DIR, "law_db.json")

load_data()

with open(LAW_DB_FILE, "r", encoding="utf-8") as f:
    LAW_CORPUS = json.load(f)

# ===== Routes =====
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    question = (data.get("question") or "").strip()
    user_id = data.get("user_id", "default_user")
    if not question:
        return jsonify({"error": "Question required"}), 400
    
    answer, related = answer_question(user_id, question, law_corpus=LAW_CORPUS)
    return jsonify({"answer": answer, "related_questions": related})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json or {}
    question = data.get("question")
    answer_text = data.get("answer")
    user = data.get("user", "anonymous")
    if not question or not answer_text:
        return jsonify({"error": "Question and answer required"}), 400
    learn_from_feedback(question, answer_text, user_id=user)
    return jsonify({"status": "success"})

@app.route("/admin/feedback", methods=["GET"])
def admin_list_feedback():
    return jsonify(list_feedback())

@app.route("/admin/promote", methods=["POST"])
def admin_promote():
    data = request.json or {}
    idx = data.get("index")
    if idx is None:
        return jsonify({"error": "index required"}), 400
    try:
        ok, msg = promote_feedback(int(idx))
        return jsonify({"ok": ok, "msg": msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
