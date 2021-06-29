from telethon.sync import TelegramClient
from telethon import events
import json
import re
import time
import random

with open("bad_words.txt", 'r', encoding='utf8') as file:
    bad_words = file.read().split("\n")

with open("good_words.txt", 'r', encoding='utf8') as file:
    good_words = file.read().split("\n")

with open("change.txt", 'r', encoding='utf8') as file:
    all_list = file.read().split("\n")
    to_change = []
    for set_change in all_list:
        to_change.append(set_change.split(" - "))

print(good_words)

with open("setting.json", 'r', encoding='utf8') as out:
    setting = json.load(out)

    client = TelegramClient(
        setting['account']['session'],
        setting['account']['api_id'],
        setting['account']['api_hash']
    )

    client.start()

dialogs = client.get_dialogs()

for index, dialog in enumerate(dialogs):
    print(f'[{index}] {dialog.name}')

channels_len = int(input("Введите количество каналов для парсинга: "))
channels = []

for _ in range(channels_len):
    channels.append(dialogs[int(input("Введите номер канала для парсинга: "))])


my_channels_len = int(input("Введите количество каналов для перессылки: "))
my_channels = []

for _ in range(my_channels_len):
    my_channels.append(dialogs[int(input("Введите номер канала для перессылки: "))])


@client.on(events.NewMessage(chats=channels))
async def handler_first(event):
    print("New message")
    for word in bad_words:
        if word in event.message.text:
            print(f"Bad word is {word}")
            return

    print("No bad words")
    good_words_counter = 0
    for word in good_words:
        if word in event.message.text:
            print("+1")
            good_words_counter += 1
    print(good_words_counter)
    if good_words_counter == 0:
        return

    for set_change in to_change:
        if set_change[0] in event.message.text:
            print(set_change[1])
            event.message.text = event.message.text.replace(set_change[0], set_change[1])
            print(event.message.text)

    for channel in my_channels:

        await client.send_message(channel, event.message)
    print("Complete!")

client.run_until_disconnected()
