import peewee
import psycopg2
import pytest
import telebot

from common.models import StorageManager
from common.settings import (
    PG_USER, PG_PASSWORD,
    PG_HOST, PG_DATABASE, PG_PORT
)


def gen_new_member_json(chat_id: int, user_id: int, is_bot: bool):
    message_json = {
        'message_id': 118,
        'from': {
            'id': 797686828,
            'is_bot': False,
            'first_name': 'Gleb',
            'last_name': 'Novikov',
            'username': 'ganovikov'
        },
        'chat': {
            'id': chat_id,
            'title': 'тест вахтера',
            'type': 'supergroup'
        },
        'date': 1588538411,
        'new_chat_members': [
            {
                'id': user_id,
                'is_bot': is_bot,
                'first_name': 'Gleb',
                'last_name': 'Novikov',
                'username': 'ganovikov'
            }
        ]
    }
    return message_json


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
        port=PG_PORT,
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
    message_json = gen_new_member_json(
        chat_id=-1001439152964,
        user_id=797686828,
        is_bot=False
    )
    message = telebot.types.Message.de_json(message_json)
    users = storage_psql.register_new_chat_members(message)
    assert len(users) == 1
    assert users[0].user_id == 797686828


def test_register_user_bot(storage_psql: StorageManager):
    message_json = gen_new_member_json(
        chat_id=-1001439152964,
        user_id=797686828,
        is_bot=True
    )
    message = telebot.types.Message.de_json(message_json)
    users = storage_psql.register_new_chat_members(message)
    assert len(users) == 0


def test_register_user_twice_same(storage_psql: StorageManager):
    message_json = gen_new_member_json(
        chat_id=-1001439152964,
        user_id=797686828,
        is_bot=False
    )
    message = telebot.types.Message.de_json(message_json)
    storage_psql.register_new_chat_members(message)
    with pytest.raises(peewee.IntegrityError):
        storage_psql.register_new_chat_members(message)


def test_register_user_in_different_chats(storage_psql: StorageManager):
    message_json_1 = gen_new_member_json(
        chat_id=-1,
        user_id=797686828,
        is_bot=False
    )
    message_json_2 = gen_new_member_json(
        chat_id=-2,
        user_id=797686828,
        is_bot=False
    )
    users_1 = storage_psql.register_new_chat_members(telebot.types.Message.de_json(message_json_1))
    users_2 = storage_psql.register_new_chat_members(telebot.types.Message.de_json(message_json_2))
    assert len(users_1) == 1
    assert len(users_2) == 1
    assert users_1[0].chat_id == -1
    assert users_2[0].chat_id == -2
