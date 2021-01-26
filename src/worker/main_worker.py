from src.common.utils import get_ngrok_url
import requests
from time import sleep
from src.common.settings import (
    WORKER_URL_PATH, WORKER_SLEEP
)

if __name__ == '__main__':
    while 1:
        url: str = get_ngrok_url()
        # print(storage.get_actions())
        # data = json.dumps(storage.get_actions())
        # requests.post(url + WORKER_URL_PATH, data, headers = {'content-type': 'application/json'})
        # TODO: check safety
        requests.get(url + WORKER_URL_PATH)
        sleep(WORKER_SLEEP)
