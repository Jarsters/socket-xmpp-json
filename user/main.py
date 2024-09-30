import os
import json
import time
import ipaddress
import threading

from user_utils.presence import get_presence_target, init_presence, logout, update_presence, view_users_presence
from user_utils.roster import add_roster, delete_roster, get_my_roster, update_roster, see_my_rosters
from user_utils.communicate_with_another_component import handle_message_from_manager, handle_message_from_relay
from user_utils.message import send_message_to_relay
from user_utils.packet import get_message_manager, get_message_tracker, send_message

from socketClient import SocketClient

def connect_to_tracker():
    ask = input("Local (y/n)?")
    if(ask.lower() == 'y'):
        client_tracker = SocketClient(None, 5000)
    else:
        client_tracker = SocketClient("103.178.153.189", 5000)
    # ct = Client Tracker
    ct = client_tracker.socket
    my_ip = client_tracker.localAddress
    ip_is_private = ipaddress.ip_address(my_ip[0]).is_private

    objek = {
        "ip_local": my_ip[0],
        "port": my_ip[1],
        "type": "client",
        "is_private": ip_is_private
    }
    
    send_message(ct, objek)
    message = get_message_tracker(ct)
    # message = json.loads(message)
    print(message)

    # ct.close()
    return client_tracker, message


s, message = connect_to_tracker()
client_to_tracker = s.socket
my_ip = s.localAddress

def get_component_manager(communicate):
    objek = {"message": "get components"}
    send_message(communicate, objek)
    return get_message_tracker(communicate)

def connect_to_manager(message, s, communicate):
    while not s:
        target = None
        for m in message:
            if(m.get("type").lower() == "manager"):
                target = m
                break
        if(target):
            ip = target.get("ip_local")
            port = target.get("port")
            print(ip, port)
            s = SocketClient(ip, port)
            my_ip = s.localAddress
            objek = {
                "ip_local": my_ip[0],
                "port": my_ip[1],
                "type": "client"
            }
            send_message(s.socket, objek)
            return s
        if(not s or not len(message)):
            print(f"Belum ada manager!")
            time.sleep(10)
            message = get_component_manager(communicate)
            for m in message:
                message = m

def get_component_relay(communicate, username):
    objek = {"type": "get_relay_less_connection", "username": username}
    send_message(communicate, objek)
    msg = get_message_manager(communicate)
    for m in msg:
        return json.loads(m)

def get_component_relay_auth(communicate, username, password, register=False):
    if(register):
        objek = {"type": "auth", "username": username, "password": password, "register": register}
    else:
        objek = {"type": "auth", "username": username, "password": password}
    send_message(communicate, objek)
    msg = get_message_manager(communicate)
    for m in msg:
        return json.loads(m)

def login_to_manager(communicate):
    username = input("Username: ")
    password = input("Password: ")
    message = get_component_relay_auth(communicate, username, password)
    return message, username, password

def register_to_manager(communicate):
    username = input("Username: ")
    password = input("Password: ")
    message = get_component_relay_auth(communicate, username, password, register=True)
    # print(message)
    return message, username, password

def connect_to_relay(message, s, communicate):
    username = None
    password = None
    count = 1
    while not s:
        target = None
        if(count > 1):
            components = message.get("component")
        else:
            components = message
        # print(components)
        if(components and count > 1):
            for m in components:
                if(m.get("type").lower() == "relay"):
                    target = m
                    break
        if(target):
            ip = target.get("ip_local")
            port = target.get("port")
            print(ip, port)
            s = SocketClient(ip, port)
            # objek = {"msg": "hello!"}
            objek = {"username": username, "message": "hello!"}
            send_message(s.socket, objek)
            return s, username
        if(not s):
            time.sleep(1)
            print(message)
            if(count == 1):
                message = get_component_relay_auth(communicate, username, password)
                count += 1
            if(message.get("code") == 404):
                print("Username or password is wrong!")
                message, username, password = login_to_manager(communicate)
            elif(message.get("code") == 409):
                print(message.get("msg"))
                message, username, password = register_to_manager(communicate)
            # elif(message.get("code") == 400 and not username and not password):
            #     print(message.get("msg"))
            #     message, username, password = register_to_manager(communicate)
            elif(message.get("error") and (message.get("code") == 403 or message.get("code") == 400)):
                print(message.get("msg"))
                print("Do you have an account?\n\
                      \t1. Yes (Login)\n\
                      \t2. No (Register)")
                choose = input("Input your answer with the number: ")
                if(choose == "1"):
                    message, username, password = login_to_manager(communicate)
                else:
                    message, username, password = register_to_manager(communicate)
            else:
                print(f"Belum ada relay!")
                time.sleep(2)
                message = get_component_relay(communicate, username)

s2 = None
client_to_manager = None
s2 = connect_to_manager(message, s2, client_to_tracker)

client_to_manager = s2.socket

s3 = None
client_to_relay = None
s3, username = connect_to_relay(message, s3, client_to_manager)

client_to_relay = s3.socket

threading.Thread(target=handle_message_from_relay, args=(client_to_relay, ), daemon=True).start()
threading.Thread(target=handle_message_from_manager, args=(client_to_manager, ), daemon=True).start()

objek_roster = {
    "stanza": "iq",
    "namespace": "roster",
    "from": username,
    "type": None,
    "query": None
}

print("Step 1, get roster")
get_my_roster(objek_roster, client_to_manager)
time.sleep(0.1)

objek_presence = {
    "stanza": "presence",
}

print("Step 2, init presence")
init_presence(objek_presence, client_to_manager)
time.sleep(0.1)

while True:
    time.sleep(0.3)
    receiver = input("Masukkan username penerima: ")
    msg = input("Masukkan pesan: ")
    if(msg.lower() == "clear cli"):
        result = os.system("cls")
        if(result):
            os.system("clear")
        continue
    elif(msg.lower() == "//roster"):
        print("Silahkan pilih\
              \n\t1. Meminta daftar teman ke server\
              \n\t2. Menambahkan teman\
              \n\t3. Mengubah nama teman\
              \n\t4. Menghapus teman\
              \n\t5. Melihat daftar teman")
        pilihan = int(input("Silahkan memilih pilihan dengan angkanya: "))
        if(pilihan == 1):
            get_my_roster(objek_roster, client_to_manager)
        elif(pilihan == 2):
            add_roster(objek_roster, client_to_manager)
        elif(pilihan == 3):
            update_roster(objek_roster, client_to_manager)
        elif(pilihan == 4):
            delete_roster(objek_roster, client_to_manager)
        elif(pilihan == 5):
            see_my_rosters()
        continue
    elif(msg.lower() == '//presence'):
        print("Silahkan pilih\
              \n\t1. Melihat status teman\
              \n\t2. Meminta presence\
              \n\t3. Mengubah bioku\
              \n\t4. Logout")
        pilihan = int(input("Silahkan memilih pilihan dengan angkanya: "))
        if(pilihan == 1):
            view_users_presence()
        elif(pilihan == 2):
            get_presence_target(objek_presence, client_to_manager)
        elif(pilihan == 3):
            objek_presence['from'] = username
            update_presence(objek_presence, client_to_manager)
        elif(pilihan == 4):
            objek_presence['from'] = username
            logout(objek_presence, client_to_manager)
            break
        continue
    # elif(msg.lower() == "//logout"):
    #     objek = {"type": "logout"}
    #     send_message(client_to_manager, objek)
    #     break
    send_message_to_relay(client_to_relay, username, receiver, msg)