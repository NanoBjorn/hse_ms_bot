import logging
import typing
from datetime import datetime, timedelta
import peewee
import telebot
from src.common.settings import DEADLINE_TIME


class Banned(peewee.Model):
    user_id = peewee.CharField(primary_key=True)


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
    current_username = peewee.CharField(null=True)

    class Meta:
        primary_key = peewee.CompositeKey('chat_id', 'user_id')


class Message(peewee.Model):
    message_id = peewee.BigIntegerField()
    chat_id = peewee.BigIntegerField()
    user_id = peewee.BigIntegerField()


MODELS = [User, Action, Message, Banned]

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, db: peewee.Database):
        self._db = db
        self._db.bind(MODELS)
        self._db.connect()
        self._db.create_tables(MODELS)

    def update_mail(self, message: telebot.types.Message, mail):
        if len(User.select().where((User.user_id != message.from_user.id) & (User.current_user_mail == mail))) > 0:
            return 1
        if len(User.select().where((User.user_id == message.from_user.id) & (User.current_mail_authorised == '1'))):
            return 2
        User.update(current_user_mail=mail).where(
            (User.user_id == message.from_user.id)).execute()
        User.update(current_mail_authorised='0').where(
            (User.user_id == message.from_user.id)).execute()
        return 0

    def clean_db(self):
        self._db.drop_tables(MODELS)
        self._db.close()

    def get_db(self):
        res = User.select()
        return res

    def get_user_chats(self, user_id):
        return [user for user in User.select().where((user_id == User.user_id))]

    def check_ban(self, user_id):
        query = Banned.select().where((Banned.user_id == user_id))
        return len(query) > 0

    def ban(self, user_id):
        Banned.create(user_id=user_id)

    def unban(self, user_id):
        Banned.delete().where((Banned.user_id == user_id)).execute()

    def add_message(self, message_id, chat_id, user_id):
        Message.create(message_id=message_id, chat_id=chat_id, user_id=user_id)

    def check_member(self, message):
        if len(User.select().where((User.user_id == message.from_user.id) & (User.chat_id == message.chat.id))) > 0:
            return 0
        else:
            return 1

    def check_reg(selfself, message):
        if len(User.select().where((User.user_id == message.from_user.id) &
                                   (User.current_mail_authorised == '1'))) > 0 or message.from_user.is_bot:
            return 0
        else:
            return 1

    def register_old_chat_member(self, message: telebot.types.Message):
        user = message.from_user
        with self._db.atomic() as db:
            if len(User.select().where((User.user_id == user.id) & (User.chat_id == message.chat.id))) > 0:
                return 0
            db_user = User.create(
                chat_id=message.chat.id,
                user_id=user.id,
                current_username=user.username,
                current_first_name=user.first_name,
                current_last_name=user.last_name,
                current_user_mail="",
                current_mail_authorised="0"
            )
            if len(User.select().where((User.user_id == user.id) & (User.current_mail_authorised == "1"))) <= 0:
                db_action = Action.create(
                    chat_id=message.chat.id,
                    user_id=user.id,
                    current_username=user.username,
                    time=datetime.now()
                )
                return 1
        return 0

    def register_new_chat_members(self, message: telebot.types.Message) -> typing.List[User]:
        res = []
        for user in message.new_chat_members:
            if user.is_bot:
                logger.info('User %s is bot, skipping', message.from_user)
                continue
            with self._db.atomic() as db:
                if len(User.select().where((User.user_id == user.id) & (User.chat_id == message.chat.id))) > 0:
                    continue
                if len(User.select().where((User.user_id == user.id) & (User.current_mail_authorised == '1'))) > 0:
                    user_query = User.select().where((User.user_id == user.id) & (User.current_mail_authorised == '1'))
                    temp = [user_cur for user_cur in user_query]
                    db_user = User.create(
                        chat_id=message.chat.id,
                        user_id=user.id,
                        current_username=user.username,
                        current_first_name=user.first_name,
                        current_last_name=user.last_name,
                        current_user_mail=temp[0].current_user_mail,
                        current_mail_authorised="1"
                    )
                else:
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
                        current_username=user.username,
                        time=datetime.now()
                    )
                    res.append(db_user)
        return res

    def get_messages(self, user_id):
        query = Message.select().where((user_id == Message.user_id))
        res = []
        for message in query:
            res.append(message)
        Message.delete().where((user_id == Message.user_id)).execute()
        return res

    def get_user_id(self, username):
        res = [it for it in User.select().where((User.current_username == username))]
        return res[0].user_id

    def ignore(self, user_id):
        Action.delete().where(Action.user_id == user_id).execute()
        User.update(current_mail_authorised="1").where(User.user_id == user_id).execute()

    def get_actions(self):
        query = Action.select().where(Action.time < datetime.now() - timedelta(minutes=DEADLINE_TIME))
        res = []
        for it in query:
            user_query = User.select().where((it.user_id == User.user_id) & (User.current_mail_authorised == "0"))
            if len(user_query) > 0:
                for user in user_query:
                    res.append(user)
                    Action.delete().where(Action.user_id == res[-1].user_id).execute()
            User.delete().where((it.user_id == User.user_id) & (User.current_mail_authorised == "0")).execute()
        return res

    def success_mail(self, mail, user_id):
        User.update(current_mail_authorised="1").where((User.user_id == user_id) &
                                                       (User.current_user_mail == mail) &
                                                       (User.current_mail_authorised == "0")).execute()
        return User.select().where((User.user_id == user_id) &
                                   (User.current_user_mail == mail) &
                                   (User.current_mail_authorised == "1"))

    def fail_mail(self, mail):
        return User.select().where((User.current_user_mail == mail) & (User.current_mail_authorised == "0"))
