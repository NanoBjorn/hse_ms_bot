import urllib.parse

from settings import MS_AUTHORIZE_URL


def gen_authorize_url(state=None):
    return MS_AUTHORIZE_URL + (f'&state={state}' if state is not None else '')
