from flask import Flask, request

from oauth import get_token, get_ms_me
from settings import APP_NAME, MS_REDIRECT_URI_PATH
from state import decode_state

app = Flask(APP_NAME)


@app.route(MS_REDIRECT_URI_PATH)
def redirect_uri():
    ms_code = request.args.get('code')
    state = request.args.get('state')
    ms_access_token = get_token(ms_code)
    me_resp = get_ms_me(ms_access_token)
    if decode_state(state) == me_resp.get('mail'):
        return 'Success!'
    return 'Email does not correspond to state argument!'
