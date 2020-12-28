# Search bot for articles from the Androtips channel
# Created by YeudaBy t.me/m100achuz
# https://github.com/M100achuz2/androtipSearchBot

from pyrogram import Client

if __name__ == '__main__':
    Client("bot/config/androtipSearch",
           config_file='bot/config/config.ini').run()
