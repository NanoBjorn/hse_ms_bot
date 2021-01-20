from common.utils import get_ngrok_url
import requests
from time import sleep
from common.settings import WORKER_URL_PATH
while 1:
    url: str = get_ngrok_url()
    requests.get(url + WORKER_URL_PATH)
    sleep(5)
