# pydb/__init__.py
from flask import Flask, jsonify, request
from flask_cors import CORS

from pydb.db import load_db

# init


def handle_get(db, key, path):
    ret = {}
    # print(path)
    if path != [] and path != [""]:
        ret[key] = []
        # For every item in the list
        for item in db[key]:
            # For every obj in the item
            for (k, v) in item.items():
                # Do search
                if path[0].lower() in str(v).lower():
                    if item not in ret[key]:
                        ret[key].append(x)

    else:
        # print("No subpath, returning all")
        ret = {key: db[key]}

    return jsonify(ret)
# handle_get


def handle_post(db, key, data):
    pass
    print(data)
    # Get new ID and add info
    return jsonify(data)
# handle_post


def create_app():
    app = Flask(__name__)
    CORS(app)
    db = load_db("db.json")

    # routes
    @app.route("/")
    def test():
        return "Flask up and running\n"

    @app.route("/api/<path:p>", methods=["GET"])
    def gets(p):
        # print(p)
        path = p.split("/")
        key = None
        for k in db.keys():
            # print(k)
            if path[0] == k:
                key = k
        if key:
            return handle_get(db, key, path[1:])
        else:
            return "No matching key\n"
    # gets

    @app.route("/api/<path:p>", methods=["POST"])
    def posts(p):
        # print(p)
        path = p.split("/")
        key = None
        data = request.json

        for k in db.keys():
            # print(k)
            if path[0] == k:
                key = k
        if key:
            return handle_post(db, key, data)
        else:
            return "No matching key\n"
    # posts

    app.app_context().push()
    return app
# create_app
