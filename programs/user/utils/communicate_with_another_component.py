from database.dummy.init import delete_from_my_roster, save_single_roster, save_to_my_rosters, save_to_users_presence, user_presence_unavailable
from utils.packet import get_message_manager, get_message_relay
import json

def handle_message_from_relay(communicate):
    error = False
    while not error:
        try:
            messages = get_message_relay(communicate)
            for message in messages:
                message = json.loads(message)
                if(message.get("error_msg")):
                    error = True
                    print("Komponen relay mengalami error....")
                    break
                initiator = message.get("from")
                msg = message.get("body")
                print(f"\n\t{initiator}: {msg}")
        # except WindowsError as wer:
        #     print(wer)
        #     print("Connection with relay ended winerror...")
        #     break
        except Exception as e:
            print(e)
            print("Connection with relay ended exception....")
            break

def handle_message_from_manager(communicate):
    error = False
    while not error:
        try:
            messages = get_message_manager(communicate)
            for message in messages:
                message = json.loads(message)
                # print(message)
                if(message.get("error_msg")):
                    error = True
                    print("Komponen manager mengalami error....")
                    break
                elif(message.get("type") == "result" and message.get("stanza") == "iq" and message.get("namespace") == "roster" and message.get("query") and message.get("query").get("items")):
                    # print("masuk items")
                    items = message.get("query").get("items")
                    save_to_my_rosters(items)
                elif(message.get('type') == "error"):
                    print("Mendapatkan stanza yang error")
                elif(message.get('stanza') == 'presence' and message.get('type') == 'subscribed' and message.get("item")):
                    item = message.get("item")
                    save_single_roster(item)
                    # time.sleep(0.2)
                elif(message.get('stanza') == 'presence' and message.get('type') == 'unsubscribed'):
                    jid_target = message.get("from")
                    delete_from_my_roster(jid_target)
                    # print(message)
                elif(message.get('stanza') == 'presence' and message.get('type') == 'unavailable'):
                    # print("Masuk unavailable presence")
                    user_presence_unavailable(message)
                elif(message.get('stanza') == 'presence'):
                    # print("Masuk init presence")
                    save_to_users_presence(message)
                print(f"Manager: {message}")
        except Exception as e:
            print(e)
            print("Connection with manager ended....")
            break