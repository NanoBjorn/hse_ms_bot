import peewee
import psycopg2

from bot import bot
from models import StorageManager
from server import Server
from settings import (
    APP_NAME, DEBUG, PG_DATABASE,
    PG_HOST, PG_USER, PG_PASSWORD, PG_PORT
)

if __name__ == '__main__':
    psql_db = peewee.PostgresqlDatabase(
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        isolation_level=psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    )
    storage = StorageManager(psql_db)
    server = Server(APP_NAME, bot, DEBUG)
    bot.set_server(server)
    bot.set_storage(storage)
    server.run_server()
