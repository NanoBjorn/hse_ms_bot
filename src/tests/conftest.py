import pytest

from bot import bot
from server import Server
from settings import APP_NAME, DEBUG


@pytest.fixture
def app():
    return Server(APP_NAME, bot, DEBUG)


@pytest.fixture
def client(app):
    return app.test_client()
