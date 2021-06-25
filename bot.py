import logging
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup as repMark, KeyboardButton as repBtn
from pyrogram.raw import functions, types
from jedis import Jedis
from sample_config import Config
from helper_funcs.step_one import request_tg_code_get_random_hash
from helper_funcs.step_two import login_step_get_stel_cookie
from helper_funcs.step_three import scarp_tg_existing_app
from helper_funcs.step_four import create_new_tg_app
from helper_funcs.helper_steps import parse_to_meaning_ful_text
import phonenumbers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

api_hash, api_id, TOKEN = Config.BOT_API_HASH, Config.BOT_API_ID, \
                          Config.TG_BOT_TOKEN

app = Client("idScraperBot", api_id, api_hash, bot_token=TOKEN)

j = Jedis("scraperUsersData.json")

userStats = {}
with app:
    app.send(
        functions.bots.SetBotCommands(
            commands=[
                types.BotCommand(
                    command="start",
                    description="Start Bot"
                ),
                types.BotCommand(
                    command="cancel",
                    description="Cancel the current process"
                ),
            ]
        )
    )


@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    if str(message.from_user.id) not in j.keys():
        j.dset(str(message.from_user.id), mapping={"lang": "FA"})
        await message.reply_text(Config.START_TEXT_FA.replace("{mention_name}", message.from_user.first_name.strip()),
                                 True, "html",
                                 reply_markup=repMark(
                                     [[repBtn(
                                         f" تغییر زبان {'🇮🇷' if j.dget(str(message.from_user.id), 'lang') == 'FA' else '🇺🇸'} Change Language")],
                                         [repBtn(
                                             f"{'ارسال شماره تلفن 📱' if j.dget(str(message.from_user.id), 'lang') == 'FA' else 'Send Phone number 📱'}",
                                             True)]
                                     ], True, False, False))
    else:
        if j.dget(str(message.from_user.id), 'lang') == "FA":
            await message.reply_text(
                Config.START_TEXT_FA.replace("{mention_name}", message.from_user.first_name.strip()), True,
                "html", reply_markup=repMark(
                    [[repBtn(
                        f" تغییر زبان {'🇮🇷' if j.dget(str(message.from_user.id), 'lang') == 'FA' else '🇺🇸'} Change Language")],
                        [repBtn(
                            f"{'ارسال شماره تلفن 📱' if j.dget(str(message.from_user.id), 'lang') == 'FA' else 'Send Phone number 📱'}",
                            True)]
                    ], True, False, False))
        elif j.dget(str(message.from_user.id), 'lang') == "EN":
            await message.reply_text(
                Config.START_TEXT_EN.replace("{mention_name}", message.from_user.first_name.strip()),
                True,
                "html", reply_markup=repMark(
                    [[repBtn(
                        f" تغییر زبان {'🇮🇷' if j.dget(str(message.from_user.id), 'lang') == 'FA' else '🇺🇸'} Change Language")],
                        [repBtn(
                            f"{'ارسال شماره تلفن 📱' if j.dget(str(message.from_user.id), 'lang') == 'FA' else 'Send Phone number 📱'}",
                            True)]
                    ], True, False, False))
        if j.dexists(str(message.from_user.id), "phone_number"):
            j.ddel(str(message.from_user.id), "phone_number")
        if j.dexists(str(message.from_user.id), "random_hash"):
            j.ddel(str(message.from_user.id), "random_hash")
        try:
            del userStats[str(message.from_user.id)]
        except KeyError:
            pass


@app.on_message(filters.regex("تغییر زبان 🇮🇷 Change Language|تغییر زبان 🇺🇸 Change Language") & filters.private)
async def changeLang(_, message: Message):
    if str(message.from_user.id) in j.keys():
        if j.dget(str(message.from_user.id), 'lang') == "FA":
            j.dset(str(message.from_user.id), 'lang', "EN")
            await message.reply_text("Language set to English ✅", reply_markup=repMark(
                [[repBtn(
                    f" تغییر زبان {'🇮🇷' if j.dget(str(message.from_user.id), 'lang') == 'FA' else '🇺🇸'} Change Language")],
                    [repBtn(
                        f"{'ارسال شماره تلفن 📱' if j.dget(str(message.from_user.id), 'lang') == 'FA' else 'Send Phone number 📱'}",
                        True)]
                ], True, False, False))
        elif j.dget(str(message.from_user.id), 'lang') == "EN":
            j.dset(str(message.from_user.id), 'lang', "FA")
            await message.reply_text("زبان روی فارسی تنظیم شد ✅", reply_markup=repMark(
                [[repBtn(
                    f" تغییر زبان {'🇮🇷' if j.dget(str(message.from_user.id), 'lang') == 'FA' else '🇺🇸'} Change Language")],
                    [repBtn(
                        f"{'ارسال شماره تلفن 📱' if j.dget(str(message.from_user.id), 'lang') == 'FA' else 'Send Phone number 📱'}",
                        True)]
                ], True, False, False))


@app.on_message((filters.regex("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$") | filters.contact) & filters.private)
async def getNumber(_, message: Message):
    try:
        userStats[message.from_user.id]
    except KeyError:
        if message.contact:
            message.text = message.contact.phone_number
        if len(message.text) > 4:
            try:
                phonenumbers.parse(message.text)
            except:
                if j.dget(str(message.from_user.id), 'lang') == "FA":
                    await message.reply_text("<b>شماره وارد شده نامعتبر است ❌</b>", True, "html")
                else:
                    await message.reply_text("<b>The entered phone number is invalid ❌</b>", True, "html")
            if phonenumbers.is_possible_number(phonenumbers.parse(str(message.text))) or phonenumbers.is_valid_number(
                    phonenumbers.parse(str(message.text))):

                if j.dget(str(message.from_user.id), 'lang') == "FA":
                    __msgCode = await message.reply_text("♻️ در حال ارسال کد ♻️", True)
                else:
                    __msgCode = await message.reply_text("♻️ Sending Code ♻️")
                isRequestOk, random_hash = request_tg_code_get_random_hash(message.text)
                if isRequestOk:
                    userStats[str(message.from_user.id)] = "giveCode"
                    j.dset(str(message.from_user.id), mapping={"random_hash": random_hash["random_hash"]})
                    j.dset(str(message.from_user.id), mapping={"phone_number": message.text})
                    if j.dget(str(message.from_user.id), 'lang') == "FA":
                        await __msgCode.edit_text(Config.AFTER_RECVD_CODE_TEXT_FA, "html")
                    else:
                        await __msgCode.edit_text(Config.AFTER_RECVD_CODE_TEXT_EN, "html")
                else:
                    if random_hash == 'Sorry, too many tries. Please try again later.':
                        if j.dget(str(message.from_user.id), 'lang') == "FA":
                            await __msgCode.edit_text('درخواست با مشکل مواجه شد ❌\n\n'
                                                      'این خطا می تواند به دلیل یکی از موارد زیر باشد:\n'
                                                      '➖ شماره وارد شده اشتباه بوده\n'
                                                      '➖ بیش از حد تلاش کرده اید'
                                                      '\n⁤')
                        else:
                            await __msgCode.edit_text('Your request has encountered a problem ❌\n\n'
                                                      'This error could be due to one of the following:\n'
                                                      '➖ The number entered was incorrect\n'
                                                      '➖ Too many tries'
                                                      '\n⁤')
                    # Send error to log channel
                    else:
                        await app.send_message(Config.LOG_CHANNEL_ID, f"<code>Error from telegram code request</code>\n"
                                                                      f"<b>Error</b>: <code>{random_hash}</code>\n"
                                                                      f"User: <a href='tg://user?id={message.from_user.id}'>"
                                                                      f"{message.from_user.id}</a>", "html")
                        if j.dget(str(message.from_user.id), 'lang') == "FA":
                            await __msgCode.edit_text('درخواست با مشکل مواجه شد ❌\n\n'
                                                      'این خطا می تواند به دلیل یکی از موارد زیر باشد:\n'
                                                      '➖ شماره وارد شده اشتباه بوده\n'
                                                      '➖ بیش از حد تلاش کرده اید')
                        else:
                            await __msgCode.edit_text('Your request has encountered a problem ❌\n\n'
                                                      'This error could be due to one of the following:\n'
                                                      '➖ The number entered was incorrect\n'
                                                      '➖ Too many tries')  # #
            else:
                if j.dget(str(message.from_user.id), 'lang') == "FA":
                    await message.reply_text("<b>شماره وارد شده نامعتبر است ❌</b>", True, "html")
                else:
                    await message.reply_text("<b>The entered phone number is invalid ❌</b>", True, "html")


@app.on_message(filters.command("cancel") & filters.private)
async def cancel(_, message: Message):
    try:
        userStats[str(message.from_user.id)]
        if j.dexists(str(message.from_user.id), "phone_number"):
            j.ddel(str(message.from_user.id), "phone_number")
        if j.dexists(str(message.from_user.id), "random_hash"):
            j.ddel(str(message.from_user.id), "random_hash")
        try:
            del userStats[str(message.from_user.id)]
        except KeyError:
            pass
        if j.dget(str(message.from_user.id), 'lang') == "FA":
            await message.reply_text("<b>کنسل شد ✅</b>", True, "html")
        else:
            await message.reply_text("<b>Canceled ✅</b>", True, "html")
    except KeyError:
        pass


@app.on_message(filters.text & filters.private)
async def messagesGet(_, message: Message):
    try:
        if userStats[str(message.from_user.id)] == "giveCode":
            if j.dget(str(message.from_user.id), 'lang') == "FA":
                __msgCode = await message.reply_text(
                    "<b>♻️ کد دریافت شد. در حال دریافت <code>Api id</code> و <code>Api hash</code> ♻️ </b>"
                    , True, "html")
            else:
                __msgCode = await message.reply_text(
                    "<b>♻️ Code received. Receiving <code>Api Id</code> & <code>Api hash</code> ♻️</b>"
                    , True, "html")
            status_r, cookie_v = login_step_get_stel_cookie(
                j.dget(str(message.from_user.id), "phone_number"),
                j.dget(str(message.from_user.id), "random_hash"),
                message.text
            )
            if status_r:
                # scrap the my.telegram.org/apps page
                # and check if the user had previously created an app
                status_t, response_dv = scarp_tg_existing_app(cookie_v)
                if not status_t:
                    # if not created
                    # create an app by the provided details
                    create_new_tg_app(
                        cookie_v,
                        response_dv.get("tg_app_hash"),
                        Config.APP_TITLE,
                        Config.APP_SHORT_NAME,
                        Config.APP_URL,
                        Config.APP_PLATFORM,
                        Config.APP_DESCRIPTION
                    )
                # now scrap the my.telegram.org/apps page
                # it is guranteed that now the user will have an APP ID.
                # if not, the stars have failed us
                # and throw that error back to the user
                status_t, response_dv = scarp_tg_existing_app(cookie_v)
                if status_t:
                    # parse the scrapped page into an user readable
                    # message
                    me_t = parse_to_meaning_ful_text(
                        j.dget(str(message.from_user.id), "phone_number"),
                        response_dv
                    )
                    me_t += "\n"
                    me_t += "\n"
                    # add channel ads at the bottom, because why not?
                    me_t += Config.FOOTER_TEXT
                    # and send to the user
                    await __msgCode.edit_text(
                        text=me_t,
                        parse_mode="html"
                    )
                else:
                    if j.dget(str(message.from_user.id), 'lang') == "FA":
                        await __msgCode.edit_text(Config.ERRED_PAGE_FA)
                    else:
                        await __msgCode.edit_text(Config.ERRED_PAGE_EN)
            else:
                # return the Telegram error message to user,
                # incase of incorrect LogIn
                await __msgCode.edit_text(cookie_v)
            if j.dexists(str(message.from_user.id), "phone_number"):
                j.ddel(str(message.from_user.id), "phone_number")
            if j.dexists(str(message.from_user.id), "random_hash"):
                j.ddel(str(message.from_user.id), "random_hash")
            try:
                del userStats[str(message.from_user.id)]
            except KeyError:
                pass

    except KeyError:
        pass


app.run()
