import pytest

from bot import bot
from server import Server
from settings import APP_NAME, DEBUG


@pytest.fixture
def tg_bot():
    return bot


@pytest.fixture
def app(tg_bot):
    return Server(APP_NAME, tg_bot, DEBUG)


@pytest.fixture
def client(app):
    return app.test_client()
