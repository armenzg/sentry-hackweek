from flask import jsonify, request, Flask

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    print(request.data)
    print(request.headers)
    # return "<p>Hello, World!</p>"
    return jsonify({}), 200
