import os

APP_NAME = 'HSE Auth Telegram Bot'

EXTERNAL_HOST = os.getenv('HSE_BOT_HOST', 'localhost')
DEBUG = os.getenv('HSE_BOT_DEBUG', 'True').lower() not in ('false', '0')

MS_CLIENT_ID = os.getenv('MS_CLIENT_ID', 'placeholder_for_client_id')
MS_CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET', 'placeholder_for_client_secret')
MS_REDIRECT_URI_PATH = '/redirect_uri/'
MS_REDIRECT_URI = f'https://{EXTERNAL_HOST}{MS_REDIRECT_URI_PATH}'
MS_CLIENT_SCOPE = 'offline_access+user.read'
MS_AUTHORIZE_URL = f'https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize' \
                   f'?client_id={MS_CLIENT_ID}' \
                   f'&response_type=code' \
                   f'&redirect_uri={MS_REDIRECT_URI}' \
                   f'&response_mode=query' \
                   f'&scope={MS_CLIENT_SCOPE}'
