import peewee

from server_dir.bot import bot
from common.models import StorageManager
from server_dir.server import Server
from common.settings import (
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
    # TODO: dont forget about DEBUG
    server = Server(APP_NAME, bot, DEBUG)
    # server_dir = Server(APP_NAME, bot, "bot_debug") #ms_debug
    bot.set_server(server)
    bot.set_storage(storage)
    server.run_server()
