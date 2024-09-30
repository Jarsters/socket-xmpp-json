from utils.packet import send_message

def send_message_to_relay(communicate, *args):
    '''
    *args = username, to, body/msg
    {
        stanza_name: "message",
        from: initiate_entity,
        to: receiver_entity,
        lang: "id", # Indonesian
        body: main_of_message
    }
    '''
    packet = {
        "stanza": "message",
        "from": args[0],
        "to": args[1],
        "lang": "id",
        "body": args[2]
    }
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