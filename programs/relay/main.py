import json
import time
import ipaddress
import threading
import dotenv
import os

from relay_utils.import_abs_path import import_outside_utils
from relay_utils.message import send_message_to_target, send_packet_error
from relay_utils.packet import get_message, get_message_manager, get_message_relay, get_message_tracker, get_message_user, send_message
from database.init_data import my_username, connection_relay, user_in_another_relay, relay_to_tracker\
                            , my_ip, r, relay, s2, relay_to_manager, connections
# from socketServer import SocketServerRelay
from socketClient import SocketClientRelay

'''
    Relay connection_relay = {
        username_relay: connection_socket
    }
    User user_in_another_relay = {
        username_user: username_relay
    }
'''
try:
    module_socket = import_outside_utils("utils\\kelas\\", "socketServer.py")
except:
    module_socket = import_outside_utils("utils/kelas/", "socketServer.py")
SocketServer = module_socket.SocketServer

dotenv.load_dotenv()
IP_TRACKER = os.getenv("IP_TRACKER")

# Fungsionalitas terhubung ke tracker
def connect_to_tracker():
    ask = input("Local (y/n)?")
    if(ask.lower() == 'y'):
        client_tracker = SocketClientRelay(None, 5000, tipe="Tracker")
    else:
        client_tracker = SocketClientRelay(IP_TRACKER, 5000, tipe="Tracker")
    # ct = Client Tracker
    ct = client_tracker.socket
    my_ip = client_tracker.localAddress
    ip_is_private = ipaddress.ip_address(my_ip[0]).is_private

    objek = {
        "ip_local": my_ip[0],
        "port": my_ip[1],
        "type": "relay",
        "is_private": ip_is_private
    }

    send_message(ct, objek)
    message = get_message_tracker(ct)
    print(f"Komponen dari tracker:\r\n {message}")
    print("==========================================")
    
    return client_tracker, message

# Fungsionalitas meminta manager kepada tracker
def get_manager(communicate):
    objek = {"message": "get components"}
    send_message(communicate, objek)
    return get_message_tracker(communicate)

s, message = connect_to_tracker()
relay_to_tracker = s.socket
my_ip = s.localAddress

# Fungsionalitas menyimpan koneksi relay ke dalam daftar connection_relay
def config_new_relay(uname, communicate):
    global connection_relay
    connection_relay[uname] = communicate
    print(f"Koneksi dengan relay lainnya saat ini:\r\n{connection_relay}")

# Fungsionalitas untuk menghapus relay dan juga user yang terkoneksi dengannya
def delete_disconnected_relay(uname):
    global connection_relay, user_in_another_relay
    print(f"Menghapus informasi relay {uname}")
    # Menghapus relay dari daftar koneksi relay
    if(connection_relay.get(uname)):
        del connection_relay[uname]
    target_delete = []
    print(f"Koneksi dengan relay lainnya saat ini:\r\n{connection_relay}")
    for key, uname_relay in user_in_another_relay.items():
        if(uname_relay == uname):
            target_delete.append(key)
    # Menghapus koneksi user yang terhubung dengan relay yang baru saja dihapus
    for target in target_delete:
        del user_in_another_relay[target]
    print(f"Koneksi user pada relay lainnya saat ini:\r\n{user_in_another_relay}")

# Fungsionalitas mengirimkan informasi new user kepada relay lain yang terkoneksi
def send_new_user_to_another_relay(username_user, my_uname):
    global connection_relay
    # Membuat objek yang akan dikirimkan ke relay lain dengan message "new user"
    objek = {
        "message": "new user",
        "username_user": username_user,
        "relay_username": my_uname
    }
    # Mengirimkan packet kepada relay yang terkoneksi dengan relay
    for communicate in connection_relay.values():
        send_message(communicate, objek)

# Fungsionalitas mengelola komponen relay yang terkoneksi
def handle_component_relay(communicate, connected_relay_username):
    global connection_relay, user_in_another_relay
    error = False
    while not error:
        messages = get_message_relay(communicate)
        for msg in messages:
            message = json.loads(msg)
            # Menangani jika tiba-tiba mengalami error atau terputus untuk komponen relay
            if(message.get("error_msg")):
                print('==========================================')
                print(f"Komponen relay {connected_relay_username} mengalami error")
                print(message)
                # Memanggil fungsi untuk menangani relay yang error atau terputus
                delete_disconnected_relay(connected_relay_username)
                error = True
                print('==========================================')
                break
            # Mengelola packet yang masuk adalah stanza message
            elif(message.get("stanza") and message.get("stanza") == "message"):
                print('==========================================')
                print(f"Relay mendapatkan stanza message dari relay {connected_relay_username}")
                print(message)
                target = message.get("to")
                connection_target = connections.get(target)
                # Memanggil fungsi untuk mengirim stanza message kepada target
                result = send_message_to_target(connection_target, message)
                # Membuat objek untuk mengembalikan hasil dari pengiriman pesan, dengan nilai activity adalah "message from another relay"
                objek = {"from": message.get("from"), "to": message.get("to"), "activity": "message from another relay"}
                # Validitas apakah error atau success
                if(not result):
                    objek["error"] = 1
                else:
                    objek["success"] = 1
                send_message(communicate, objek)
                print('==========================================')
            # Mengelola packet dengan nilai message "new user"
            elif(message.get("message") and message.get("message").lower() == "new user"):
                print('==========================================')
                print("Relay mendapatkan pesan 'new user' dari relay lainnya")
                print(message)
                relay_uname = message.get("relay_username")
                username_user = message.get("username_user")
                print(f"Koneksi {username_user} kepada {relay_uname} telah tersambung!")
                # Mendaftarkan user ke dalam daftar koneksi relay pengirim
                user_in_another_relay[username_user] = relay_uname
                print(f"User didalam relay {relay_uname} adalah {user_in_another_relay}")
                print('==========================================')
            # Mengelola packet dengan nilai message "new user"
            elif(message.get("message") and message.get("message").lower() == "end user"):
                print('==========================================')
                print("Relay mendapatkan pesan 'end user' dari relay lainnya")
                print(message)
                relay_uname = message.get("username_relay")
                username_user = message.get("username_user")
                print(f"Koneksi {username_user} kepada {relay_uname} telah terputus!")
                # Menghapus user dari daftar koneksi relay pengirim
                del user_in_another_relay[username_user]
                print('==========================================')
            # Mengelola jika packet yang diterima nilai error adalah 1 dan nilai activity adalah "message from another relay"
            elif(message.get("error") and message.get("activity") == "message from another relay"):
                print('==========================================')
                print("Relay mendapatkan packet nilai error 1 dan nilai activity 'messsage from another relay'")
                print(message)
                initiate_user = message.get("from")
                communicate = connections[initiate_user]
                send_packet_error(communicate, 404, initiate_user)
                print('==========================================')
            elif(message.get("success") and message.get("activity") == "message from another relay"):
                print('==========================================')
                print("Relay mendapatkan packet nilai success 1 dan nilai activity 'messsage from another relay'")
                print(message)
                print('==========================================')
            else:
                continue

# Fungsionalitas untuk melakukan koneksi ke relay yang sudah ada di dalam sistem
def connect_to_another_relay(ip, port, uname):
    print("Melakukan koneksi dengan relay lainnya")
    # print(f"IP {ip}; PORT {port}")
    connection_with_another_relay = SocketClientRelay(ip, port, relay=True, tipe="Relay")
    # cwar = Client With Another Relay
    cwar = connection_with_another_relay.socket
    my_ip = connection_with_another_relay.localAddress
    ip_is_private = ipaddress.ip_address(my_ip[0]).is_private

    objek = {
        "ip_local": my_ip[0],
        "port": my_ip[1],
        "type": "relay",
        "is_private": ip_is_private,
        "relay_username": uname
    }
    
    send_message(cwar, objek)   
    messages = get_message_relay(cwar)
    for msg in messages:
        msg = json.loads(msg)
        print(f"Pesan dari relay senior: {msg}")
        if(msg.get("error_msg")):
            return False, False, False
        usernames_in_another_relay = msg.get("username_users")
        username_relay = msg.get("relay_username")

        threading.Thread(target=handle_component_relay, args=(cwar, username_relay), daemon=True).start()

        return connection_with_another_relay, username_relay, usernames_in_another_relay

# Fungsionalitas untuk konfigurasi awal saat relay online
def config_starter_relay(m): # m = message_from_manager
    global my_username, connection_relay, user_in_another_relay, my_ip
    mip = my_ip[0]
    mport = my_ip[1]
    my_username = m.get("username")
    connections = m.get("components") # Components Relay yang diberikan Manager
    for c in connections:
        ip = c.get("ip_local")
        port = c.get("port")
        # Mengecek agar tidak terkoneksi ke diri sendiri
        mine = ip == mip and port == mport
        if(not mine):
            connection_with_another_relay, username_relay, usernames_in_another_relay = connect_to_another_relay(ip, port, my_username)
            if(not username_relay):
                continue
            # Menyimpan koneksi dengan relay lainnya ke dalam connection_relay
            connection_relay[username_relay] = connection_with_another_relay.socket
            # Menyimpan user yang terkoneksi dengan relay yang baru saja disimpan
            for uname in usernames_in_another_relay:
                user_in_another_relay[uname] = username_relay
        print("==========================================")
    print(f"Connection Relay Konfigurasi: {connection_relay}")
    print(f"User in Another Relay Konfigurasi: {user_in_another_relay}")
    print("==========================================")


# Connect ke manager
while not s2:
    target = None
    for m in message:
        if(m.get("type").lower() == "manager"):
            target = m
            break
    if(target):
        ip = target.get("ip_local")
        port = target.get("port")
        s2 = SocketClientRelay(ip, port, tipe="Manager")
        relay_to_manager = s2.socket
        my_ip = s2.localAddress
        ip_is_private = ipaddress.ip_address(my_ip[0]).is_private
        objek = {
            "ip_local": my_ip[0],
            "port": my_ip[1],
            "type": "relay"
        }
        send_message(relay_to_manager, objek)
        messages = get_message_manager(relay_to_manager)
        for msg in messages:
            msg_from_manager = json.loads(msg)
            print(f"Pesan dari manager: {msg_from_manager}")
            print("==========================================")
            # Melakukan konfigurasi awal saat relay pertama kali online, dengan daftar komponen yang diberikan oleh manager
            config_starter_relay(msg_from_manager)
            my_port = my_ip[1]
            # r = SocketServerRelay(my_port)
            r = SocketServer(my_port)
            relay = r.socket
    if(not s2 or not len(message)):
        print("Belum ada manager!")
        time.sleep(10)
        # Meminta manager kepada tracker
        message = get_manager(relay_to_tracker)

# Fungsionalitas mengelola komponen user
def handle_component_user(communicate, relay_username, user_username):
    global relay_to_manager, connection_relay, user_in_another_relay
    error = False
    while not error:
        try:
            messages = get_message_user(communicate)
            for msg in messages:
                message = json.loads(msg)
                if(message.get("error_msg")):
                    print('==========================================')
                    print(f"Komponen user {user_username} mengalami error")
                    error = True
                    print('==========================================')
                elif(message.get("stanza") and message.get("stanza") == "message"):
                    print('==========================================')
                    print(f'Menerima packet stanza message dari user')
                    print(message)
                    target = message.get("to")
                    connection_target = connections.get(target)
                    # Target dalam relay yang sama
                    if(connection_target): 
                        print("Mengirim pesan kepada target pada relay yang sama")
                        send_message_to_target(connection_target, message)
                    # Target dalam relay yang berbeda
                    else: 
                        relay_user = user_in_another_relay.get(target)
                        print(f"Meneruskan pesan kepada relay {relay_user}")
                        if(not relay_user):
                            print("Terjadi error karena user yang dituju tidak terdapat di dalam sistem")
                            initiate_user = message.get("from")
                            # Mengirim packet error kepada user
                            send_packet_error(communicate, 404, initiate_user)
                            print('==========================================')
                            continue
                        socket_relay = connection_relay.get(relay_user)
                        send_message_to_target(socket_relay, message)
                    print('==========================================')
                else:
                    print('==========================================')
                    print("Inisialisasi awal dari user")
                    objek = {"msg": "Hallo target"}
                    send_message(communicate, objek)
                    print('==========================================')
        except Exception as e:
            print(e)
            print("Connection end...")
            # Objek yang akan diberitahukan kepada relay lainnya
            objek = {
                "message":"end user",
                "username_user": user_username,
                "username_relay": relay_username
            }
            # Menghapus user dari daftar user yang terkoneksi
            del connections[user_username]
            # Memberi tahu relay lain bahwa ada user yang terputus koneksinya dengan dirinya
            for r in connection_relay.values():
                send_message(r, objek)
            # Objek messagenya diganti "ecir" dan dikirim kepada manager
            objek["message"] = "ecir"
            # objek[tipe]
            send_message(relay_to_manager, objek)
            break

# Fungsionalitas untuk menerima segala koneksi TCP yang ingin terkoneksi dengan dirinya
while True:
    connection, address = relay.accept()
    messages = get_message(connection)
    for msg in messages:
        # print(msg)
        message = json.loads(msg)
        if(message.get("username")):
            print(f"Mendapatkan koneksi baru dari user {msg}")
            username = message.get("username")
            # Menyimpan user ke dalam daftar koneksinya
            connections[username] = connection
            # Membuat layanan eksklusif untuk mengelola komponen user
            threading.Thread(target=handle_component_user, args=(connection, my_username, username), daemon=True).start()
            objek = {
                "message": "ncir", # new connection in relay
                "username_relay": my_username,
                "tipe": "relay"
            }
            send_message(relay_to_manager, objek)
            send_new_user_to_another_relay(username, my_username)
        elif(message.get("type") == "relay"):
            print(f"Mendapatkan koneksi baru dari relay junior {msg}")
            uname_relay = message.get("relay_username")
            # Memanggil fungsi untuk menyimpan relay yang baru terkoneksi
            config_new_relay(uname_relay, connection)
            usernames = list(connections.keys())
            # Membuat objek yang akan dikirimkan kepada relay yang baru terkoneksi
            objek = {
                "relay_username": my_username,
                "username_users": usernames
            }
            send_message(connection, objek)
            # Membuat layanan eksklusif untuk mengelola komponen relay
            threading.Thread(target=handle_component_relay, args=(connection, my_username, ), daemon=True).start()
            print('==========================================')
        elif(message.get("msg") == "Hello relay!"):
            objek = {"msg": "Hallo target"}
            send_message(connection, objek)