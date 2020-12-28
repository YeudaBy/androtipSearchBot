from pyrogram import Client

if __name__ == '__main__':
    Client("bot/config/androtipSearch",
           config_file='bot/config/config.ini').run()