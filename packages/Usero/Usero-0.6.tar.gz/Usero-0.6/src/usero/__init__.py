_B = "password"
_A = "data.json"
import hashlib, os, json, uuid

if not os.path.exists(_A):
    open(_A, "w+").write("{}")
global DATA
DATA = json.loads(open(_A, "r").read())


def write_data(DATA):
    open(_A, "w+").write(json.dumps(DATA, indent=4, sort_keys=True))
    DATA = json.loads(open(_A, "r").read())


def add_user(username, password):
    A = username
    DATA[A] = {}
    DATA[A][_B] = hashlib.md5(str.encode(password)).hexdigest()
    DATA[A]["id"] = str(uuid.uuid4())
    write_data(DATA)


def remove_user(username):
    del DATA[username]
    write_data(DATA)


def set_user_key(username, key_name, key_value):
    DATA[username][key_name] = key_value
    write_data(DATA)


def remove_user_key(username, key_name):
    del DATA[username][key_name]
    write_data(DATA)


def login_to_user(username, password):
    if hashlib.md5(str.encode(password)).hexdigest() == DATA[username][_B]:
        return True
    else:
        return False
