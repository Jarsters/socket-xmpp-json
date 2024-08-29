from utils.get_time import get_timestamp
from utils.relay_less_connection import get_relay_with_less_connection
from utils.packet import send_message
import re


def helper_registering_user(users, username, password, timestamp):
    users[username] = {
        "username": username,
        "password": password,
        "bio": "Feel happy using this application! ;D",
        "online": True,
        "created_at": timestamp,
        "updated_at": timestamp
    }

def verify_whitespace(username):
    # return username.find(" ")
    return re.search("\s", username)

def handle_auth(message, users, components, communicate):
    username = message.get("username")
    # print("Lewat")
    # print(message)
    register = message.get("register")
    user = users.get(username)
    if(register):
        if(not username or verify_whitespace(username)):
            # print("Username kosong")
            objek = {"error": True, "msg": "Bad request", "code": 400}
            send_message(communicate, objek)
            return
        password = message.get("password")
        if(not password or verify_whitespace(password)):
            # print("Password kosong")
            objek = {"error": True, "msg": "Bad request", "code": 400}
            send_message(communicate, objek)
            return
        if(user):
            # print("Username yang dimasukkan telah digunakan yang lain")
            objek = {"error": True, "msg": "Username used", "code": 409}
            send_message(communicate, objek)
        else:
            # print("Registrasi berhasil")
            relay_for_user = get_relay_with_less_connection(components)
            objek = {"error": False, "msg": "Account created", "code": 201, "component": relay_for_user}
            password = message.get("password")
            timestamp = get_timestamp()
            helper_registering_user(users, username, password, timestamp)
            send_message(communicate, objek)
    else:
        if(not username or verify_whitespace(username)):
            # print("Username kosong")
            objek = {"error": True, "msg": "Bad request", "code": 400}
            send_message(communicate, objek)
            return
        password = message.get("password")
        if(not password or verify_whitespace(password)):
            # print("Password kosong")
            objek = {"error": True, "msg": "Bad request", "code": 400}
            send_message(communicate, objek)
            return
        # user = users.get(username)
        # print(users)
        # print(user)
        if(not user):
            objek = {"error": True, "msg": "User not found", "code": 404}
            send_message(communicate, objek)
            return
        password_db = user.get("password")
        if(user.get("online")):
            if(not password == password_db):
                # print("Password tidak cocok")
                objek = {"error": True, "msg": "User not found", "code": 404}
                send_message(communicate, objek)
                return
            # print("User sedang online")
            objek = {"error": True, "msg": "Already logged in", "code": 409}
            send_message(communicate, objek)
            return
        if(password == password_db):
            # print(f"{username} berhasil melakukan login")
            relay_for_user = get_relay_with_less_connection(components)
            objek = {"error": False, "msg": "Login successfull", "code": 200, "component": relay_for_user}
            users[username]['online'] = True
            users[username]['updated_at'] = get_timestamp()
            send_message(communicate, objek)
        else:
            # print("Password tidak cocok in else")
            objek = {"error": True, "msg": "User not found", "code": 404}
            send_message(communicate, objek)