import peewee

from src.server.bot import bot
from src.server.models import StorageManager
from src.server.server import Server
from src.common.settings import (
    APP_NAME, PG_DATABASE,
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
    server = Server(APP_NAME, bot)
    bot.set_server(server)
    bot.set_storage(storage)
    server.run_server()
