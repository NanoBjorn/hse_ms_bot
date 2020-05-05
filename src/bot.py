import logging

import telebot

from models import StorageManager
from server import Server
from settings import TG_BOT_TOKEN

TG_BASE_URL = f'https://api.telegram.org/bot{TG_BOT_TOKEN}'


class TelegramBot(telebot.TeleBot):
    server: Server = None
    storage: StorageManager = None

    def set_server(self, server: Server):
        self.server = server

    def set_storage(self, storage: StorageManager):
        self.storage = storage


bot = TelegramBot(TG_BOT_TOKEN)

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)


@bot.message_handler(func=lambda m: True)
def handle_all(message):
    logger.debug(message)


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
    logger.debug(message)
    users = bot.storage.register_new_chat_members(message)
    if len(users) > 0:
        bot.send_message(message.chat.id, f'@{users[0].current_username}, добро пожаловать!')
