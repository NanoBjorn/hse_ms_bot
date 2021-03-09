from src.common.utils import get_ngrok_url
import requests
from time import sleep
from src.common.settings import WORKER_URL_PATH, WORKER_SLEEP, DEBUG, EXTERNAL_HOST, SERVER_HOST

if __name__ == '__main__':
    if DEBUG.find('ngrok') != -1:
        url: str = get_ngrok_url()
    else:
        url: str = SERVER_HOST
    while 1:
        requests.get(url + WORKER_URL_PATH)
        sleep(WORKER_SLEEP)
