import socket
import json
import threading

from utils.packet import get_message, send_message

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


'''
    {
        "ip_address"
        "port"
        "type"
        "created_at"
    }
'''

components = [] # [{}] => list of object

# def get_message(communicate):
#     message = communicate.recv(1024)
#     message = message.decode()
#     return json.loads(message)

def delete_component(message):
    ip_local = message.get("ip_local")
    port = message.get("port")
    index = 0
    for c in components:
        if(c.get("ip_local") == ip_local and c.get("port") == port):
            break
        index += 1
    components.pop(index)

def handleComponent(communicate, msg):
    while True:
        try:
            messages = get_message(communicate)
            for msg in messages:
                message = json.loads(msg)
                if(message.get("message").lower() == "get components"):
                    send_message(communicate, components)
                    # communicate.
        except ConnectionAbortedError:
            print("Connection end...")
            # delete_component(msg)
            break
        except ConnectionRefusedError:
            print("Connection end...")
            # delete_component(msg)
            break
        except ConnectionError:
            print("Connection end...")
            # delete_component(msg)
            break
        except Exception as e:
            print(e)
            print("Connection end...")
            # delete_component(msg)
            break


s = SocketServer()
server = s.socket

while True:
    connection, address = server.accept()
    messages = get_message(connection)
    for message in messages:
        message = json.loads(message)
        print(message)
        # ip_is_private = ipaddress.ip_address(message.get("ip_local")).is_private
        ip_is_private = message.get("is_private")
        tipe = message.get('type').lower()
        if(not ip_is_private or tipe == 'manager' or tipe == 'relay'):
            components.append(message)
        feedback = json.dumps(components)
        connection.send(feedback.encode())
        print(components)
        threading.Thread(target=handleComponent, args=(connection, message), daemon=True).start()

# server.close()
# del server

# print(components)