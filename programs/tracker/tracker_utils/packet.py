import json
import re

msg = ""

def verify(message):
    pattern = '{.+}'
    if(re.findall(pattern, message)):
        return True
    return False

def get_message(communicate):
    global msg
    message = ""
    message = communicate.recv(65536)
    message = message.decode()
    items = message.split('\x80\x81\x82')
    if(len(items) == 1 and not items[0]):
        yield '{"error_msg": true, "tipe": "socket peer is closed"}'
    else:
        for i in items:
            if(msg):
                i = msg + i
                msg = ""
                yield i
            elif(verify(i)):
                    yield i
            else:
                msg = i

def send_message(communicate, msg):
    msg = json.dumps(msg).encode()
    communicate.send(msg)