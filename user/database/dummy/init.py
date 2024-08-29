my_rosters = {}
users = {} # users presence

def save_to_my_rosters(items):
    for item in items:
        my_rosters[item["jid"]] = item
    print(my_rosters)

def save_single_roster(item):
    my_rosters[item["jid"]] = item

def get_target_from_my_roster(jid_target):
    return my_rosters.get(jid_target)

def delete_from_my_roster(jid_target):
    del my_rosters[jid_target]

def my_roster():
    return my_rosters

'''
users = {
    jid_user: {
        username: username,
        bio: bio,
        online: False/True,
        updated_at: updated_at
    }
}
'''

def save_to_users_presence(items):
    item = items.copy()
    jid = item.get('from')
    if(item.get('to')):
        del item["to"]
    if(item.get('stanza')):
        del item['stanza']
    if(item.get('from')):
        del item['from']
    users[jid] = item

def user_presence_unavailable(item):
    print(item)
    print(users)
    if(users.get(item.get('from'))):
        users[item.get('from')]['online'] = False