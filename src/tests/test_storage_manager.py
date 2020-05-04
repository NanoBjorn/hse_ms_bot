import peewee
import psycopg2
import pytest
import telebot

from models import StorageManager
from settings import PG_USER, PG_PASSWORD, PG_HOST, PG_DATABASE


@pytest.fixture
def storage_psql():
    # TODO: Move database operations to StorageManager
    test_db_name = 'test_' + PG_DATABASE
    with psycopg2.connect(user=PG_USER, password=PG_PASSWORD, host=PG_HOST) as conn:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(f'DROP DATABASE IF EXISTS {test_db_name}')
            cursor.execute(f'CREATE DATABASE {test_db_name}')

    psql_db = peewee.PostgresqlDatabase(
        database=test_db_name,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        isolation_level=psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    )

    storage = StorageManager(psql_db)
    yield storage
    storage.clean_db()

    with psycopg2.connect(user=PG_USER, password=PG_PASSWORD, host=PG_HOST) as conn:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(f'DROP DATABASE {test_db_name}')


def test_register_user_no_bot(storage_psql: StorageManager):
    message_str = {
        'message_id': 118,
        'from': {
            'id': 797686828,
            'is_bot': False,
            'first_name': 'Gleb',
            'last_name': 'Novikov',
            'username': 'ganovikov'
        },
        'chat': {
            'id': -1001439152964,
            'title': 'тест вахтера',
            'type': 'supergroup'
        },
        'date': 1588538411,
        'new_chat_members': [
            {
                'id': 797686828,
                'is_bot': False,
                'first_name': 'Gleb',
                'last_name': 'Novikov',
                'username': 'ganovikov'
            }
        ]
    }
    message = telebot.types.Message.de_json(message_str)
    users = storage_psql.register_new_chat_members(message)
    assert len(users) == 1
    assert users[0].user_id == 797686828


def test_register_user_bot(storage_psql: StorageManager):
    message_str = {
        'message_id': 118,
        'from': {
            'id': 797686828,
            'is_bot': False,
            'first_name': 'Gleb',
            'last_name': 'Novikov',
            'username': 'ganovikov'
        },
        'chat': {
            'id': -1001439152964,
            'title': 'тест вахтера',
            'type': 'supergroup'
        },
        'date': 1588538411,
        'new_chat_members': [
            {
                'id': 797686828,
                'is_bot': True,
                'first_name': 'Gleb',
                'last_name': 'Novikov',
                'username': 'ganovikov'
            }
        ]
    }
    message = telebot.types.Message.de_json(message_str)
    users = storage_psql.register_new_chat_members(message)
    assert len(users) == 0
