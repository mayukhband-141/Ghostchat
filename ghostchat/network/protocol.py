import json
import time

def encode_message(msg_type, sender, content=""):
    payload = {
        "type": msg_type,      # "chat" | "quit"
        "sender": sender,
        "message": content,
        "timestamp": time.time()
    }
    return json.dumps(payload).encode("utf-8")

def decode_message(raw_bytes):
    return json.loads(raw_bytes.decode("utf-8"))
