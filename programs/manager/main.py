import json
import threading
from string import printable
from random import randint
import ipaddress
import dotenv
import os

# from manager_utils.get_time import get_timestamp
from manager_utils.presence import get_presence_by_jid, init_presence, logout, send_presence_to_someone, set_my_bio
from manager_utils.roster import delete_roster, get_packet_subscribed_for_init_entity, get_packet_unsubscribed_for_init_entity, get_rosters, set_roster
from manager_utils.auth import handle_auth
from manager_utils.packet import get_message, get_message_client, get_message_relay, get_message_tracker, send_message
from manager_utils.import_abs_path import import_outside_utils

from database.dummy.init_data import socket_user
from database.sqlite.component import components as c_db, convert_components_db, delete_all_data_component_db, delete_components_db_by_id, save_component_to_db, get_relay_with_less_connection_db, update_total_connection
from database.sqlite.user import get_user_by_username, users as u_db , get_user_online
from database.sqlite.roster import get_roster_user, rosters as r_db

from socketClient import SocketClientManager
# from socketServer import SocketServerManager

try:
    module_socket = import_outside_utils("utils\\kelas\\", "socketServer.py")
except:
    print("Masuk except 1")
    module_socket = import_outside_utils("utils/kelas/", "socketServer.py")
try:
    module_get_time = import_outside_utils("utils\\utility\\", "get_time.py")
except:
    print("Masuk except 2")
    module_get_time = import_outside_utils("utils/utility/", "get_time.py")
SocketServer = module_socket.SocketServer
get_timestamp = module_get_time.get_timestamp

u_db.delete_data()
c_db.delete_data()
r_db.delete_data()

dotenv.load_dotenv()
IP_TRACKER = os.getenv("IP_TRACKER")

def connect_to_tracker():
    ask = input("Local (y/n)?")
    if(ask.lower() == 'y'):
        client_tracker = SocketClientManager(None, 5000, tipe="Tracker")
    else:
        client_tracker = SocketClientManager(IP_TRACKER, 5000, tipe="Tracker")
    # ct = Client Tracker
    ct = client_tracker.socket
    my_ip = client_tracker.localAddress
    ip_is_private = ipaddress.ip_address(my_ip[0]).is_private

    objek = {
        "ip_local": my_ip[0],
        "port": my_ip[1],
        "type": "manager",
        "is_private": ip_is_private
    }
    
    send_message(ct, objek)
    message = get_message_tracker(ct)
    print(message)
    return ct, my_ip

def get_all_components(components):
    return convert_components_db(components)

def lost_connection(reason, tipe, username_relay, username):
    print(f"Tipe yang terputus adalah {tipe}")
    print(f"Putus karena {reason}")
    if(tipe and tipe.lower() == "relay"):
        # Menghapus komponen relay dari database
        delete_components_db_by_id(c_db, tuple_condition=username_relay)
    if(username):
        # Menghapus koneksi dari user
        del socket_user[username]
        # Konfigurasi user yang logout atau mengalami error
        timestamp = get_timestamp()
        logout(socket_user, username, timestamp)
        # lockWhile.release()
    # print("Connection end...")

lockThread = threading.Lock()
# lockWhile = threading.Lock()

def handle_component(communicate, tipe, username_relay):  
    username = None
    error = False
    while not error:
        # if(tipe == "client"):
        #     lockWhile.acquire()
        try:
            messages = None
            if(tipe == "relay"):
                messages = get_message_relay(communicate)
            elif(tipe == "client"):
                messages = get_message_client(communicate)
            for msg in messages:
                with lockThread:
                    message = json.loads(msg)
                    # if(message.get("message") != "ecir"):
                    print(message)
                    if(message.get("error_msg")):
                        error = True
                        if(tipe == "relay"):
                            print(f"Komponen relay dengan username {username_relay} mengalami error....")
                            lost_connection(message.get("tipe"), tipe, username_relay, None)
                            break
                        elif(tipe == 'client'):
                            if(username):
                                print(f"Komponen client dengan username {username} mengalami error....")
                                # logout(socket_user, username, timestamp)
                                lost_connection("Menerima 'error_msg'", tipe, username_relay, username)
                            else:
                                print(f"Komponen client dengan username \"tanpa username\" mengalami error....")
                                error = True
                                # lockWhile.release()
                            break
                    elif(message.get("username")):
                        username = message.get("username")
                        socket_user[username] = communicate

                    # Ketika mau login dan belum online, kalo udah online minta get_relay_less_connection aja
                    if(tipe == "client" and message.get("type") == "auth" and not get_user_online(username)):
                        print("=========================================")
                        print("AUTH")
                        result = handle_auth(message, communicate, u_db, get_relay_with_less_connection_db)
                        if(not result):
                            username = None
                        print("=========================================")
                        # continue

                    # Ketika ada relay yang tiba-tiba error dan user mau relay dengan koneksi paling rendah terbaru
                    elif(tipe == "client" and message.get("type") == "get_relay_less_connection" and get_user_online(username)):
                        print("=========================================")
                        print("GET RELAY LESS CONNECTION")
                        relay_for_user = get_relay_with_less_connection_db()
                        objek = {"error": False, "msg": "Relay Less Connection", "code": 200, "component": relay_for_user}
                        print("=========================================")
                        send_message(communicate, objek)

                    # new connection in relay
                    elif(message.get("message") and message.get("message").lower() == "ncir" and tipe == "relay"):
                        print("=========================================")
                        print("NCIR")
                        print("Koneksi user terhubung dengan relay!")
                        username_relay = message.get("username_relay")
                        update_total_connection(username_relay, get_timestamp, 'NCIR')
                        print("=========================================")

                    # end connection in relay
                    elif(message.get("message") and message.get("message").lower() == "ecir" and tipe == "relay"):
                        # lockWhile.acquire()
                        print(message)
                        print("=========================================")
                        print("ECIR")
                        print("Koneksi user terputus dengan relay!")
                        username_relay = message.get("username_relay")
                        update_total_connection(username_relay, get_timestamp, 'ECIR')
                        print("=========================================")
                        # lockWhile.release()

                    # Mengelola yang berkaitan dengan roster
                    elif(message.get("stanza") and message.get("stanza").lower() == "iq" and message.get("namespace") and message.get("namespace").lower() == "roster"):
                        print("=========================================")
                        print("IQ, ROSTER")
                        # Mengelola user yang meminta rosternya
                        if(message.get("type") and message.get("type").lower()  == "get"):
                            print(f"Terjadi permintaan mendapatkan roster dari user {username}")
                            objek = get_rosters(username, message)
                            send_message(communicate, objek)
                        # Mengelola roster yang ingin menambahkan atau memperbarui roster item
                        elif(message.get("type") and message.get("type").lower()  == "set" and not message.get("subscription")):
                            print(f"Terjadi permintaan untuk menambahkan atau memperbarui roster item dari user {username}")
                            jid_target = message.get('query').get('item').get('jid')
                            objek = set_roster(username, message)
                            if(objek['type'] != "error"):
                                # Membuat presence bertipe "subscribed" untuk user pengirim
                                packet_presence_subscribed = get_packet_subscribed_for_init_entity(username, jid_target)
                                # Mengambil data roster item di dalam roster terbaru untuk user pengirim dari database
                                item = get_roster_user(username, jid_target)
                                print(f"ITEM {item}")
                                print(f"GET ITEM DB ROSTER: {get_roster_user(username, jid_target)}")
                                # Melengkapi packet presence bertipe "subscribed" dengan roster item terbaru
                                packet_presence_subscribed["item"] = item
                                # Mengirimkan packet lengkap presence bertipe "subscribed" kepada user pengirim
                                send_message(communicate, packet_presence_subscribed)
                                if(item.get("subscription") == "both" and get_user_online(jid_target)):
                                    packet_presence_subscribed_for_roster_item = get_packet_subscribed_for_init_entity(username, jid_target)    
                                    item_for_roster_item = get_roster_user(jid_target, username)
                                    packet_presence_subscribed_for_roster_item["item"] = item_for_roster_item
                                    send_message(socket_user[jid_target], packet_presence_subscribed_for_roster_item)
                                # Mengambil data presence terbaru dari roster item yang dikirimkan oleh user pengirim
                                subscribed_entity_presence = get_presence_by_jid(jid_target)
                                subscribed_entity_presence['to'] = username
                                # Mengirimkan packet presence terbaru roster item kepada user pengirim
                                send_message(communicate, subscribed_entity_presence)
                            else:
                                print(f"Terjadi error saat user {username} melakukan permintaan menambahkan atau mengubah roster item")
                            # Mengirimkan hasil dari set roster item atau update roster item kepada user pengirim
                            send_message(communicate, objek)
                        # Menghapus roster item dari roster user pengirim    
                        elif(message.get("type") and message.get("type").lower() == "set" and message.get("subscription") and message.get("subscription").lower() == "remove"):
                            print(f"Terjadi permintaan menghapus roster item dari user {username}")
                            jid_target = message.get('query').get('item').get('jid')
                            objek = delete_roster(username, message) # delete_roster_user
                            if(objek['type'] != 'error'):
                                # Membuat presence bertipe "unsubscribed" untuk user pengirim
                                packet_presence_unsubscribed = get_packet_unsubscribed_for_init_entity(username, jid_target)
                                # Mengirim packet presence kepada user pengirim
                                send_message(communicate, packet_presence_unsubscribed)
                            else:
                                print(f"Terjadi error saat user {username} melakukan permintaan menghapus roster item")
                            # Mengirimkan hasil dari menghapus roster item kepada user pengirim
                            send_message(communicate, objek)
                        print("=========================================")

                    # Mengelola yang berkaitan dengan presence
                    elif(message.get("stanza") and message.get("stanza").lower() == "presence"):
                        print("=========================================")
                        print("PRESENCE")
                        # Mengelola init presence
                        if(not message.get('type') and not message.get("bio") and not message.get("to")):
                            print(f"Terjadi permintaan init presence dari user dengan username {username}")
                            timestamp = get_timestamp()
                            init_presence(socket_user, username, timestamp)
                        # Mengelola ketika user memperbarui bio-nya
                        elif(message.get('bio')):
                            print(f"Terjadi permintaan perubahan bio dari user dengan username {username}")
                            timestamp = get_timestamp()
                            set_my_bio(socket_user, username, message, timestamp)
                        # Mengelola ketika user membuat permintaan directed presence
                        elif(message.get('to')):
                            jid_target = message.get('to')
                            print(f"Terjadi permintaan directed presence yang dilakukan oleh user {username} dengan target user adalah {jid_target}")
                            if(not get_user_by_username(jid_target)):
                                print(f"Terjadi error saat permintaan directed presence karena target user {jid_target} tidak terdaftar di dalam sistem")
                                objek_presence_error = {'stanza': 'presence', 'type': 'error', 'to': username, 'target': jid_target}
                                send_message(communicate, objek_presence_error)
                                continue
                            # Kirim status presence init_entity ke target_entity jika target_entity online
                            if(get_user_online(jid_target)):
                                print(f"Mengirimkan directed presence kepada target user {jid_target} karena target user sedang online")
                                init_entity_presence = get_presence_by_jid(username)
                                init_entity_presence['directed_entity'] = True
                                send_presence_to_someone(jid_target, socket_user, init_entity_presence)
                            # Ambil status dari target_entity dan kirim ke init_entity
                            target_entity_presence = get_presence_by_jid(jid_target)
                            target_entity_presence['directed_entity'] = True
                            print(target_entity_presence)
                            send_presence_to_someone(username, socket_user, target_entity_presence)
                        # Mengelola ketika user membuat permintaan presence tipe "unavailable" atau logout
                        elif(message.get('type') == 'unavailable'):
                            print(f"Terjadi permintaan presence bertipe 'unavailable' dari user {username}")
                            # timestamp = get_timestamp()
                            # logout(socket_user, username, timestamp)
                            lost_connection("Memberikan presence tipe unavailable", tipe, username_relay, username)
                            error = True
                        print("=========================================")
                    # if(tipe == "client"):
                    #     lockWhile.release()
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

ct, my_address = connect_to_tracker()

# m = SocketServerManager(my_address[1])
m = SocketServer(my_address[1])
manager = m.socket

print("Manager listening...")

# Fungsi untuk menghasilkan username untuk relay yang baru terkoneksi sepanjang 10 karakter
def generate_username(w):
    result = ""
    length_w = len(w) - 1
    for _ in range(10):
        result += w[randint(0, length_w)]
    return result

# Fungsi validasi untuk username relay, untuk memastikan bahwa username akan unik
def random_username_for_relay(c_db, data):
    ## Jika mau diimplementasiin logic, 
    ## jika ip address dan port yang sama sudah terdaftar maka tidak boleh menjadi relay
    # Mengecek validitas bahwa ip address dan port belum terdaftar sebagai relay
    check_validity_ip_and_port = not c_db.get_all_with_limit(1, ['ip_address', 'port'], (data.get("ip_local"), data.get("port")), ['AND'])
    if(not check_validity_ip_and_port):
        return False
    # printable, digits, dan punctuation dari library string
    letter = printable
    while True:
        username_relay = generate_username(letter)
        # Mengecek validitas bahwa username akan unik
        check_validity_username_of_relay = not c_db.get_all_with_limit(1, ['component_id'], (username_relay,))
        if(check_validity_username_of_relay):
            return username_relay

# Konfigurasi relay yang baru saja melakukan koneksi
def config_new_relay(msg, uname):
    msg["username"] = uname
    msg["connection"] = 0
    print(f"CONFIG RELAY: {msg}")
    # Menyimpan relay baru ke dalam database
    save_component_to_db(list(msg.values()), get_timestamp)

# Fungsionalitas untuk menerima setiap koneksi yang baru terhubung dengan manager
while True:
    try:
        connection, address = manager.accept()
        # Fungsionalitas penerimaan pesan
        messages = get_message(connection)
        for msg in messages:
            message = json.loads(msg)
            print("===================================================")
            print(message)
            username_relay = None
            # Metode yang dilakukan jika koneksi yang baru bertipe relay
            if(message.get("type").lower() == "relay"):
                print("KONFIGURASI RELAY")
                # print(f'RELAY MESSAGE: {msg}')
                username_relay = random_username_for_relay(c_db, message)
                ### jika ip address dan port yang sama sudah terdaftar maka tidak boleh menjadi relay
                if(not username_relay):
                    obj_error = {
                        "error_msg": True,
                        "msg": "IP address dan port sudah terdaftar",
                        "error-type": "bad request"
                    }
                    send_message(connection, obj_error)
                    continue
                # Konfigurasi awal relay
                config_new_relay(message, username_relay)
                # Mengambil semua data komponen yang terkoneksi dengan manager
                c = get_all_components(c_db.get_all())
                print(f"Komponen yang diberikan kepada relay {username_relay} adalah:\r\n {c}")
                # Membuat packet yang akan dikirimkan kepada relay yang baru terkoneksi
                objek = {
                    "components": c,
                    "username": username_relay
                }
                # Mengirimkan semua data komponen kepada relay yang baru terkoneksi
                # print(f"KONFIGURASI RELAY {objek}")
                send_message(connection, objek)
            # Mendapatkan tipe dari komponen yang terhubung
            tipe = message.get('type')
            # Membuat layanan eksklusif untuk menerima packet pesan dari komponen terkoneksi
            # lockThread = threading.Lock()
            threading.Thread(target=handle_component, args=(connection, tipe, username_relay), daemon=True).start()
            print("===================================================")
    except KeyboardInterrupt as e:
        print("Masuk keyboard interrupt")
        delete_all_data_component_db()
        break
    except Exception as e:
        print("Masuk exception")
        print(e)
        delete_all_data_component_db()
        break