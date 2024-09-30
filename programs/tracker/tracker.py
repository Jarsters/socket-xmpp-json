import socket
import json
import threading

from tracker_utils.import_abs_path import import_outside_utils
from tracker_utils.packet import get_message, send_message

from database.component import delete_component_by_id, delete_components, get_all, get_components, save_component_to_db
# from tracker_utils.get_time import get_timestamp
try:
    module_socket = import_outside_utils("utils\\kelas\\", "socketServer.py")
except:
    module_socket = import_outside_utils("utils/kelas/", "socketServer.py")
try:
    module_get_time = import_outside_utils("utils\\utility\\", "get_time.py")
except:
    module_get_time = import_outside_utils("utils/utility/", "get_time.py")
SocketServer = module_socket.SocketServer
get_timestamp = module_get_time.get_timestamp

delete_components()

def delete_component(message, id_component):
    print(message)
    delete_component_by_id(id_component, get_timestamp)
    print(f"Daftar koneksi dalam sistem {get_all()}")
    print("================================================")

def send_connected_components_to_component(communicate):
    # print(f"Koneksi yang diberikan kepada komponen terkoneksi")
    print(f"Tracker memberikan komponen yang terkoneksi dengannya kepada komponen yang baru koneksi")
    send_message(communicate, get_components())

def handleComponent(communicate:socket.socket, msg, id_component):
    error = False
    while not error:
        try:
            messages = get_message(communicate)
            for msg in messages:
                message = json.loads(msg)
                if(message.get("message") and message.get("message").lower() == "get components"):
                    # send_message(communicate, get_components())
                    send_connected_components_to_component(communicate)
                elif(message.get("error_msg")):
                    print(f"Terjadi putus koneksi dengan id_component {id_component}")
                    delete_component(msg, id_component)
                    error = True
        except ConnectionAbortedError:
            print("Connection end 1 ...")
            delete_component(msg, id_component)
            break
        except ConnectionRefusedError:
            print("Connection end 2 ...")
            delete_component(msg, id_component)
            break
        except ConnectionError:
            print("Connection end 3 ...")
            delete_component(msg, id_component)
            break
        except Exception as e:
            print(e)
            print("Connection end 4 ...")
            delete_component(msg, id_component)
            break

s = SocketServer()
server = s.socket
print(f"Tracker listening .... on ({s.localIP} - 5000)")
print(f"Daftar koneksi dalam sistem {get_components()}")
print("================================================")

while True:
    connection, address = server.accept()
    messages = get_message(connection)
    id_component = None
    for message in messages:
        message = json.loads(message)
        print(f"Koneksi baru: {message}\r\n")
        ip_is_private = message.get("is_private")
        tipe = message.get('type').lower()
        if(not ip_is_private or tipe == 'manager' or tipe == 'relay'):
            data = list(message.values())
            id_component = save_component_to_db(data, get_timestamp)
        print(f"Daftar koneksi dalam sistem {get_all()}\r\n")
        send_connected_components_to_component(connection)
        threading.Thread(target=handleComponent, args=(connection, message, id_component), daemon=True).start()
        print("================================================")