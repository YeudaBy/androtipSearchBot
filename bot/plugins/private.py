# Handling commands in PM with the bot

from pyrogram import Client, filters
from pyrogram.types import (Message,
                            InlineKeyboardButton,
                            InlineKeyboardMarkup)
from ..helper import json_dump, json_load
from ..MSG import MSG

users_file = 'bot/db/users.json'  # db file for users

# lambda func for chack if the command is only "start" or mai be mor.
only_start = lambda _, __, m: True if m.text == "/start" else False


@Client.on_message(filters.private & filters.command("start")
                   & filters.create(only_start))
# reply msg start for first chat with user.
# use with command "start"
def start_msg(_client: Client, message: Message):
    message.reply(MSG["start"].format(
        f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"),
        disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("לחיפוש ברובוט 🔎", switch_inline_query_current_chat='')],
             [InlineKeyboardButton("לערוץ עדכוני רובוטים 🦾", url="t.me/m100achuzBots")]]))

    # Saves the user to a database
    users_db: list = json_load(users_file)
    if message.from_user.id not in users_db:
        users_db.append(message.from_user.id)
        json_dump(users_db, users_file)


@Client.on_message(filters.private & filters.command(["start", "help"])
                   & ~filters.create(only_start))
# msg of links and about
def post_msg(_, message: Message):
    message.reply(MSG["post"], disable_web_page_preview=True)
