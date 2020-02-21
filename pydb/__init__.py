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
                # Check if searching by ID
                if int(path[0]):
                    if k == "id" and v == int(path[0]):
                        ret[key].append(item)
                else:
                    # Do string search otherwise
                    if path[0].lower() in str(v).lower():
                        if item not in ret[key]:
                            ret[key].append(item)
    else:
        # No query, showing all
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


def handle_put(dbtup, key, path, data):
    db = dbtup[0]
    keynames = []
    intpath = int(path[0])
    index = -1

    # missing id
    if path == [] or path == [""]:
        return "Error! You must provide an ID in the path\n"

    if "id" not in data:
        return "Error! You must provide an ID in the object\n"

    if intpath != data["id"]:
        return "Error! The ID in the path and in the object must match\n"

    # Update record
    try:
        for i, item in enumerate(db[key]):
            for (k, v) in item.items():
                keynames.append(k)
                if intpath == data["id"]:
                    if k == "id" and v == intpath:
                        # print(item)
                        # print(data)
                        db[key][i] = data.copy()
                        index = i
    except Exception as e:
        return f"Error! {e}"

    # Verify data structure is OK
    for k in data.keys():
        if k not in keynames:
            return "Error! db structure does not match\n"

    write_db(db, dbtup[1])

    return jsonify(db[key][index])
# handle_post


def handle_delete(dbtup, key, path):
    db = dbtup[0]
    intpath = int(path[0])
    index = -1

    # missing id
    if path == [] or path == [""]:
        return "Error! You must provide an ID in the path\n"

    try:
        for i, item in enumerate(db[key]):
            for (k, v) in item.items():
                if k == "id" and v == intpath:
                    # print(item)
                    del db[key][i]
    except Exception as e:
        return f"Error! {e}"

    # print(db)
    write_db(db, dbtup[1])

    return f"Success! Deleted id: {intpath}\n"
# handle_delete


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

    @app.route("/api/<path:p>", methods=["PUT", "PATCH"])
    def puts(p):
        # print(p)
        path = p.split("/")
        key = None
        data = request.json

        for k in dbtup[0].keys():
            # print(k)
            if path[0] == k:
                key = k
        if key:
            return handle_put(dbtup, key,  path[1:], data)
        else:
            return "No matching key\n"
    # puts

    @app.route("/api/<path:p>", methods=["DELETE"])
    def deletes(p):
        # print(p)
        path = p.split("/")
        key = None
        for k in dbtup[0].keys():
            # print(k)
            if path[0] == k:
                key = k
        if key:
            return handle_delete(dbtup, key, path[1:])
        else:
            return "No matching key\n"
    # deletes

    app.app_context().push()
    return app
# create_app
