import logging

from bot import bot
from server import Server
from settings import APP_NAME, DEBUG

logging.basicConfig()

if __name__ == '__main__':
    server = Server(APP_NAME, bot, DEBUG)
    server.run_server()
