import logging
import typing

import peewee
import telebot


class User(peewee.Model):
    chat_id = peewee.BigIntegerField(index=True)
    user_id = peewee.BigIntegerField(index=True)
    current_username = peewee.CharField(null=True)
    current_first_name = peewee.CharField(null=True)
    current_last_name = peewee.CharField(null=True)
    current_user_mail = peewee.CharField(index=True)
    current_mail_status = peewee.BigIntegerField(null=True)

    class Meta:
        primary_key = peewee.CompositeKey('chat_id', 'user_id')


MODELS = [User]

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, db: peewee.Database):
        self._db = db
        self._db.bind(MODELS)
        self._db.connect()
        self._db.create_tables(MODELS)


    def update_mail(self, message: telebot.types.Message, mail):
        User.update(current_user_mail=mail).where(User.chat_id == message.chat.id
                                                  and User.user_id == message.from_user.id)
        User.update(current_mail_status=0).where(User.chat_id == message.chat.id
                                                  and User.user_id == message.from_user.id)


    def clean_db(self):
        self._db.drop_tables(MODELS)
        self._db.close()

    def register_new_chat_members(self, message: telebot.types.Message) -> typing.List[User]:
        res = []
        for user in message.new_chat_members:
            if user.is_bot:
                logger.info('User %s is bot, skipping', message.from_user)
                continue
            with self._db.atomic() as db:
                db_user = User.create(
                    chat_id=message.chat.id,
                    user_id=user.id,
                    current_username=user.username,
                    current_first_name=user.first_name,
                    current_last_name=user.last_name,
                    current_user_mail="",
                    current_mail_status=0
                )
            res.append(db_user)
        return res
