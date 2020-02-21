# pydb/db.py
import os
import json


def load_db(filename="./pydb/files/default.json"):
    db = {}
    try:
        with open(filename, "r") as f:
            db = json.loads(f.read())
    except Exception as e:
        print(f"Could not load db. {e}")
        exit(1)
    # print(db)
    return db
# load_db


def write_db(db, filename="./pydb/files/default.json"):
    try:
        with open(filename, "w") as f:
            f.write(json.dumps(db))
    except Exception as e:
        print(f"Could not save db. {e}")
        exit(1)
    # print(db)
# write_db
