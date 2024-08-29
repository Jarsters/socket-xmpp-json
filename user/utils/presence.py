from utils.packet import send_message
from database.dummy.init import users

def init_presence(objek_presence, client_to_manager):
    send_message(client_to_manager, objek_presence)

def update_presence(objek_presence, client_to_manager):
    bio = input("Masukkan status terbarumu: ")
    objek_presence['bio'] = bio
    print(objek_presence)
    send_message(client_to_manager, objek_presence)
    del objek_presence['bio']

# Directed presence
def get_presence_target(objek_presence, client_to_manager):
    jid_target = input("Masukkan username yang diinginkan: ")
    objek_presence['to'] = jid_target
    print(objek_presence)
    send_message(client_to_manager, objek_presence)
    del objek_presence['to']

def logout(objek_presence, client_to_manager):
    objek_presence['type'] = 'unavailable'
    send_message(client_to_manager, objek_presence)

def view_users_presence():
    print("masuk sini")
    print(users)
    for u in users.values():
        print(u)