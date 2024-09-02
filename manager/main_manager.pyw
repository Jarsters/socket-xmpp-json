import socket
import json
import threading
from string import printable, digits, punctuation
from random import randint
import time

from utils.presence import get_presence_by_jid, init_presence, logout, send_presence_to_someone, set_my_bio
from utils.roster import delete_roster, get_packet_subscribed_for_init_entity, get_packet_unsubscribed_for_init_entity, get_roster, set_roster
from utils.relay_less_connection import get_relay_with_less_connection
from utils.auth import handle_auth, helper_registering_user
from utils.packet import get_message, get_message_client, get_message_relay, get_message_tracker, send_message

from database.dummy.init_data import components, users, rosters, socket_user

# from database.sqlite.component import components as c_db, delete_all_data_component_db, delete_components_db_by_id, save_component_to_db
 
# === Inititate Variable
# components = [] # List of object = [{}] -> Isinya kumpulan relay
'''
    objek relay: {
        "username":,
        "ip":,
        "port":,
        ....
    }
'''
# ===


class SocketClient:
    def __init__(self, ip_target, port_target):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if(not ip_target):
            ip_target = self.getMyLocalAddress()[0]
        self.address_target = (ip_target, port_target)
        self.localAddress = self.getMyLocalAddress()
        print("Try to connecting....")
        self.connectToTarget()
        print("Connected")
    def connectToTarget(self):
        try: 
            self.socket.connect(self.address_target)
        except Exception as e:
            print(e)
            print("Error when connecting....")
            print("Quit program")
            self.socket.close()
            exit()
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

    objek = {
        "ip_local": my_ip[0],
        "port": my_ip[1],
        "type": "manager"
    }

    # stringObjek = json.dumps(objek)

    # ct.send(stringObjek.encode())
    send_message(ct, objek)
    message = get_message_tracker(ct)
    # message = json.loads(message)
    print(message)

    ct.close()
    return my_ip

def get_all_components(components):
    # print(f"===GAC===")
    # datas_c = c_db.get_all()
    # print(datas_c)
    # print(list(components.values()))
    # print(f"===END GAC===")
    return list(components.values())
    # return convert_components_db(datas_c)

def lost_connection(reason, tipe, username_relay, username):
    global components
    print(f"Tipe yang terputus adalah {tipe}")
    print(f"Putus karena {reason}")
    if(tipe and tipe.lower() == "relay"):
        if(components.get(username_relay)):
            del components[username_relay]
        # delete_components_db_by_id(c_db, tuple_condition=username_relay)
        print(components)
    if(username):
        del socket_user[username]
        logout(rosters, users, socket_user, username)
    print("Connection end...")

def handle_component(communicate, tipe, username_relay):  
    global components, users
    username = None
    error = False
    while True:
        try:
            if(error):
                del components[username_relay]
                # delete_components_db_by_id(c_db, tuple_condition=username_relay)
                break
            messages = None
            if(tipe == "relay"):
                messages = get_message_relay(communicate)
            elif(tipe == "client"):
                messages = get_message_client(communicate)
            for msg in messages:
                print(msg)
                message = json.loads(msg)
                if(message.get("error_msg")):
                    error = True
                    print(f"Masuk msg error: {message.get('tipe')}")
                if(message.get("username")):
                    username = message.get("username")
                    socket_user[username] = communicate

                # Ketika mau login atau ketika tiba-tiba user mengalami error
                if(message.get("type") == "auth" or (users.get(username) and not users.get(username)['online'])):
                    print("AUTH")
                    handle_auth(message, users, components, communicate)
                    continue      
                
                elif(message.get("type") == "get_relay_less_connection" and users.get(username) and users[username].get("online")):
                    print("GET RELAY LESS CONNECTION")
                    relay_for_user = get_relay_with_less_connection(components)
                    objek = {"error": False, "msg": "Relay Less Connection", "code": 200, "component": relay_for_user}
                    send_message(communicate, objek)

                # elif(message.get("message") and message.get("message").lower() == "get components"):
                #     print("GET COMPONENTS")
                #     com = get_all_components(components)
                #     # print(components)
                #     send_message(communicate, com)
                #     continue

                elif(message.get("message") and message.get("message").lower() == "ncir"): # new connection in relay
                    print("Koneksi user terhubung dengan relay!")
                    username_relay = message.get("username_relay")
                    components[username_relay]["connection"] = components[username_relay]["connection"] + 1

                elif(message.get("message") and message.get("message").lower() == "ecir"): # end connection in relay
                    print("Koneksi user terputus dengan relay!")
                    username_relay = message.get("username_relay")
                    components[username_relay]["connection"] = components[username_relay]["connection"] - 1

                elif(message.get("stanza") and message.get("stanza").lower() == "iq" and message.get("namespace") and message.get("namespace").lower() == "roster"):
                    # print("IQ, ROSTER")
                    # print(message)
                    # print(username)
                    # print('==========')
                    if(message.get("type") and message.get("type").lower()  == "get"):
                        objek = get_roster(username, rosters, message)
                        send_message(communicate, objek)
                    elif(message.get("type") and message.get("type").lower()  == "set" and not message.get("subscription")):
                        jid_target = message.get('query').get('item').get('jid')
                        objek = set_roster(username, rosters, message, users)
                        if(objek['type'] != "error"):
                            # print("=== Masuk Subscribed ===")
                            packet_presence_subscribed = get_packet_subscribed_for_init_entity(username, jid_target)
                            item = rosters[username][jid_target]
                            packet_presence_subscribed["item"] = item
                            # print(f"{packet_presence_subscribed}\n=== Akhir Subscribed ===")
                            send_message(communicate, packet_presence_subscribed)
                            subscribed_entity_presence = get_presence_by_jid(jid_target, users)
                            subscribed_entity_presence['to'] = username
                            send_message(communicate, subscribed_entity_presence)
                            # print(subscribed_entity_presence)
                            # time.sleep(0.2)
                            # send_presence_to_someone(username, socket_user, subscribed_entity_presence)
                            # pass
                        send_message(communicate, objek)
                    elif(message.get("type") and message.get("type").lower() == "set" and message.get("subscription") and message.get("subscription").lower() == "remove"):
                        jid_target = message.get('query').get('item').get('jid')
                        objek = delete_roster(username, rosters, message, users)
                        if(objek['type'] != 'error'):
                            packet_presence_unsubscribed = get_packet_unsubscribed_for_init_entity(username, jid_target)
                            send_message(communicate, packet_presence_unsubscribed)
                        send_message(communicate, objek)

                elif(message.get("stanza") and message.get("stanza").lower() == "presence"):
                    if(not message.get('type') and not message.get("bio") and not message.get("to")):
                        init_presence(rosters, users, socket_user, username)
                    elif(message.get('bio')):
                        set_my_bio(rosters, users, socket_user, username, message)
                    elif(message.get('to')):
                        jid_target = message.get('to')
                        if(not users.get(jid_target)):
                            objek_presence_error = {'stanza': 'presence', 'type': 'error', 'to': username, 'target': jid_target}
                            send_message(communicate, objek_presence_error)
                            continue
                        # Kirim status presence init_entity ke target_entity
                        if(users.get(jid_target).get("online")):
                            init_entity_presence = get_presence_by_jid(username, users)
                            init_entity_presence['directed_entity'] = True
                            send_presence_to_someone(jid_target, socket_user, init_entity_presence)
                        # Ambil status dari target_entity dan kirim ke init_entity
                        target_entity_presence = get_presence_by_jid(jid_target, users)
                        target_entity_presence['directed_entity'] = True
                        print(target_entity_presence)
                        send_presence_to_someone(username, socket_user, target_entity_presence)
                    elif(message.get('type') == 'unavailable'):
                        logout(rosters, users, socket_user, username)
                        break

        except ConnectionAbortedError as e:
            lost_connection(e, tipe, username_relay, username)
            break
        except ConnectionRefusedError as e:
            lost_connection(e, tipe, username_relay, username)
            break
        except ConnectionError as e:
            lost_connection(e, tipe, username_relay, username)
            break
        except Exception as e:
            lost_connection(e, tipe, username_relay, username)
            break

my_address = connect_to_tracker()

m = SocketServer(my_address[1])
manager = m.socket

print("Manager listening...")

# ====== BAGIAN RELAY
collections_username = set()

def generate_username(w):
    result = ""
    length_w = len(w) - 1
    for i in range(10):
        result += w[randint(0, length_w)]
    return result

def random_username_for_relay(collections_username):
    # printable, digits, dan punctuation dari library string
    letter = printable + digits + punctuation
    while True:
        username_relay = generate_username(letter)
        bool1 = not (username_relay in collections_username)
        # bool2 = not c_db.get_all(['component_id'], (username_relay,))
        if(bool1):
            collections_username.add(username_relay)
            return username_relay

def config_new_relay(components, msg, uname):
    msg["username"] = uname
    msg["connection"] = 0
    print(f"CONFIG RELAY: {msg}")
    components[uname] = msg
    # save_component_to_db(list(msg.values()))
# ======

while True:
    try:
        connection, address = manager.accept()
        messages = get_message(connection)
        for msg in messages:
            message = json.loads(msg)
            username_relay = None
            if(message.get("type").lower() == "relay"):
                username_relay = random_username_for_relay(collections_username)
                config_new_relay(components, message, username_relay)
                # c = list(components.values())
                c = get_all_components(components)
                objek = {
                    "components": c,
                    "username": username_relay
                }
                # print(f"OBJ R: {objek}")
                send_message(connection, objek)
            # ip_is_private = message.get("is_private")
            tipe = message.get('type')
            # print(message)
            threading.Thread(target=handle_component, args=(connection, tipe, username_relay), daemon=True).start()
            # print(components)
    except Exception as e:
        # delete_all_data_component_db()
        print("----End Manager ----")
        break