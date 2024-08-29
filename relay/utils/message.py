from utils.packet import send_message


def send_message_to_target(communicate, packet):
    if(not communicate):
        return False
    send_message(communicate, packet)
    return True

def send_packet_error(communicate, code_error, initiator):
    packet = {
        "stanza": "message",
        "from": "relay",
        "to": initiator,
        "error": True,
        "body": "User not found Or User not online"
    }
    if(code_error == 404):
        send_message(communicate, packet)
