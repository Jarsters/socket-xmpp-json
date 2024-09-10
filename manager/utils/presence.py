from database.sqlite.roster import get_rosters_user
from utils.packet import send_message
from utils.get_time import get_timestamp

from database.sqlite.user import get_presence_user, update_bio, update_status_online

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

# Fungsionalitas mengirimkan packet untuk rostem item dari user yang memiliki subscription 'from' atau 'both'
def send_to_roster_subscription_from(roster, socket_user, objek_presence, init=True):
    print(f"ROSTER FROM AND BOTH IN DB: {roster}")
    for r in roster:
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
                    presence_target = get_presence_by_jid(r.get('jid'))
                    send_presence_to_someone(objek_presence.get('from'), socket_user, presence_target)
            except Exception as e:
                print(e)
                continue

# Fungsionalitas mengirimkan packet untuk rostem item dari user yang memiliki subscription 'to' atau 'both'
def get_presence_entity_subscription_to(roster, socket_user, username):
    print(f"ROSTER TO AND BOTH IN DB: {roster}")
    socket = socket_user[username]
    for r in roster:
        if(r.get("subscription") == "to" or r.get("subscription") == "both"):
            objek_presence = get_presence_by_jid(r.get('jid'))
            try:
                send_message(socket, objek_presence)
            except Exception as e:
                print(e)
                continue

# Fungsionalitas untuk mengirimkan presence kepada user target
def send_presence_to_someone(jid_target, socket_user, objek_presence):
    objek_presence["to"] = jid_target
    # print(objek_presence)
    send_message(socket_user[jid_target], objek_presence)

# ========== CRUD ada dibawah ini

# Fungsionalitas untuk mengelola initial presence dari user
def init_presence(socket_user, username):
    update_status_online(['online', 'updated_at'], (1, get_timestamp(),), ['user_id'], (username,))
    roster_db_from = get_rosters_user(username, ("from", "both",))
    roster_db_to = get_rosters_user(username, ("to", "both",))
    objek_presence = get_presence_by_jid(username)
    if(roster_db_from):
        send_to_roster_subscription_from(roster_db_from, socket_user, objek_presence)
    if(roster_db_from):
        get_presence_entity_subscription_to(roster_db_to, socket_user, username)

# Fungsionalitas untuk mendapatkan presence dari jid yang diinginkan
def get_presence_by_jid(jid_target):
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
    return get_presence_user(jid_target)

# Fungsionalitas untuk mengelola permintaan user mengubah bio
def set_my_bio(socket_user, username, msg):
    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(username != msg.get("from")):
        return helper_error(msg, "auth", "forbidden")
    updated_at = get_timestamp()
    update_bio(['bio', 'updated_at'], (msg.get('bio'), updated_at,), ['user_id'], (username,))
    my_presence = get_presence_by_jid(username)
    roster_db_from = get_rosters_user(username, ("from", "both",))
    if(not roster_db_from):
        return
    send_to_roster_subscription_from(roster_db_from, socket_user, my_presence, False)

# Fungsionalitas untuk mengelola permintaan user presence bertipe 'unavailable' atau logout
def logout(socket_user, username):
    update_status_online(['online', 'updated_at'], (0, get_timestamp(),), ['user_id'], (username,))
    roster_db_from = get_rosters_user(username, ("from", "both",))
    if(not roster_db_from):
        return
    objek_presence = {
        "stanza": "presence",
        "from": username,
        "type": "unavailable"
    }
    send_to_roster_subscription_from(roster_db_from, socket_user, objek_presence)