from database.dummy.init import get_target_from_my_roster, my_roster
from utils.packet import send_message


def get_my_roster(objek_roster, client_to_manager):
    objek_roster["type"] = "get"
    objek_roster["query"] = {"items": None}
    send_message(client_to_manager, objek_roster)
    del objek_roster['type']
    del objek_roster['query']

def see_my_rosters():
    print(my_roster())

def add_roster(objek_roster, client_to_manager):
    jid_target = input("Masukkan username teman: ")
    name = input("Panggilan teman (boleh kosong): ")
    objek_roster["type"] = "set"
    item = {
        "jid": jid_target,
        "name": name,
        "subscription": "to"
    }
    if(not name):
        del item["name"]
    objek_roster["query"] = {"item": item}
    send_message(client_to_manager, objek_roster)
    del objek_roster['query']

def update_roster(objek_roster, client_to_manager):
    jid_target = input("Masukkan username teman yang namanya mau diubah: ")
    item = get_target_from_my_roster(jid_target)
    if(not item):
        print("JID yang dimasukkan salah")
        return
    name = input("Panggilan teman (boleh kosong): ")
    objek_roster["type"] = "set"
    item["name"] = name
    if(not name):
        del item["name"]
    objek_roster["query"] = {"item": item}
    send_message(client_to_manager, objek_roster)
    del objek_roster['query']

def delete_roster(objek_roster, client_to_manager):
    jid_target = input("Masukkan teman yang ingin dihapus: ")
    item = get_target_from_my_roster(jid_target)
    print(f"ITEM: {item}")
    if(not item):
        print("JID yang dimasukkan salah")
        return
    objek_roster["type"] = "set"
    objek_roster["query"] = {"item": item}
    objek_roster["subscription"] = "remove"
    send_message(client_to_manager, objek_roster)
    del objek_roster["type"]
    del objek_roster["query"]
    del objek_roster["subscription"]