import json
import re

msg = ""
msg_manager = ""
msg_relay = ""

def verify(message):
    pattern = '{.+}'
    if(re.findall(pattern, message)):
        return True
    return False

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

def get_message_tracker(communicate):
    message = None
    try:
        message = communicate.recv(65536)
        message = message.decode()
    except WindowsError as e:
        print("masuk error winerror")
        print(e)
        message = json.dumps({"error_msg": True, "tipe": "winerror"})
    except Exception as e:
        print("masuk error get message relay")
        print(e)
        message = json.dumps({"error_msg": True})
    return json.loads(message)

# def get_message(communicate):
#     global msg
#     message = communicate.recv(65536)
#     message = message.decode()
#     items = message.split('\x80\x81\x82')
#     for i in items:
#         if(msg):
#             i = msg + i
#             msg = ""
#             yield i
#         elif(verify(i)):
#                 yield i
#         else:
#             msg = i
    # return json.loads(message)

def get_message_manager(communicate):
    global msg_manager
    message = ""
    message = communicate.recv(65536)
    message = message.decode()
    items = message.split('\x80\x81\x82')
    for i in items:
        if(msg_manager):
            i = msg_manager + i
            msg_manager = ""
            yield i
        elif(verify(i)):
                yield i
        else:
            msg_manager = i

def get_message_relay(communicate):
    global msg_relay
    message = ""
    message = communicate.recv(65536)
    message = message.decode()
    items = message.split('\x80\x81\x82')
    for i in items:
        if(msg_relay):
            i = msg_relay + i
            msg_relay = ""
            yield i
        elif(verify(i)):
                yield i
        else:
            msg_relay = i

def send_message(communicate, msg):
    msg = json.dumps(msg) + '\x80\x81\x82'
    msg = msg.encode()
    communicate.send(msg)