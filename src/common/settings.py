import os
import logging

APP_NAME = 'HSE Auth Telegram Bot'

EXTERNAL_HOST = os.getenv('HSE_BOT_HOST', 'localhost')
#DEBUG = os.getenv('HSE_BOT_DEBUG') TODO: deal with debug
DEBUG = 'bot_debug' #ms_debug

PG_DATABASE = os.getenv('HSE_BOT_PG_DATABASE', 'postgres')
PG_HOST = os.getenv('HSE_BOT_PG_HOST', 'postgres')
PG_PORT = int(os.getenv('HSE_BOT_PG_PORT', 5432))
PG_USER = os.getenv('HSE_BOT_PG_USER', 'hse_ms_bot')
PG_PASSWORD = os.getenv('HSE_BOT_PG_PASSWORD', 'hse_ms_bot')

MS_CLIENT_ID = os.getenv('MS_CLIENT_ID', 'placeholder_for_client_id')
MS_CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET', 'placeholder_for_client_secret')
MS_REDIRECT_URI_PATH: str = '/redirect_uri/'
MS_REDIRECT_URI = f'https://{EXTERNAL_HOST}' + (':8000' if DEBUG else '') + MS_REDIRECT_URI_PATH
MS_CLIENT_SCOPE = 'offline_access+user.read'
MS_AUTHORIZE_URL = f'https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize' \
                   f'?client_id={MS_CLIENT_ID}' \
                   f'&response_type=code' \
                   f'&redirect_uri={MS_REDIRECT_URI}' \
                   f'&response_mode=query' \
                   f'&scope={MS_CLIENT_SCOPE}'

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', 'placeholder_for_tg_bot_token')
TG_URL_PATH = '/telegram_bot/'

WORKER_URL_PATH = '/worker'

logging.basicConfig()
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)