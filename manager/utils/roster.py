'''
TIDAK MENGIMPLEMENTASIKAN ROSTER PUSH, KARENA HANYA AKAN ADA 1 RESOURCE.
'''


'''
FORMAT ROSTER REQUEST
{
    stanza: "iq",
    namespace: "roster",
    from: initial_entity,
    type: "get/set",
    subscription: "remove" # untuk delete roster,
    query: {
                item: {
                    jid: ,
                    name: ,
                    subscription: to/from/both
                }
            }
}
'''

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

def helper_set_rosters(rosters, username_target, item):
    if(not rosters.get(username_target)):
        rosters[username_target] = {}
    rosters[username_target][item["jid"]] = item

def helper_check_and_get_roster(rosters, username, target_jid):
    if(not rosters.get(username)):
        return None
    if(rosters.get(username).get(target_jid)):
        return rosters.get(username).get(target_jid)
    return None

def set_to_rosters(rosters, username, item):
    jid_target = item["jid"]
    # Mengecek apakah init_user sudah masuk ke roster_target
    tmp_item_jid = helper_check_and_get_roster(rosters, jid_target, username)
    # print(f"TIJ 1: {tmp_item_jid}")
    # print(f"ITEM 1: {item}")
    if(not tmp_item_jid):
        tmp_item_jid = {"jid": username, "subscription": None}
    if(not rosters.get(username)):
        rosters[username] = {}
        # Untuk set si init_entity sebagai rosternya contact
        tmp_item_jid["subscription"] = "from"
    elif(not rosters.get(username).get(jid_target)):
        tmp_item_jid["subscription"] = "from"
    elif(tmp_item_jid.get("subscription") == "to"):
        item["subscription"] = "both"
        tmp_item_jid["subscription"] = "both"
    print(item)
    print(tmp_item_jid)
    helper_set_rosters(rosters, username, item)
    helper_set_rosters(rosters, jid_target, tmp_item_jid)

def delete_from_rosters(rosters, username, item):
    jid_target = item["jid"]
    # Mengecek apakah init_user sudah masuk ke roster_target
    tmp_item_jid = helper_check_and_get_roster(rosters, jid_target, username)
    init_entity_roster = rosters.get(username).get(jid_target)
    # print(f"TIJ 1: {tmp_item_jid}")
    # print(f"INIT_ENTITY_ITEM 1: {init_entity_roster}")

    # Jika both, init_entity => "from", target_entity => "to"
    # Jika to, init_entity => None, target_entity => None

    if(init_entity_roster.get("subscription") == "both"):
        tmp_item_jid["subscription"] = "to"
        init_entity_roster["subscription"] = "from"
        helper_set_rosters(rosters, username, init_entity_roster)
        helper_set_rosters(rosters, jid_target, tmp_item_jid)
    elif(init_entity_roster.get("subscription") == "to"):
        print("Masuk sini")
        del rosters[username][jid_target]
        del rosters[jid_target][username]
    print(init_entity_roster)
    print(tmp_item_jid)
    print(rosters)

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

# Yang diatas ini fungsi CRUD-nya


# CRUD yang dipanggil keluar ada di bawah ini
def get_roster(username, table_roster, msg):
    '''
        AMBIL YANG SUBSCRIPTIONNYA TO ATAU BOTH
    '''
    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(msg.get("from") != username):
        return helper_error(msg, "auth", "forbidden")

    # ====== INI PAKE DATABASE DUMMY ======
    rosters = table_roster.get(username)
    roster = [] # Ini nanti ganti jadi table di db
    if(rosters):
        for value in rosters.values():
            if(value.get("subscription") == 'to' or value.get("subscription") == "both"):
                roster.append(value)

    # ===== NANTI DATABASE ASLI DIBAWAH SINI ======
    # logic in here

    msg = helper_parse_from_req_to_res(msg)
    msg["query"]["items"] = roster

    return msg

def set_roster(username, table_roster, msg, users):
    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(username != msg.get("from")):
        return helper_error(msg, "auth", "forbidden")
    elif(not users.get(msg.get("query").get("item").get("jid"))):
        return helper_error(msg, "modify", "bad-request")
    
    try:
        query = msg.get("query")
        item = query.get("item")
        jid = item.get("jid")
    except AttributeError as e:
        print(e)
        return helper_error(msg, "modify", "bad-request")

    if(query and item and jid and users.get(jid)):
        # ==== ini set roster masih ke data dummy
        set_to_rosters(table_roster, username, item)

        del msg["query"]
        return helper_parse_from_req_to_res(msg)
    else:
        return helper_error(msg, "modify", "bad-request")

def delete_roster(username, table_roster, msg, users):
    if (type(msg) != dict):
        return helper_error(msg, "modify", "bad-request")
    elif(username != msg.get("from")):
        return helper_error(msg, "auth", "forbidden")
    elif(not users.get(msg.get("query").get("item").get("jid"))):
        return helper_error(msg, "modify", "bad-request")
    
    try:
        query = msg.get("query")
        item = query.get("item")
        jid = item.get("jid")
    except AttributeError as e:
        print(e)
        return helper_error(msg, "modify", "bad-request")
    
    # if(not table_roster.get(username)):
    #     return helper_error(msg, "modify", "bad-request")
    if(not helper_check_and_get_roster(table_roster, item["jid"], username)):
        return helper_error(msg, "modify", "bad-request")
    
    if(query and item and jid and users.get(jid)):
        # ==== ini delete roster masih ke data dummy
        delete_from_rosters(table_roster, username, item)

        del msg["query"]
        return helper_parse_from_req_to_res(msg)
    else:
        return helper_error(msg, "modify", "bad-request")