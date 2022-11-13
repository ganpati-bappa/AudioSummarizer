from transcript import run
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def summary():
    if request.method == "POST":
        file = request.files.get('audio')
        return jsonify(run(file))


if __name__ == "__main__":
    app.run(debug=True)
