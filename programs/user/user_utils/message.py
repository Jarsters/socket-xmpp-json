from user_utils.packet import send_message
from user_utils.get_time import get_timestamp

def send_message_to_relay(communicate, *args):
    '''
    *args = username, to, body/msg
    {
        stanza_name: "message",
        from: initiate_entity,
        to: receiver_entity,
        lang: "id", # Indonesian
        body: main_of_message,
        time_send: Timestamp
    }
    '''
    packet = {
        "stanza": "message",
        "from": args[0],
        "to": args[1],
        "lang": "id",
        "body": args[2],
        "time_send": get_timestamp()
    }
    print(f"PACKET MESSAGE {packet}")
    send_message(communicate, packet)

'''
1. register/login.
2. target, nulis username "fajar".
'''

'''
1. Penulisan pencarian protokol dulu.
2. Penulisan XML supaya bisa diganti ke JSON.
3. Ganti primary key jadi user_id, pada table yang menggunakan phone_numberr
'''