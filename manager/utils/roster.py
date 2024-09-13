from database.sqlite.roster import delete_roster_user, get_roster_user, rosters as r_db, get_rosters_user, save_rosters, update_subscription
from database.sqlite.user import get_user_by_username
from utils.get_time import get_timestamp

def helper_parse_from_req_to_res(msg):
    msg["type"] = "result"
    tmp = msg["from"]
    del msg["from"]
    msg["to"] = tmp
    del tmp
    return msg

def helper_error(msg, error_type, stanza_error):
    msg["type"] = "error"
    tmp = msg["from"]
    del msg["from"]
    msg["to"] = tmp
    del tmp
    del msg["query"]
    msg["error"] = {}
    msg["error"]["type"] = error_type
    msg["error"]["stanza_error"] = stanza_error
    msg["error"]["stanza_error_ns"] = "xmpp-stanzas"
    return msg

# Fungsionalitas membantu menyimpan atau mengubah roster item dalam user's roster
def helper_set_rosters(username_target, item, updating=False):
    if(updating):
        print(f"DATA IN UPDATING: {username_target}, {item}")
        data_set_tuple = (item.get("name"), item.get("subscription"))
        data_condition_tuple = (username_target, item.get("jid"))
        update_subscription(data_set_tuple, data_condition_tuple)
    else:
        print(f"HST: {username_target}, {item}")
        item_roster = (username_target,) + tuple(item.values())
        save_rosters(list(item_roster), get_timestamp())
    print(f"ROSTER IN DB: {r_db.get_all()}")

# def helper_check_and_get_roster(rosters, username, target_jid):
def helper_check_and_get_roster(username, target_jid):
    print(f"GRU DB: {get_roster_user(username, target_jid)}")
    return get_roster_user(username, target_jid)

# Fungsionalitas untuk membantu menambahkan atau mengubah roster item
def set_to_rosters(username, item):
    jid_target = item["jid"]
    updating = False
    new = False
    # Mengecek apakah init_user sudah masuk ke roster_target
    tmp_item_jid = helper_check_and_get_roster(jid_target, username)
    # Logic komponen manager untuk menentukan apakah roster item akan ditambahkan atau diperbarui saja
    if(not tmp_item_jid):
        tmp_item_jid = {"jid": username, "subscription": None}
        new = True
    else:
        print("We will updating")
        updating = 1
    # Menentuka tipe subscription yang akan ditetapkan berdasarkan logic kepintaran pembeda
    if(not tmp_item_jid.get("subscription")):
        tmp_item_jid["subscription"] = "from"
    elif(tmp_item_jid.get("subscription") == "to"):
        updating = 2
        item["subscription"] = "both"
        tmp_item_jid["subscription"] = "both"
    if(updating == 2 or new):
        # Memanggil fungsionalitas untuk menyimpan atau mengubah roster item dari user's roster
        helper_set_rosters(username, item, updating)
        # Memanggil fungsionalitas untuk menyimpan atau mengubah roster item dari roster item's roster dengan roster itemnya adalah user pengirim
        helper_set_rosters(jid_target, tmp_item_jid, updating)
    else:
        helper_set_rosters(username, item, updating)

# Fungsionalitas untuk menghapus roster item dari user's roster
def delete_from_rosters(username, item):
    jid_target = item["jid"]
    # Mengecek apakah user pengirim sudah masuk ke roster item's roster
    tmp_item_jid = helper_check_and_get_roster(jid_target, username)
    init_entity_roster = get_roster_user(username, jid_target)

    # Jika both, init_entity => "from", target_entity => "to"
    # Jika to, init_entity => None, target_entity => None
    if(init_entity_roster.get("subscription") == "both"):
        tmp_item_jid["subscription"] = "to"
        init_entity_roster["subscription"] = "from"
        helper_set_rosters(username, init_entity_roster, True)
        helper_set_rosters(jid_target, tmp_item_jid, True)
    elif(init_entity_roster.get("subscription") == "to"):
        delete_roster_user(username, jid_target)
        delete_roster_user(jid_target, username)

# Fungsionalitas membuat packet presence subscribed
def get_packet_subscribed_for_init_entity(init_entity, target_entity):
    '''
    {
        stanza: 'presence',
        'to': init_entity,
        'from': target_entity,
        'type': 'subscribed',
    }
    '''
    objek = {
        'stanza': 'presence',
        'from': target_entity,
        'to': init_entity,
        'type': 'subscribed'
    }
    return objek

# Fungsionalitas membuat packet presence unsubscribed
def get_packet_unsubscribed_for_init_entity(init_entity, target_entity):
    '''
    {
        stanza: 'presence',
        'to': init_entity,
        'from': target_entity,
        'type': 'unsubscribed',
    }
    '''
    objek = {
        'stanza': 'presence',
        'from': target_entity,
        'to': init_entity,
        'type': 'unsubscribed'
    }
    return objek

# Yang diatas ini fungsionalitas helper

# CRUD yang dipanggil keluar ada di bawah ini
# Fungsionalitas untuk mendapatkan roster dari user
def get_rosters(username, msg):
    '''
        AMBIL YANG SUBSCRIPTIONNYA TO ATAU BOTH
    '''
    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(msg.get("from") != username):
        return helper_error(msg, "auth", "forbidden")
    
    # Meminta data roster dari database, dengan tipe subscription 'to' atau 'both'
    roster = get_rosters_user(username, ('to', 'both'))

    msg = helper_parse_from_req_to_res(msg)
    msg["query"]["items"] = roster
    return msg

# Fungsional menambahkan atau mengubah roster item
def set_roster(username, msg):
    # Validitas data yang dimasukkan oleh user
    try:
        query = msg.get("query")
        item = query.get("item")
        jid = item.get("jid")
    except AttributeError as e:
        print(e)
        return helper_error(msg, "modify", "bad-request")
    
    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(username != msg.get("from")):
        return helper_error(msg, "auth", "forbidden")
    elif(not get_user_by_username(jid)):
        return helper_error(msg, "modify", "bad-request")
    # Data yang diberikan valid
    else:
        # Memanggil fungsionalitas helper untuk menambahkan atau mengubah roster item
        set_to_rosters(username, item)
        del msg["query"]
        # Memberikan feedback bahwa permintaan menambahkan atua mengubah roster item berhasil dilakukan
        return helper_parse_from_req_to_res(msg)

# Fungsionalitas untuk menghapus roster item dari user's roster
def delete_roster(username, msg):
    try:
        query = msg.get("query")
        item = query.get("item")
        jid = item.get("jid")
    except AttributeError as e:
        print(e)
        return helper_error(msg, "modify", "bad-request")

    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(username != msg.get("from")):
        return helper_error(msg, "auth", "forbidden")
    elif(not get_user_by_username(jid)):
        return helper_error(msg, "modify", "bad-request")
    
    tmp_r = helper_check_and_get_roster(username, item["jid"])
    # Validitas jika tidak ada keterhubungan atau tipe subscriptionnya adalah 'from'
    if(not tmp_r or tmp_r.get("subscription") == "from"):
        return helper_error(msg, "modify", "bad-request")
    else:
        delete_from_rosters(username, item)
        del msg["query"]
        return helper_parse_from_req_to_res(msg)