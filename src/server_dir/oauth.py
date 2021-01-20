import requests

from common.settings import (
    MS_CLIENT_ID, MS_CLIENT_SCOPE,
    MS_REDIRECT_URI, MS_CLIENT_SECRET
)


def get_token(code):
    url = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f'client_id={MS_CLIENT_ID}' \
           f'&code={str(code)}' \
           f'&scope={MS_CLIENT_SCOPE}' \
           f'&redirect_uri={MS_REDIRECT_URI}' \
           f'&grant_type=authorization_code' \
           f'&client_secret={MS_CLIENT_SECRET}'
    resp = requests.post(url, headers=headers, data=data).json()
    return resp.get('access_token')


def get_ms_me(access_token):
    url = 'https://graph.microsoft.com/v1.0/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    resp = requests.get(url, headers=headers).json()
    return {
        'displayName': resp.get('displayName'),
        'mail': resp.get('mail')
    }
