import json
import re

msg_relay = ""
msg_client = ""
msg_tracker = ""
msg = ""

def verify(message):
    pattern = '{.+}'
    if(re.findall(pattern, message)):
        return True
    return False

def get_message_relay(communicate):
    global msg_relay
    items = None
    try:
        message = ""
        message = communicate.recv(65536)
        message = message.decode()
        # print(f"INI MESSAGE RELAY: {message}")
        items = message.split('\x80\x81\x82')
        if(len(items) == 1 and not items[0]):
            yield '{"error_msg": true, "tipe": "socket peer is closed"}'
        else:
            for i in items:
                if(msg_relay):
                    i = msg_relay + i
                    msg_relay = ""
                    yield i
                elif(verify(i)):
                        yield i
                else:
                    msg_relay = i
    # except WindowsError as e:
    #     items = ['{"error_msg": true, "tipe": "winerror"}']
    except KeyboardInterrupt as e:
        items = ['{"error_msg": true, "tipe": "keyboard interrupt"}']
    except Exception as e:
        items = ['{"error_msg": true, "tipe": "exception"}']


def get_message_client(communicate):
    global msg_client
    message = ""
    message = communicate.recv(65536)
    message = message.decode()
    items = message.split('\x80\x81\x82')
    # print(f'INI MESSAGE CLIENT: {message}')
    if(len(items) == 1 and not items[0]):
            yield '{"error_msg": true, "tipe": "socket peer is closed"}'
    else:
        for i in items:
            if(msg_client):
                i = msg_client + i
                msg_client = ""
                yield i
            elif(verify(i)):
                    yield i
            else:
                msg_client = i

def get_message_tracker(communicate):
    msg_tracker = None
    try:
        msg_tracker = communicate.recv(65536)
        msg_tracker = msg_tracker.decode()
    # except WindowsError as e:
    #     print("masuk error winerror")
    #     print(e)
    #     msg_tracker = json.dumps({"error_msg": True, "tipe": "winerror"})
    except Exception as e:
        print("masuk error get message")
        print(e)
        msg_tracker = json.dumps({"error_msg": True})
    return json.loads(msg_tracker)

def get_message(communicate):
    global msg
    message = ""
    message = communicate.recv(65536)
    message = message.decode()
    items = message.split('\x80\x81\x82')
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
    msg = json.dumps(msg) + '\x80\x81\x82'
    msg = msg.encode()
    print("Pesan dikirimkan")
    communicate.send(msg)