import logging
import typing
from datetime import datetime, timedelta
import peewee
import telebot
from src.common.settings import DEADLINE_TIME


class User(peewee.Model):
    chat_id = peewee.BigIntegerField(index=True)
    user_id = peewee.BigIntegerField(index=True)
    current_username = peewee.CharField(null=True)
    current_first_name = peewee.CharField(null=True)
    current_last_name = peewee.CharField(null=True)
    current_user_mail = peewee.CharField(null=True)
    current_mail_authorised = peewee.CharField(null=True)

    class Meta:
        primary_key = peewee.CompositeKey('chat_id', 'user_id')


class Action(peewee.Model):
    time = peewee.DateTimeField()
    chat_id = peewee.BigIntegerField(index=True)
    user_id = peewee.BigIntegerField(index=True)

    class Meta:
        primary_key = peewee.CompositeKey('chat_id', 'user_id')


class Message(peewee.Model):
    message_id = peewee.BigIntegerField()
    chat_id = peewee.BigIntegerField()
    user_id = peewee.BigIntegerField()


MODELS = [User, Action, Message]

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, db: peewee.Database):
        self._db = db
        self._db.bind(MODELS)
        self._db.connect()
        self._db.create_tables(MODELS)

    def update_mail(self, message: telebot.types.Message, mail):
        User.update(current_user_mail=mail).where(
            (User.user_id == message.from_user.id) & (User.chat_id == message.chat.id)).execute()
        User.update(current_mail_authorised='0').where(
            (User.user_id == message.from_user.id) & (User.chat_id == message.chat.id)).execute()

    def clean_db(self):
        self._db.drop_tables(MODELS)
        self._db.close()

    def get_db(self):
        res = User.select()
        # print(res)
        return res

    def add_message(selfself, message_id, chat_id, user_id):
        print(message_id)
        Message.create(message_id=message_id, chat_id=chat_id, user_id=user_id)

    def register_new_chat_members(self, message: telebot.types.Message) -> typing.List[User]:
        res = []
        for user in message.new_chat_members:
            if user.is_bot:
                logger.info('User %s is bot, skipping', message.from_user)
                continue
            with self._db.atomic() as db:
                if len(User.select().where(
                        (User.user_id == message.from_user.id) & (User.chat_id == message.chat.id))) > 0:
                    continue
                db_user = User.create(
                    chat_id=message.chat.id,
                    user_id=user.id,
                    current_username=user.username,
                    current_first_name=user.first_name,
                    current_last_name=user.last_name,
                    current_user_mail="",
                    current_mail_authorised="0"
                )
                db_action = Action.create(
                    chat_id=message.chat.id,
                    user_id=user.id,
                    time=datetime.now()
                )
            res.append(db_user)
        return res

    def get_messages(self, chat_id, user_id):
        query = Message.select().where((chat_id == Message.chat_id) &
                                       (user_id == Message.user_id))
        res = []
        for message in query:
            res.append(message)
        Message.delete().where((chat_id == Message.chat_id) &
                               (user_id == Message.user_id)).execute()
        return res

    def get_actions(self):
        query = Action.select().where(Action.time < datetime.now() - timedelta(minutes=DEADLINE_TIME))
        res = []
        for it in query:
            user_query = User.select().where((it.user_id == User.user_id) &
                                             (it.chat_id == User.chat_id) &
                                             (User.current_mail_authorised == '0'))
            if len(user_query) > 0:
                for user in user_query:
                    res.append(user)
            User.delete().where((it.user_id == User.user_id) &
                                (it.chat_id == User.chat_id) &
                                (User.current_mail_authorised == '0')).execute()

        Action.delete().where(Action.time < datetime.now() - timedelta(minutes=DEADLINE_TIME)).execute()

        return res

    def success_mail(self, mail, user_id, chat_id):
        User.update(current_mail_authorised="1").where((User.chat_id == chat_id) &
                                                       (User.user_id == user_id) &
                                                       (User.current_user_mail == mail) &
                                                       (User.current_mail_authorised == "0")).execute()
        return User.select().where((User.chat_id == chat_id) &
                                   (User.user_id == user_id) &
                                   (User.current_user_mail == mail) &
                                   (User.current_mail_authorised == "1"))

    def fail_mail(self, mail):
        return User.select().where((User.current_user_mail == mail) & (User.current_mail_authorised == "0"))
