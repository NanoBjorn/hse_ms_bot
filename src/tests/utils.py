from server import Server
from settings import APP_NAME, DEBUG


def create_test_client(bot):
    server = Server(APP_NAME, bot, DEBUG)
    return server.test_client()
