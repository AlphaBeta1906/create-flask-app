from flask import Blueprint,jsonify,render_template

example = Blueprint("example",__name__)

@example.get("/")
def json_return():
    return jsonify(name="hello world")

@example.get("/index")
def templates_return():
    return render_template("index.html")