import configparser
import json
import os

from telethon.sync import TelegramClient

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
username = os.getenv("USERNAME")

client = TelegramClient(username, api_id, api_hash)

client.start()


async def dump_all_participants(chat):
    offset_user = 0
    limit_user = 500

    all_participants = []
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(chat, filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)

    all_users_details = []

    for participant in all_participants:
        if not participant.bot:
            all_users_details.append({"chat_id": chat.id,
                                      "user_id": participant.id,
                                      "current_username": participant.username,
                                      "current_first_name": participant.first_name,
                                      "current_last_name": participant.last_name})

    with open('users.json', 'w', encoding='utf8') as outfile:
        json.dump(all_users_details, outfile, ensure_ascii=False)


async def main():
    url = input("Введите ссылку или id: ")
    try:
        url = int(url)
    except BaseException:
        pass
    chat = await client.get_entity(url)
    await dump_all_participants(chat)


with client:
    client.loop.run_until_complete(main())
