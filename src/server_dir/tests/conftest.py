import pytest

from server_dir.bot import bot
from server_dir.server import Server
from common.settings import APP_NAME, DEBUG


@pytest.fixture
def tg_bot():
    return bot


@pytest.fixture
def app(tg_bot):
    return Server(APP_NAME, tg_bot, DEBUG)


@pytest.fixture
def client(app):
    return app.test_client()
