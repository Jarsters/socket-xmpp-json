import socket

class SocketClientRelay:
    def __init__(self, ip_target, port_target, relay=False, tipe=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        if(not ip_target):
            ip_target = self.getMyLocalAddress()[0]
        self.address_target = (ip_target, port_target)
        self.localAddress = self.getMyLocalAddress()
        print(f"Try to connecting.... {ip_target} - {port_target} ({tipe})")
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