import socket
import json
import time
import ipaddress
import threading

from utils.message import send_message_to_target, send_packet_error
from utils.packet import get_message, get_message_manager, get_message_relay, get_message_tracker, get_message_user, send_message
from database.dummy import my_username, connection_relay, user_in_another_relay, relay_to_tracker\
                            , my_ip, r, relay, s2, relay_to_manager, connections

class SocketClient:
    def __init__(self, ip_target, port_target, relay=False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if(not ip_target):
            ip_target = self.getMyLocalAddress()[0]
        self.address_target = (ip_target, port_target)
        self.localAddress = self.getMyLocalAddress()
        print(f"Try to connecting.... {ip_target} - {port_target}")
        res = self.connectToTarget(relay)
        print("Connected")
    def connectToTarget(self, relay):
        try: 
            self.socket.connect(self.address_target)
            return True
        except Exception as e:
            print(e)
            print("Error when connecting....")
            print("Quit program")
            self.socket.close()
            if(not relay):
                exit()
            return False
    def getMyLocalAddress(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.connect(("8.8.8.8", 80))
        output = udp.getsockname()
        udp.close()
        del udp
        return output

class SocketServer:
    def __init__(self, port=5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.localIP = self.getMyLocalIP()
        self.socket.bind((self.localIP, port))
        self.socket.listen()
    def getMyLocalIP(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.connect(("8.8.8.8", 80))
        output = udp.getsockname()[0]
        udp.close()
        del udp
        return output

def connect_to_tracker():
    # client_tracker = SocketClient("192.168.1.6", 5000)
    client_tracker = SocketClient(None, 5000)
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

    # stringObjek = json.dumps(objek)

    # ct.send(stringObjek.encode())
    send_message(ct, objek)
    message = get_message_tracker(ct)
    # message = json.loads(message)
    print(message)

    # ct.close()
    return client_tracker, message

def get_manager(communicate):
    objek = {"message": "get components"}
    send_message(communicate, objek)
    return get_message_tracker(communicate)

'''
    Relay connection_relay = {
        username_relay: connection_socket
    }
    User user_in_another_relay = {
        username_user: username_relay
    }
'''



s, message = connect_to_tracker()
relay_to_tracker = s.socket
my_ip = s.localAddress

def config_new_relay(uname, communicate):
    global connection_relay
    connection_relay[uname] = communicate

def delete_disconnected_relay(uname):
    global connection_relay, user_in_another_relay
    del connection_relay[uname]
    target_delete = []
    for key, uname_relay in user_in_another_relay.items():
        if(uname_relay == uname):
            target_delete.append(key)
    for target in target_delete:
        del user_in_another_relay[target]

def send_new_user_to_another_relay(username_user, my_uname):
    global connection_relay
    objek = {
        "message": "new user",
        "username_user": username_user,
        "relay_username": my_uname
    }
    for communicate in connection_relay.values():
        # print(communicate)
        send_message(communicate, objek)

def handle_component_relay(communicate, connected_relay_username):
    global connection_relay, user_in_another_relay
    error = False
    while True:
        if(error):
            delete_disconnected_relay(connected_relay_username)
            break
        messages = get_message_relay(communicate)
        for msg in messages:
            message = json.loads(msg)
            if(message.get("error_msg")):
                print("Masuk ke sini")
                error = True
            if(message.get("stanza") and message.get("stanza") == "message"):
                    # print("masuk sini")
                    target = message.get("to")
                    connection_target = connections.get(target)
                    result = send_message_to_target(connection_target, message)
                    objek = {"from": message.get("from"), "to": message.get("to"), "activity": "message from another relay"}
                    if(not result):
                        objek["error"] = 1
                    else:
                        objek["success"] = 1
                    send_message(communicate, objek)
            elif(message.get("message") and message.get("message").lower() == "new user"):
                relay_uname = message.get("relay_username")
                username_user = message.get("username_user")
                print(f"Koneksi {username_user} kepada {relay_uname} telah tersambung!")
                user_in_another_relay[username_user] = relay_uname
                print(f"User didalam relay {relay_uname} adalah {user_in_another_relay}")
            elif(message.get("message") and message.get("message").lower() == "end user"):
                relay_uname = message.get("username_relay")
                username_user = message.get("username_user")
                print(f"Koneksi {username_user} kepada {relay_uname} telah terputus!")
                del user_in_another_relay[username_user]
            elif(message.get("error") and message.get("activity") == "message from another relay"):
                initiate_user = message.get("from")
                print(initiate_user)
                communicate = connections[initiate_user]
                send_packet_error(communicate, 404, initiate_user)
            else:
                continue

def connect_to_another_relay(ip, port, uname):
    # print(f"Masuk connect to another relay IP: {ip}, Port: {port}")
    connection_with_another_relay = SocketClient(ip, port, relay=True)
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
        if(msg.get("error_msg")):
            return False, False, False
        usernames_in_another_relay = msg.get("username_users")
        username_relay = msg.get("relay_username")

        threading.Thread(target=handle_component_relay, args=(cwar, username_relay), daemon=True).start()

        return connection_with_another_relay, username_relay, usernames_in_another_relay

def config_starter_relay(m): # m = message_from_manager
    global my_username, connection_relay, user_in_another_relay, my_ip
    mip = my_ip[0]
    mport = my_ip[1]
    my_username = m.get("username")
    connections = m.get("components") # Components Relay
    print(f"CONNECTIONS: {connections}")
    for c in connections:
        ip = c.get("ip_local")
        port = c.get("port")
        if(ip == mip and port != mport):
            connection_with_another_relay, username_relay, usernames_in_another_relay = connect_to_another_relay(ip, port, my_username)
            # print(connection_with_another_relay, username_relay, usernames_in_another_relay)
            if(not username_relay):
                # print("Masuk sini")
                continue
            connection_relay[username_relay] = connection_with_another_relay.socket
            for uname in usernames_in_another_relay:
                user_in_another_relay[uname] = username_relay
    print(f"Connection Relay: {connection_relay}")
    print(f"User in Another Relay: {user_in_another_relay}")


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
        # print(ip, port)
        s2 = SocketClient(ip, port)
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
            config_starter_relay(msg_from_manager)
            r = SocketServer(my_ip[1])
            relay = r.socket
    if(not s2 or not len(message)):
        print("Belum ada manager!")
        time.sleep(10)
        message = get_manager(relay_to_tracker)

def handle_component_user(communicate, relay_username, user_username):
    global relay_to_manager, connection_relay, user_in_another_relay
    while True:
        try:
            messages = get_message_user(communicate)
            for msg in messages:
                message = json.loads(msg)
                if(message.get("stanza") and message.get("stanza") == "message"):
                    target = message.get("to")
                    connection_target = connections.get(target)
                    result = None
                    if(connection_target): # Target dalam relay yang sama
                        result = send_message_to_target(connection_target, message)
                    else: # Target dalam relay yang berbeda
                        # print("masuk")
                        # print(user_in_another_relay)
                        relay_user = user_in_another_relay.get(target)
                        if(not relay_user):
                            initiate_user = message.get("from")
                            send_packet_error(communicate, 404, initiate_user)
                            continue
                        socket_relay = connection_relay.get(relay_user)
                        send_message_to_target(socket_relay, message)
                        # print(result)
                        # print("lewat")
                elif(message.get('error_msg')):
                    if(message.get("tipe") == "winerror"):
                        break
                    # print(message)
                else:
                    objek = {"msg": "Hallo target"}
                    send_message(communicate, objek)
        except Exception as e:
            print(e)
            print("Connection end...")
            objek = {
                "message":"end user",
                "username_user": user_username,
                "username_relay": relay_username
            }
            del connections[user_username]
            for r in connection_relay.values():
                send_message(r, objek)
            objek["message"] = "ecir"
            send_message(relay_to_manager, objek)
            break

# count = 0
while True:
    connection, address = relay.accept()
    messages = get_message(connection)
    for msg in messages:
        print(msg)
        message = json.loads(msg)
        if(message.get("username")):
            username = message.get("username")
            connections[username] = connection
            threading.Thread(target=handle_component_user, args=(connection, my_username, username), daemon=True).start()
            objek = {
                "message": "ncir", # new connection in relay
                "username_relay": my_username
            }
            send_message(relay_to_manager, objek)
            send_new_user_to_another_relay(username, my_username)
        elif(message.get("type") == "relay"):
            uname_relay = message.get("relay_username")
            config_new_relay(uname_relay, connection)
            usernames = list(connections.keys())
            objek = {
                "relay_username": my_username,
                "username_users": usernames
            }
            send_message(connection, objek)
            threading.Thread(target=handle_component_relay, args=(connection, my_username, ), daemon=True).start()
        elif(message.get("msg") == "Hello relay!"):
            objek = {"msg": "Hallo target"}
            send_message(connection, objek)
        

    

'''
    # print("Hello world!")
    # time.sleep(30)

    # relay_to_tracker.close()
    # del relay_to_tracker
'''