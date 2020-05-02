import logging

import telebot

from settings import TG_BOT_TOKEN

TG_BASE_URL = f'https://api.telegram.org/bot{TG_BOT_TOKEN}'

bot = telebot.TeleBot(TG_BOT_TOKEN)

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)


@bot.message_handler(func=lambda m: True)
def handle_all(message):
    logger.debug(message)


@bot.message_handler(content_types='new_chat_members')
def handle_new_chat_members(message):
    logger.debug(message)
    bot.reply_to(message, 'Добро пожаловать!')
