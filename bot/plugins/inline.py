from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite3 import ProgrammingError
from ..MSG import MSG


photo_url = "https://telegra.ph/file/a2ca683386e152c2701b7.jpg"
# link-photo for tumb

usr = Client('bot/config/usr', config_file='bot/config/usr.ini')
# create instance Client for the user-bot


@Client.on_inline_query(filters.regex(r"\$"))
# share the bot
def share(_, inline: InlineQuery):
    """
    inline answer for share the bot.
    :param _: Client
    :param inline: InlineQuery
    :return: Inline Result for share
    """
    inline.answer([InlineQueryResultArticle(
        "לחץ כאן לשיתוף הרובוט לחברים 😍",
        InputTextMessageContent(MSG["share"])
    )])


@Client.on_inline_query(~filters.regex(r"\$"))
# search post on the channel
async def inline_mode(_, inline: InlineQuery):
    """
    the main func.
    We get a query from the user, searcing in the channel,
    and return list Inline Results of post from channel.
    :param _: Client
    :param inline: InlineQuery
    :return: list Inline Results
    """

    # ----- start the user Client --------
    try:
        await usr.start()  # starting the user for the search

    except ConnectionError:
        pass
    except OSError:
        pass
    except ProgrammingError:
        await usr.stop()
        await usr.start()

    # ------- search for results --------
    posts_match = []
    try:
        async for post in usr.search_messages('AndroidTipsIL', query=inline.query, limit=15):
            # searcing the query in channel.
            if post.web_page and post.web_page.title:
                posts_match.append(post)  # adding iter to the list
    except OSError:
        pass
    except ProgrammingError:
        pass

    # ------ return none results --------
    if len(posts_match) == 0:
        # Handle in case there are no results
        await inline.answer(
            results=[InlineQueryResultArticle(
                title="לא נמצאו תוצאות! ☹️",
                input_message_content=InputTextMessageContent(
                    message_text='מחפשים מידע על נושא שעדיין אין עליו מדריך?\n\nיותר מנשמח לשמוע על מה מדובר, '
                                 'ואולי בחיפוש הבא שלכם כבר תמצאו מדריך מוכן על הנושא 🤪',
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        "להצעת מדריכים 👀", url="t.me/AndroTipsBot")
                    ]])
            )],
            switch_pm_text="אודות אנדרוטיפס 💡", switch_pm_parameter="about"
        )

    # ------ return the results --------
    else:
        rez = []
        for post_result in posts_match:
            # Create a list of results
            rez.append(
                InlineQueryResultArticle(
                    title= post_result.web_page.title,
                    description= f'ע"י {post_result.web_page.author}, צפיות: {post_result.views}\n{post_result.web_page.description}',
                    reply_markup= InlineKeyboardMarkup([
                        [InlineKeyboardButton("לשיתוף הפוסט ♻️", url="https://t.me/share/url?url="
                                                                     + post_result.web_page.url)],
                        [InlineKeyboardButton("לחיפוש ברובוט 🔎", switch_inline_query_current_chat=''),
                         InlineKeyboardButton("לשיתוף הרובוט 🤖", switch_inline_query="$share")],
                        [InlineKeyboardButton("למעבר לפוסט 💬", url=post_result.link)]
                    ]),
                    input_message_content= InputTextMessageContent(
                        f'**{post_result.web_page.title}**\nע"י {post_result.web_page.author}\n\n{post_result.web_page.url}',
                        ),
                    thumb_url= photo_url))

        # Return the results
        await inline.answer(results= rez,
                            switch_pm_text="אודות אנדרוטיפס 💡", switch_pm_parameter="about")

    # ----- stop the user -------
    try:
        await usr.stop()
    except ConnectionError:
        return
