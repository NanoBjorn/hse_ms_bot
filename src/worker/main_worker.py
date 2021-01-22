from common.models import StorageManager
from common.utils import get_ngrok_url
import requests
import peewee
from time import sleep
import json
from common.settings import (
    APP_NAME, PG_DATABASE, WORKER_URL_PATH,
    PG_HOST, PG_USER, PG_PASSWORD, PG_PORT, DEBUG
)

if __name__ == '__main__':
    psql_db = peewee.PostgresqlDatabase(
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        isolation_level=0
    )
    storage = StorageManager(psql_db)
    while 1:
        url: str = get_ngrok_url()
        # print(storage.get_actions())
        data = json.dumps(storage.get_actions())
        requests.post(url + WORKER_URL_PATH, data, headers = {'content-type': 'application/json'}) # TODO: check safety
        sleep(5)
