import urllib.parse


def encode_state(mail):
    return urllib.parse.quote(mail)


def decode_state(state):
    return state
