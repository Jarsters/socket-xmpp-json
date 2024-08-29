components = {} # List of object = {username_relay: objek_relay} -> Isinya kumpulan relay
users = {} # {username_1: {"password": blabla, "bio": blabla}} -> Isinya kumpulan user
socket_user = {} # {username_1: socket_user_1}
rosters = {}

'''
FORMAT ROSTER DATABASE DUMMY
rosters = {
    jid_user_1: {
        item_jid_user_1: {
            atribute_jid: ,
            atribute_name: ,
            atribute_subscription: ,
        },
        item_jid_user_2: {
            atribute_jid: ,
            atribute_name: ,
            atribute_subscription: ,
        },
        ....
    },
    jid_user_2: {
        .....
    }
}

FORMAT ROSTER DATABASE ASLI
TABLE_NAME = ROSTER
COLUMN:
    - ROSTER_ID
    - OWNER_ROSTER_JID
    - JID
    - NAME
    - SUBSCRIPTION
    - CREATED_AT
    - UPDATED_AT

'''

'''
FORMAT USERS DATABASE DUMMY
users = {
    jid_1: {
        "username": username,
        "password": password,
        "bio": "Feel happy using this application! ;D",
        "online": True,
        "updated_at": timestamp,
        "created_at": timestamp
    }
}

FORMAT USERS DATABASE ASLI
TABLE_NAME = USER
    - USERNAME/JID
    - PHONE_NUMBER
    - PASSWORD
    - BIO
    - ONLINE
    - CREATED_AT
    - UPDATED_AT
'''