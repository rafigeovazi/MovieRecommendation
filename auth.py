import json
import hashlib
import os

USER_FILE = "users.json"

# hash password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# load user function
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)

# save user function
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# register user function
def register_user(username, password):
    users = load_users()
    if username in users:
        return False  # Username already exists
    users[username] = hash_password(password)
    save_users(users)
    return True

# Login user function
def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    return username in users and users[username] == hashed
