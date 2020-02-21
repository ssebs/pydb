# pydb/__init__.py
from flask import Flask, jsonify, request
from flask_cors import CORS

from pydb.db import load_db, write_db


def handle_get(dbtup, key, path):
    db = dbtup[0]
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
                        ret[key].append(item)

    else:
        # print("No subpath, returning all")
        ret = {key: db[key]}

    return jsonify(ret)
# handle_get


def handle_post(dbtup, key, data):
    db = dbtup[0]
    keynames = []
    new_id = -1

    # Get new ID
    for item in db[key]:
        for (k, v) in item.items():
            if k == "id" and new_id <= v:
                new_id = v + 1
            keynames.append(k)

    # Verify data structure is OK
    for k in data.keys():
        if k not in keynames:
            return "Error! db structure does not match\n"

    # Create record
    new_obj = data.copy()
    new_obj["id"] = new_id
    db[key].append(new_obj)

    # print(db)
    # print(db[key])
    # print(new_obj)

    write_db(db, dbtup[1])

    return jsonify(db[key][new_id-1])
# handle_post


def create_app():
    app = Flask(__name__)
    CORS(app)
    dbtup = (load_db("db.json"), "db.json")

    # routes
    @app.route("/")
    def test():
        return "Flask up and running\n"

    @app.route("/api/<path:p>", methods=["GET"])
    def gets(p):
        # print(p)
        path = p.split("/")
        key = None
        for k in dbtup[0].keys():
            # print(k)
            if path[0] == k:
                key = k
        if key:
            return handle_get(dbtup, key, path[1:])
        else:
            return "No matching key\n"
    # gets

    @app.route("/api/<path:p>", methods=["POST"])
    def posts(p):
        # print(p)
        path = p.split("/")
        key = None
        data = request.json

        for k in dbtup[0].keys():
            # print(k)
            if path[0] == k:
                key = k
        if key:
            return handle_post(dbtup, key, data)
        else:
            return "No matching key\n"
    # posts

    app.app_context().push()
    return app
# create_app
