from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder="client", static_url_path="")
CORS(app)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "students": os.path.join(DATA_DIR, "students.json"),
    "classes": os.path.join(DATA_DIR, "classes.json"),
    "activities": os.path.join(DATA_DIR, "activities.json")
}

for f in FILES.values():
    if not os.path.exists(f):
        with open(f, "w", encoding="utf-8") as file:
            json.dump([], file, indent=2)


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    return send_from_directory("client", "index.html")


# Alunos
@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(load_data(FILES["students"]))


@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()
    students = load_data(FILES["students"])
    data["id"] = len(students) + 1
    students.append(data)
    save_data(FILES["students"], students)
    return jsonify(data), 201


# Turmas
@app.route("/api/classes", methods=["GET"])
def get_classes():
    return jsonify(load_data(FILES["classes"]))


@app.route("/api/classes", methods=["POST"])
def add_class():
    data = request.get_json()
    classes = load_data(FILES["classes"])
    data["id"] = len(classes) + 1
    classes.append(data)
    save_data(FILES["classes"], classes)
    return jsonify(data), 201


# Atividades
@app.route("/api/activities", methods=["GET"])
def get_activities():
    return jsonify(load_data(FILES["activities"]))


@app.route("/api/activities", methods=["POST"])
def add_activity():
    data = request.get_json()
    activities = load_data(FILES["activities"])
    data["id"] = len(activities) + 1
    activities.append(data)
    save_data(FILES["activities"], activities)
    return jsonify(data), 201


# Inteligência Artificial (recomendação simples)
@app.route("/api/ai/recommend", methods=["POST"])
def ai_recommend():
    from ai.ai_recommender import recommend_activity
    data = request.get_json()
    activities = data.get("activities", [])
    query = data.get("query", "")
    return jsonify(recommend_activity(activities, query))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
