import base64

def decode_payload(payload):

    try:

        return base64.b64decode(payload).decode()

    except:

        return "Invalid payload"