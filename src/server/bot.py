import logging
import telebot
import json
from base64 import b64encode
from src.common.settings import TG_BOT_TOKEN
from src.common.utils import gen_authorize_url

TG_BASE_URL = f'https://api.telegram.org/bot{TG_BOT_TOKEN}'


class TelegramBot(telebot.TeleBot):
    server = None  # server_dir.Server
    storage = None  # models.StorageManager
    setuper = None

    def set_server(self, server):
        self.server = server

    def set_storage(self, storage):
        self.storage = storage

    def set_setuper(self, setuper):
        self.setuper = setuper


bot = TelegramBot(TG_BOT_TOKEN)
logger = logging.getLogger('bot')
logger.setLevel(logging.ERROR)


@bot.message_handler(commands=['mail'])
def handle_mail(message):
    data = message.text.split()
    bot.storage.add_message(message.message_id, message.chat.id, message.from_user.id)
    user_id = message.from_user.id
    for word in data:
        print(word)
        if word.find("@edu.hse.ru") != -1 or word.find("@hse.ru") != -1:
            temp = bot.storage.update_mail(message, word)
            if temp == 1:
                bot.send_message(message.chat.id, bot.setuper.same_mail(message.from_user.username,
                                                                        message.from_user.first_name,
                                                                        message.from_user.last_name))
            elif temp == 2:
                bot.send_message(message.chat.id, bot.setuper.another_mail(message.from_user.username,
                                                                           message.from_user.first_name,
                                                                           message.from_user.last_name))
            else:
                message = bot.send_message(message.chat.id, bot.setuper.register(message.from_user.username,
                                                                                 message.from_user.first_name,
                                                                                 message.from_user.last_name,
                                                                                 gen_authorize_url(
                                                                                     str(bot.storage.get_uuid(
                                                                                         message.from_user.id)))))
                bot.storage.add_message(message.message_id, message.chat.id, user_id)
            break
    else:
        message = bot.send_message(message.chat.id, bot.setuper.no_mail(message.from_user.username,
                                                                        message.from_user.first_name,
                                                                        message.from_user.last_name))
        bot.storage.add_message(message.message_id, message.chat.id, user_id)


def get_uid_ignore(message):
    try:
        username = message.text.split()[1].replace('@', '')
        user_id = bot.storage.get_user_id(username)
    except BaseException:
        user_id = message.reply_to_message.new_chat_members[0].id
    return user_id


def get_uid_ban(message):
    try:
        username = message.text.split()[1].replace('@', '')
        user_id = bot.storage.get_user_id(username)
    except BaseException:
        user_id = message.reply_to_message.from_user.id
    return user_id


@bot.message_handler(commands=['ignore'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        try:
            user_id = get_uid_ignore(message)
        except BaseException:
            bot.send_message(message.chat.id, bot.setuper.went_wrong(message.from_user.username,
                                                                     message.from_user.first_name,
                                                                     message.from_user.last_name))
            return
        bot.storage.ignore(user_id)
        messages = bot.storage.get_messages(user_id)
        for cur_message in messages:
            bot.delete_message(cur_message.chat_id, cur_message.message_id)
        bot.send_message(message.chat.id, bot.setuper.ignore(message.from_user.username,
                                                             message.from_user.first_name,
                                                             message.from_user.last_name))
    else:
        bot.send_message(message.chat.id, bot.setuper.rignts(message.from_user.username,
                                                             message.from_user.first_name,
                                                             message.from_user.last_name))


@bot.message_handler(commands=['ban'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        try:
            user_id = get_uid_ban(message)
        except BaseException:
            bot.send_message(message.chat.id, bot.setuper.went_wrong(message.from_user.username,
                                                                     message.from_user.first_name,
                                                                     message.from_user.last_name))
            return
        bot.storage.ban(user_id)
        data = bot.storage.get_user_chats(user_id)
        for it in data:
            bot.kick_chat_member(it.chat_id, user_id)
            bot.send_message(it.chat_id, bot.setuper.ban(it.username,
                                                         it.first_name,
                                                         it.last_name))
    else:
        bot.send_message(message.chat.id, bot.setuper.rights(message.from_user.username,
                                                             message.from_user.first_name,
                                                             message.from_user.last_name))


@bot.message_handler(commands=['unban'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        try:
            user_id = get_uid_ban(message)
        except BaseException:
            bot.send_message(message.chat.id, bot.setuper.went_wrong(message.from_user.username,
                                                                     message.from_user.first_name,
                                                                     message.from_user.last_name))
            return
        bot.storage.unban(user_id)
        data = bot.storage.get_user_chats(user_id)
        for it in data:
            bot.send_message(it.chat_id, bot.setuper.unban(it.username,
                                                           it.first_name,
                                                           it.last_name))
    else:
        bot.send_message(message.chat.id, bot.setuper.rights(message.from_user.username,
                                                             message.from_user.first_name,
                                                             message.from_user.last_name))


@bot.message_handler(content_types='new_chat_members')
def handle_new_chat_members(message):
    temp = []
    for user in message.new_chat_members:
        if user.is_bot:
            logger.info('User %s is bot, skipping', message.from_user)
            continue
        temp.append(user)
    if len(temp) > 0:
        if bot.storage.check_ban(temp[0].id):
            bot.kick_chat_member(message.chat.id, temp[0].id)
            bot.send_message(message.chat.id, bot.setuper.banned(temp[0].username,
                                                                 temp[0].first_name,
                                                                 temp[0].last_name))
            return
    users = bot.storage.register_new_chat_members(message)
    if len(users) > 0:
        message = bot.send_message(message.chat.id, bot.setuper.greetings(users[0].current_username,
                                                                          users[0].current_first_name,
                                                                          users[0].current_last_name))
        bot.storage.add_message(message.message_id, message.chat.id, users[0].user_id)


@bot.message_handler(commands=['check'])
def check(core_message):
    try:
        message = core_message.reply_to_message
        if bot.storage.check_ban(message.from_user.id):
            bot.kick_chat_member(message.chat.id, message.from_user.id)
            bot.send_message(message.chat.id, bot.setuper.banned(message.from_user.username,
                                                                 message.from_user.first_name,
                                                                 message.from_user.last_name))
            return
        if bot.storage.check_member(message):
            if bot.storage.register_old_chat_member(message):
                user = message.from_user
                message = bot.send_message(message.chat.id, bot.setuper.check(message.from_user.username,
                                                                              message.from_user.first_name,
                                                                              message.from_user.last_name))
                bot.storage.add_message(message.message_id, message.chat.id, user.id)
    except BaseException:
        message = core_message
        bot.send_message(message.chat.id, bot.setuper.went_wrong(message.from_user.username,
                                                                 message.from_user.first_name,
                                                                 message.from_user.last_name))


@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if bot.setuper.switch():
        if bot.storage.check_reg(message):
            bot.delete_message(message.chat.id, message.message_id)
        if bot.storage.check_ban(message.from_user.id):
            bot.kick_chat_member(message.chat.id, message.from_user.id)
            bot.send_message(message.chat.id, bot.setuper.banned(message.from_user.username,
                                                                 message.from_user.first_name,
                                                                 message.from_user.last_name))
            return
        if bot.storage.check_member(message):
            if bot.storage.register_old_chat_member(message):
                user = message.from_user
                message = bot.send_message(message.chat.id, bot.setuper.check(message.from_user.username,
                                                                              message.from_user.first_name,
                                                                              message.from_user.last_name))
                bot.storage.add_message(message.message_id, message.chat.id, user.id)


def ms_ans(mail, uuid):
    user_id = bot.storage.get_uid_by_uuid(uuid)
    if bot.storage.check_mail(mail, uuid):
        user = bot.storage.success_mail(mail, user_id)
        for it in user:
            bot.send_message(it.chat_id, bot.setuper.oauth_good(it.current_username,
                                                                it.current_first_name,
                                                                it.current_last_name))
        messages = bot.storage.get_messages(user_id)
        for message in messages:
            bot.delete_message(message.chat_id, message.message_id)
    else:
        user = bot.storage.fail_mail(uuid)
        for it in user:
            message = bot.send_message(it.chat_id, bot.setuper.oauth_bad(it.current_username,
                                                                         it.current_first_name,
                                                                         it.current_last_name))
            bot.storage.add_message(message.message_id, message.chat.id, user_id)


def deadline_kick():
    for_kick = bot.storage.get_actions(bot.setuper.int_deadline())
    for it in for_kick:
        bot.send_message(it.chat_id, bot.setuper.kick(it.current_username,
                                                      it.current_first_name,
                                                      it.current_last_name))
        messages = bot.storage.get_messages(it.user_id)
        for message in messages:
            bot.delete_message(message.chat_id, message.message_id)
        bot.kick_chat_member(it.chat_id, it.user_id)
