'''
FORMAT PRESENCE
{
    stanza: 'presence',
    from: init_entity_presence,
    to: receive_entity_presence,
    type: None or unavaiable
}
'''

'''
if(not message.get('type') and not message.get("bio")):
    init_presence(rosters, users, socket_user, username)
elif(message.get('bio')):
    set_my_bio(rosters, users, socket_user, username, message)
elif(message.get('to')):
    jid_target = message.get('to')
    # Kirim status presence init_entity ke target_entity
    init_entity_presence = get_presence_by_jid(username, users)
    send_presence_to_someone(jid_target, socket_user, init_entity_presence)
    # Ambil status dari target_entity dan kirim ke init_entity
    target_entity_presence = get_presence_by_jid(jid_target, users)
    send_presence_to_someone(username, socket_user, target_entity_presence)
elif(message.get('type') == 'unavailable'):
    logout(rosters, users, socket_user, username)
    break
====
    INI DILAKUIN PAS BARU LOGIN & SETELAH MINTA ROSTER
{
	'stanza': 'presence'
}
===
{
	'stanza': 'presence',
	'from': init_entity,
	'bio': 'halo ini bio aku'
}
===
{
	'stanza': 'presence',
	'from': init_entity,
	'to': jid_target
}
===
{
	'stanza': presence,
    'from': init_entity,
	'type': 'unavailable'
}
'''



'''
DAFTAR FUNGSI YANG AKAN DIIMPLEMENTASIKAN
    1. MELIHAT STATUS ONLINE BERDASARKAN USERNAME. (DIAMBIL DARI TABLE USERS) -> DUMMY DB
    2. MENGUBAH BIO/STATUS.
    3. MENGUBAH STATUS DARI ONLINE KE OFFLINE.
'''

from utils.packet import send_message
from utils.get_time import get_timestamp

def helper_error(msg, error_type, stanza_error):
    '''
    {
        stanza: 'presence',
        from: init_entity_jid,
        bio: something
    }
    '''
    msg["type"] = "error"
    tmp = msg["from"]
    del msg["from"]
    msg["to"] = tmp
    del tmp
    msg["error"] = {}
    msg["error"]["type"] = error_type
    msg["error"]["stanza_error"] = stanza_error
    msg["error"]["stanza_error_ns"] = "xmpp-stanzas"
    return msg

def send_to_roster_subscription_from(roster, socket_user, objek_presence, users, init=True):
    '''
    objek_presence = {
        "from": init_entity_jid,
        "type": THE TYPE
    }
    tinggal tambahin "to" dan kirim ke subscriptionnya "to"
    '''
    # print('90909009')
    # print(roster)
    for r in roster.values():
        if(r.get("subscription") == "from"):
            objek_presence["to"] = r.get("jid")
            try:
                send_message(socket_user[r.get('jid')], objek_presence)
            except Exception as e:
                continue
        elif(r.get("subscription") == "both"):
            objek_presence["to"] = r.get("jid")
            try:
                send_message(socket_user[r.get('jid')], objek_presence)
                if(init):
                    print('INIT MASUK KE SINI')
                    presence_target = get_presence_by_jid(r.get('jid'), users)
                    send_presence_to_someone(objek_presence.get('from'), socket_user, presence_target)
            except Exception as e:
                continue

def get_presence_entity_subscription_to(roster, socket_user, username, users):
    socket = socket_user[username]
    for r in roster.values():
        if(r.get("subscription") == "to" or r.get("subscription") == "both"):
            objek_presence = get_presence_by_jid(r.get('jid'), users)
            try:
                send_message(socket, objek_presence)
            except Exception as e:
                continue

def send_presence_to_someone(jid_target, socket_user, objek_presence):
    objek_presence["to"] = jid_target
    print(objek_presence)
    send_message(socket_user[jid_target], objek_presence)

# ========== CRUD ada dibawah ini

def init_presence(rosters, users, socket_user, username):
    users[username]['online'] = True
    users[username]['updated_at'] = get_timestamp()
    roster = rosters.get(username)
    print(roster)
    print(username)
    if(not roster):
        return
    # objek_presence = {
    #     "from": username,
    # }
    objek_presence = get_presence_by_jid(username, users)
    send_to_roster_subscription_from(roster, socket_user, objek_presence, users)
    get_presence_entity_subscription_to(roster, socket_user, username, users)

def get_presence_by_jid(jid_target, users):
    '''
    result tmp
    {
        'stanza': 'presence',
        'from': jid_target,
        'username': jid_target,
        "bio": "Feel happy using this application! ;D",
        "online": True,
        "updated_at": timestamp,
    }
    '''
    if(not users.get(jid_target)):
        return False
    print("INI DISINI")
    tmp = users[jid_target].copy()
    del tmp["password"]
    del tmp["created_at"]
    tmp['stanza'] = 'presence'
    tmp['from'] = jid_target
    print(tmp)
    return tmp

def set_my_bio(rosters, users, socket_user, username, msg):
    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(username != msg.get("from")):
        return helper_error(msg, "auth", "forbidden")
    updated_at = get_timestamp()
    users[username]['bio'] = msg.get('bio')
    users[username]['updated_at'] = updated_at
    my_presence = get_presence_by_jid(username, users)
    roster = rosters.get(username)
    print(roster)
    if(not roster):
        return
    send_to_roster_subscription_from(roster, socket_user, my_presence, users, False)

def logout(rosters, users, socket_user, username):
    users[username]['online'] = False
    users[username]['updated_at'] = get_timestamp()
    roster = rosters.get(username)
    if(not roster):
        return
    objek_presence = {
        "stanza": "presence",
        "from": username,
        "type": "unavailable"
    }
    send_to_roster_subscription_from(roster, socket_user, objek_presence, users)