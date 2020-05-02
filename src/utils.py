import requests

from settings import MS_AUTHORIZE_URL


def gen_authorize_url(state=None):
    return MS_AUTHORIZE_URL + (f'&state={state}' if state is not None else '')


def get_ngrok_url(host='127.0.0.1', port=4040):
    resp = requests.get(f'http://{host}:{port}/api/tunnels')
    return resp.json()['tunnels'][0]['public_url']
