# from manager_utils.get_time import get_timestamp
from manager_utils.import_abs_path import import_outside_utils
from manager_utils.packet import send_message
import re

from database.sqlite.component import get_relay_with_less_connection_db
from database.sqlite.user import get_user_by_username, save_user_to_db, update_status_online, get_all_users

try:
    module_get_time = import_outside_utils("utils\\utility\\", "get_time.py")
except:
    module_get_time = import_outside_utils("utils/utility/", "get_time.py")
get_timestamp = module_get_time.get_timestamp

# Fungsionalitas untuk menyimpan data user yang baru registrasi
def helper_registering_user(username, password, timestamp):
    print(f"Menyimpan data user {username} ke dalam database")
    objek = {
        "username": username,
        "password": password,
        "bio": "Feel happy using this application! ;D",
        "online": 1,
        "created_at": timestamp,
        "updated_at": timestamp
    }
    save_user_to_db(list(objek.values()))
    # Mencetak semua user yang terdapat dalam user sekarang
    print(get_all_users())

# Fungsionalitas validasi apakah data terdapat karakter whitespace
def verify_whitespace(data):
    return re.search("\s", data)

# Fungsionalitas yang bertanggung jawab mengelola permintaan registrasi atau login
def handle_auth(message, communicate, user_db=None, f=None):
    username = message.get("username")
    register = message.get("register")
    user = get_user_by_username(username)
    if(register):
        # print(f'Terjadi permintaan registrasi dari user {username}\r\n')
        if(user):
            print(f"Terjadi error karena username {username} telah digunakan yang lain")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa registasi gagal
            objek = {"error": True, "msg": "Username used", "code": 409}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False
        elif(not username or verify_whitespace(username)):
            print(f"Terjadi error karena username {username} kosong atau terdapat whitespace")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa registasi gagal
            objek = {"error": True, "msg": "Bad request", "code": 400}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False
        password = message.get("password")
        if(not password or verify_whitespace(password)):
            print(f"Terjadi error karena password kosong atau terdapat whitespace")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa registasi gagal
            objek = {"error": True, "msg": "Bad request", "code": 400}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False
        else:
            print(f'Terjadi permintaan registrasi dari user {username}\r\n')
            print(message)
            print("Registrasi berhasil\r\n")
            # Mendapatkan relay paling sedikit yang akan diberikan kepada user
            relay_for_user = get_relay_with_less_connection_db()
            # Pembuatan packet untuk pemberitahuan kepada user bahwa registasi berhasil
            objek = {"error": False, "msg": "Account created", "code": 201, "component": relay_for_user}
            print(f"Packet success yang dikirimkan kepada user {username}\r\n{objek}")
            password = message.get("password")
            timestamp = get_timestamp()
            # Menyimpan user ke dalam database
            helper_registering_user(username, password, timestamp)
            send_message(communicate, objek)
            return True
    else:
        print(f"Terjadi permintaan login dari user {username}\r\n")
        if(not username or verify_whitespace(username)):
            print(f"Terjadi error karena username {username} kosong atau terdapat whitespace")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa login gagal
            objek = {"error": True, "msg": "Bad request", "code": 400}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False
        password = message.get("password")
        if(not password or verify_whitespace(password)):
            print(f"Terjadi error karena password kosong atau terdapat whitespace")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa login gagal
            objek = {"error": True, "msg": "Bad request", "code": 400}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False
        if(not user):
            print(f"Terjadi error karena username {username} yang dimasukkan tidak terdapat dalam sistem")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa login gagal
            objek = {"error": True, "msg": "User not found", "code": 404}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False
        password_db = user[1]
        if(user[3]):
            if(not password == password_db):
                print(f"Terjadi error karena password tidak sesuai")
                # Pembuatan packet untuk pemberitahuan kepada user bahwa login gagal
                objek = {"error": True, "msg": "Bad request", "code": 400}
                print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
                send_message(communicate, objek)
                return False
            print(f"Terjadi error karena user mencoba login ke {username} yang sedang online")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa login gagal
            objek = {"error": True, "msg": "Already logged in", "code": 409}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False
        if(password == password_db):
            print(f"{username} berhasil melakukan login\r\n")
            # Mendapatkan relay paling sedikit yang akan diberikan kepada user
            relay_for_user = get_relay_with_less_connection_db()
            # Pembuatan packet untuk pemberitahuan kepada user bahwa login berhasil
            objek = {"error": False, "msg": "Login successfull", "code": 200, "component": relay_for_user}
            # Memperbarui status dari user dari offline ke online
            print(f"Packet success yang dikirimkan kepada user {username}\r\n{objek}")
            update_status_online(["online", "updated_at"], (1, get_timestamp(),), ['user_id'], (username,))
            send_message(communicate, objek)
            return True
        else:
            print(f"Terjadi error karena password tidak sesuai")
            # Pembuatan packet untuk pemberitahuan kepada user bahwa login gagal
            objek = {"error": True, "msg": "Bad request", "code": 400}
            print(f"Packet error yang dikirimkan kepada user {username}\r\n{objek}")
            send_message(communicate, objek)
            return False