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

    def set_server(self, server):
        self.server = server

    def set_storage(self, storage):
        self.storage = storage


bot = TelegramBot(TG_BOT_TOKEN)
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)


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
                bot.send_message(message.chat.id,
                                 f'@{message.from_user.username}, кто-то уже использует эту почту')
            elif temp == 2:
                bot.send_message(message.chat.id,
                                 f'@{message.from_user.username}, ты уже зарегистрирован по другой почте')
            else:
                state = b64encode(
                    json.dumps({'mail': word, 'user_id': message.from_user.id, 'chat_id': message.chat.id}).encode(
                        'ascii'))
                message = bot.send_message(message.chat.id,
                                           f'@{message.from_user.username}, пожалуйста, авторизируйся по рабочей почте: {gen_authorize_url(str(state, "ascii"))}')
                bot.storage.add_message(message.message_id, message.chat.id, user_id)
            break
    else:
        message = bot.send_message(message.chat.id, f'@{message.from_user.username}, не увидел твою почту. отправь свою почту в следующем формате:\" /mail iiivanov@edu.hse.ru\"')
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
            bot.send_message(message.chat.id, 'Что-то пошло не так  ̄\_(ツ)_/ ̄.')
            return
        bot.storage.ignore(user_id)
        messages = bot.storage.get_messages(user_id)
        for cur_message in messages:
            bot.delete_message(cur_message.chat_id, cur_message.message_id)
        bot.send_message(message.chat.id, 'Успешно.')
    else:
        bot.send_message(message.chat.id, f'@{message.from_user.username} не является администратором')


@bot.message_handler(commands=['ban'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        try:
            user_id = get_uid_ban(message)
        except BaseException:
            bot.send_message(message.chat.id, 'Что-то пошло не так ¯\_(ツ)_/¯.')
            return
        bot.storage.ban(user_id)
        data = bot.storage.get_user_chats(user_id)
        for it in data:
            bot.kick_chat_member(it.chat_id, user_id)
            bot.send_message(it.chat_id, 'Пользователь был забанен.')
    else:
        bot.send_message(message.chat.id, f'У @{message.from_user.username} недостаточно прав')


@bot.message_handler(commands=['unban'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        try:
            user_id = get_uid_ban(message)
        except BaseException:
            bot.send_message(message.chat.id, 'Что-то пошло не так')
            return
        bot.storage.unban(user_id)
        data = bot.storage.get_user_chats(user_id)
        for it in data:
            bot.send_message(it.chat_id, 'Пользователь был разбанен.')
    else:
        bot.send_message(message.chat.id, f'У @{message.from_user.username} недостаточно прав.')


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
            bot.send_message(message.chat.id, f'@{temp[0].username} в бане.')
            return
    users = bot.storage.register_new_chat_members(message)
    if len(users) > 0:
        message = bot.send_message(message.chat.id,
                                   f'@{users[0].current_username}, добро пожаловать! Для нахождения в чате необходимо пройти регистрацию. Для начала, отправь свою почту в чат или мне в личные сообщения в следующем формате:\" /mail iiivanov@edu.hse.ru\".')
        bot.storage.add_message(message.message_id, message.chat.id, users[0].user_id)


@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if bot.storage.check_reg(message):
        bot.delete_message(message.chat.id, message.message_id)
    if bot.storage.check_ban(message.from_user.id):
        bot.kick_chat_member(message.chat.id, message.from_user.id)
        bot.send_message(message.chat.id, f'@{message.from_user.username} в бане')
        return
    if bot.storage.check_member(message):
        if bot.storage.register_old_chat_member(message):
            user = message.from_user
            message = bot.send_message(message.chat.id,
                                       f'@{user.username}, отправь свою почту в чат или мне в личные сообщения в следующем формате: \" /mail iiivanov@edu.hse.ru\".')
            bot.storage.add_message(message.message_id, message.chat.id, user.id)


def ms_ans(mail, user_id, chat_id, success):
    if success:
        user = bot.storage.success_mail(mail, user_id)
        for it in user:
            bot.send_message(it.chat_id, f'@{it.current_username}, регистрация прошла успешно.')
        messages = bot.storage.get_messages(user_id)
        for message in messages:
            bot.delete_message(message.chat_id, message.message_id)
    else:
        user = bot.storage.fail_mail(mail)
        print("-")
        for it in user:
            message = bot.send_message(it.chat_id,
                                       f'@{it.current_username}, во время регистрации что-то пошло не так. Еще раз отправь свою почту в формате: \"/mail iiivanov@edu.hse.ru\" и пройди регистрацию.')
            bot.storage.add_message(message.message_id, message.chat.id, user_id)


def deadline_kick():
    for_kick = bot.storage.get_actions()
    for it in for_kick:
        bot.send_message(it.chat_id, f'@{it.current_username} не зарегистрировался.')
        messages = bot.storage.get_messages(it.user_id)
        for message in messages:
            bot.delete_message(message.chat_id, message.message_id)
        bot.kick_chat_member(it.chat_id, it.user_id)
