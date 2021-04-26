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
            print(word)
            temp = bot.storage.update_mail(message, word)
            if temp == 1:
                bot.send_message(message.chat.id,
                                 f'@{message.from_user.username}, кто-то уже использует эту почту')
                # bot.kick_chat_member(message.chat.id, message.from_user.id)
            elif temp == 2:
                bot.send_message(message.chat.id,
                                 f'@{message.from_user.username}, я не могу этого сделать')
            else:
                state = b64encode(
                    json.dumps({'mail': word, 'user_id': message.from_user.id, 'chat_id': message.chat.id}).encode('ascii'))
                message = bot.send_message(message.chat.id,
                                           f'@{message.from_user.username}, теперь нам нужно проверить твою почту: {gen_authorize_url(str(state, "ascii"))}')
                bot.storage.add_message(message.message_id, message.chat.id, user_id)
                break
    else:
        message = bot.send_message(message.chat.id, "Попробуй еще раз")
        bot.storage.add_message(message.message_id, message.chat.id, user_id)


@bot.message_handler(commands=['ignore'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        username = message.text.split()[1].replace('@', '')
        try:
            user_id = bot.storage.get_user_id(username)
        except BaseException:
            bot.send_message(message.chat.id, 'Что-то пошло не так')
            return
        bot.storage.ignore(user_id)
        messages = bot.storage.get_messages(user_id)
        for cur_message in messages:
            bot.delete_message(cur_message.chat_id, cur_message.message_id)
        bot.send_message(message.chat.id, f'@{username} зарегистрирован')
    else:
        bot.send_message(message.chat.id, f'@{message.from_user.username} не является администратором')


@bot.message_handler(commands=['ban'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        username = message.text.split()[1].replace('@', '')
        try:
            user_id = bot.storage.get_user_id(username)
        except BaseException:
            bot.send_message(message.chat.id, 'Что-то пошло не так.')
            return
        bot.storage.ban(user_id)
        data = bot.storage.get_user_chats(user_id)
        for it in data:
            bot.kick_chat_member(it.chat_id, user_id)
            bot.send_message(it.chat_id, f'@{it.current_username} в бане')
    else:
        bot.send_message(message.chat.id, f'@{message.from_user.username} не является администратором')

@bot.message_handler(commands=['unban'])
def handle_mail(message):
    role = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if role == 'administrator' or role == 'creator':
        username = message.text.split()[1].replace('@', '')
        try:
            user_id = bot.storage.get_user_id(username)
        except BaseException:
            bot.send_message(message.chat.id, 'Что-то пошло не так.')
            return
        bot.storage.unban(user_id)
        data = bot.storage.get_user_chats(user_id)
        for it in data:
            bot.send_message(it.chat_id, f'@{it.current_username} разбанен(а)')
    else:
        bot.send_message(message.chat.id, f'@{message.from_user.username} не является администратором')

@bot.message_handler(content_types='new_chat_members')
def handle_new_chat_members(message):
    """
    Example:
    {
      "content_type": "new_chat_members",
      "message_id": 118,
      "from_user": {
        "id": 797686828,
        "is_bot": false,
        "first_name": "Gleb",
        "username": "ganovikov",
        "last_name": "Novikov",
        "language_code": null
      },
      "date": 1588538411,
      "chat": {
        "type": "supergroup",
        "last_name": null,
        "first_name": null,
        "username": null,
        "id": -1001439152964,
        "title": "тест вахтера",
        "all_members_are_administrators": null,
        "photo": null,
        "description": null,
        "invite_link": null,
        "pinned_message": null,
        "sticker_set_name": null,
        "can_set_sticker_set": null
      },
      "forward_from": null,
      "forward_from_chat": null,
      "forward_from_message_id": null,
      "forward_signature": null,
      "forward_date": null,
      "reply_to_message": null,
      "edit_date": null,
      "media_group_id": null,
      "author_signature": null,
      "text": null,
      "entities": null,
      "caption_entities": null,
      "audio": null,
      "document": null,
      "photo": null,
      "sticker": null,
      "video": null,
      "video_note": null,
      "voice": null,
      "caption": null,
      "contact": null,
      "location": null,
      "venue": null,
      "animation": null,
      "dice": null,
      "new_chat_member": null,
      "new_chat_members": [
        "<telebot.types.User object at 0x10721f748>"
      ],
      "left_chat_member": null,
      "new_chat_title": null,
      "new_chat_photo": null,
      "delete_chat_photo": null,
      "group_chat_created": null,
      "supergroup_chat_created": null,
      "channel_chat_created": null,
      "migrate_to_chat_id": null,
      "migrate_from_chat_id": null,
      "pinned_message": null,
      "invoice": null,
      "successful_payment": null,
      "connected_website": null,
      "json": {
        "message_id": 118,
        "from": {
          "id": 797686828,
          "is_bot": false,
          "first_name": "Gleb",
          "last_name": "Novikov",
          "username": "ganovikov"
        },
        "chat": {
          "id": -1001439152964,
          "title": "тест вахтера",
          "type": "supergroup"
        },
        "date": 1588538411,
        "new_chat_participant": {
          "id": 797686828,
          "is_bot": false,
          "first_name": "Gleb",
          "last_name": "Novikov",
          "username": "ganovikov"
        },
        "new_chat_member": {
          "id": 797686828,
          "is_bot": false,
          "first_name": "Gleb",
          "last_name": "Novikov",
          "username": "ganovikov"
        },
        "new_chat_members": [
          {
            "id": 797686828,
            "is_bot": false,
            "first_name": "Gleb",
            "last_name": "Novikov",
            "username": "ganovikov"
          }
        ]
      }
    }
    """
    temp = []
    for user in message.new_chat_members:
        if user.is_bot:
            logger.info('User %s is bot, skipping', message.from_user)
            continue
        temp.append(user)
    if len(temp) > 0:
        if bot.storage.check_ban(temp[0].id):
            bot.kick_chat_member(message.chat.id, temp[0].id)
            bot.send_message(message.chat.id, f'@{temp[0].username} в бане')
            return
    users = bot.storage.register_new_chat_members(message)
    if len(users) > 0:
        message = bot.send_message(message.chat.id,
                                   f'@{users[0].current_username}, добро пожаловать! Отправь свою почту в следующем формате: \" /mail aosushkov@edu.hse.ru\"')
        bot.storage.add_message(message.message_id, message.chat.id, users[0].user_id)


@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if bot.storage.check_ban(message.from_user.id):
        bot.kick_chat_member(message.chat.id, message.from_user.id)
        bot.send_message(message.chat.id, f'@{message.from_user.username} в бане')
        return
    if bot.storage.check_member(message):
        bot.storage.register_old_chat_member(message)
        user = message.from_user
        message = bot.send_message(message.chat.id,
                                   f'@{user.username}, отправь свою почту в следующем формате: \" /mail aosushkov@edu.hse.ru\"')
        bot.storage.add_message(message.message_id, message.chat.id, user.id)


def ms_ans(mail, user_id, chat_id, success):
    if success:
        user = bot.storage.success_mail(mail, user_id)
        # bot.send_message(user[0].chat_id, f'@{user[0].current_username}, регистрация прошла успешно')
        for it in user:
            bot.send_message(it.chat_id, f'@{it.current_username}, регистрация прошла успешно')
        messages = bot.storage.get_messages(user_id)
        for message in messages:
            bot.delete_message(message.chat_id, message.message_id)
    else:
        user = bot.storage.fail_mail(mail)
        print("-")
        for it in user:
            message = bot.send_message(it.chat_id,
                                       f'@{it.current_username}, попробуй еще раз отправь свою почту в формате: \" /mail aosushkov@edu.hse.ru\" и пройди регистрацию еще раз')
            bot.storage.add_message(message.message_id, message.chat.id, user_id)


def deadline_kick():
    for_kick = bot.storage.get_actions()
    for it in for_kick:
        bot.send_message(it.chat_id, f'@{it.current_username} не зарегистрировался, кикаю')
        messages = bot.storage.get_messages(it.user_id)
        for message in messages:
            bot.delete_message(message.chat_id, message.message_id)
        bot.kick_chat_member(it.chat_id, it.user_id)
        bot.storage.kick_user(it.chat_id, it.user_id)
