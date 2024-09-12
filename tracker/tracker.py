import socket
import json
import threading

from database.component import delete_component_by_id, delete_components, get_all, get_components, save_component_to_db
from utils.get_time import get_timestamp
from utils.packet import get_message, send_message

class SocketServer:
    def __init__(self, port=5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
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

delete_components()

def delete_component(message, id_component):
    print("Masuk ke delete component")
    print(message)
    delete_component_by_id(id_component, get_timestamp)
    print(f"Daftar koneksi dalam sistem {get_all()}")
    print("================================================")

def handleComponent(communicate:socket.socket, msg, id_component):
    error = False
    while not error:
        try:
            messages = get_message(communicate)
            for msg in messages:
                message = json.loads(msg)
                if(message.get("message") and message.get("message").lower() == "get components"):
                    send_message(communicate, get_components())
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
            # components.append(message)
        print(f"Daftar koneksi dalam sistem {get_all()}\r\n")
        feedback = get_components()
        print(f"Koneksi yang diberikan kepada komponen terkoneksi {feedback}")
        feedback = json.dumps(feedback)
        connection.send(feedback.encode())
        threading.Thread(target=handleComponent, args=(connection, message, id_component), daemon=True).start()
        print("================================================")