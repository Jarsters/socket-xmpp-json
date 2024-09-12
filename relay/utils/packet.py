import json
import re
import time

msg = ""
msg_manager = ""
msg_user = ""
msg_tracker = ""
msg_relay = ""

def verify(message):
    pattern = '{.+}'
    if(re.findall(pattern, message)):
        return True
    return False

def get_message_manager(communicate):
    try:
        global msg_manager
        message = ""
        message = communicate.recv(65536)
        message = message.decode()
        items = message.split('\x80\x81\x82')
        print(f"Pesan dari manager: {items}")
        if(len(items) == 1 and not items[0]):
            yield '{"error_msg": true, "tipe": "socket peer is closed"}'
        else:
            for i in items:
                if(msg_manager):
                    i = msg_manager + i
                    msg_manager = ""
                    yield i
                elif(verify(i)):
                        yield i
                else:
                    msg_manager = i
    except Exception as e:
        yield '{"error_msg": true, "tipe": "socket peer is closed"}'

def get_message_user(communicate):
    global msg_user
    message = ""
    message = communicate.recv(65536)
    message = message.decode()
    items = message.split('\x80\x81\x82')
    if(len(items) == 1 and not items[0]):
        yield '{"error_msg": true, "tipe": "socket peer is closed"}'
    else:
        for i in items:
            if(msg_user):
                i = msg_user + i
                msg_user = ""
                yield i
            elif(verify(i)):
                    yield i
            else:
                msg_user = i

def get_message_tracker(communicate):
    message = None
    try:
        message = communicate.recv(65536)
        message = message.decode()
    # except WindowsError as e:
    #     print("masuk error winerror")
    #     print(e)
    #     message = json.dumps({"error_msg": True, "tipe": "winerror"})
    except Exception as e:
        print("masuk error get message relay")
        print(e)
        message = json.dumps({"error_msg": True})
        return '{"error_msg": true, "tipe": "socket peer is closed"}'
    return json.loads(message)

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
            yield '{"error_msg": true, "tipe": "socket peer relay is closed"}'
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
    except Exception as e:
        # print(e)
        yield '{"error_msg": true, "tipe": "exception"}'
    # except WindowsError as e:
    #     yield '{"error_msg": true, "tipe": "winerror"}'

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


# def get_message(communicate):
#     message = None
#     try:
#         message = communicate.recv(65536)
#         message = message.decode()
#     except WindowsError as e:
#         print("masuk error winerror")
#         print(e)
#         message = json.dumps({"error_msg": True, "tipe": "winerror"})
#     except Exception as e:
#         print("masuk error get message relay")
#         print(e)
#         message = json.dumps({"error_msg": True})
#     return json.loads(message)

# def get_message_manager(communicate):
#     message = communicate.recv(65536)
#     message = message.decode()
#     message = message.replace('\x80\x81\x82', '')
#     return json.loads(message)

def send_message(communicate, msg):
    try:
        msg = json.dumps(msg)
    except:
        msg = '{"hello": "aku"}'
    msg += '\x80\x81\x82'
    msg = msg.encode()
    communicate.send(msg)