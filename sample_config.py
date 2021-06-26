import os


class Config:
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
    TG_BOT_USER = os.environ.get("TG_BOT_USERNAME")
    LOG_CHANNEL_ID = os.environ.get("LOG_CHANNEL_ID")
    BOT_API_ID = os.environ.get("BOT_API_ID")
    BOT_API_HASH = os.environ.get("BOT_API_HASH")
    # MyTelegram.org
    # configurtion required while creating new application
    APP_TITLE = os.environ.get("APP_TITLE", "Tg Scraper Id")
    APP_SHORT_NAME = os.environ.get("APP_SHORT_NAME", "Tg Scraper Id")
    APP_URL = os.environ.get("APP_URL", "https://t.me")
    # these platform informations were obtained
    APP_PLATFORM = [
        "android",
        "ios",
        "wp",
        "bb",
        "desktop",
        "web",
        "ubp",
        "other"
    ]
    APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", f"created using https:https://telegram.dog/{TG_BOT_USER}")
    #
    FOOTER_TEXT = os.environ.get("FTEXT", "Managed With ❤️ By @Kobsser")
    # the strings used in the different messages
    # in the bot
    START_TEXT_FA = ("سلام {mention_name} 👋\n\n"
                     "اگه میخوای Api ID و Api Hash تلگرام رو خیلی سریع دریافت کنی، من میتونم کمکت کنم\n"
                     "لطفا شماره تلفن تلگرامت رو بفرست\n"
                     "در ضمن، میتونی خیلی راحت تر از دکمه ارسال شماره استفاده کنی\n"
                     "حواست باشه که شماره رو با این فرمت بفرستی:\n"
                     "\u200E+(<code>شماره تلفن</code>) (<code>کد کشور</code>)\n"
                     "مثلا:\n"
                     "    <i>+989901234567</i>")
    START_TEXT_EN = ("Hi {mention_name} 👋\n\n"
                     "If you want to find an API ID & API HASH Telegram, here, I can help, which is certainly simple.\n"
                     "Please enter the Telegram Telephone Number, with this format :\n"
                     "+(<code>country code</code>) (<code>number</code>)\n"
                     "for example:  +10123456789\n"
                     "You can use the 'send phone number' Button as easier"
                     )
    AFTER_RECVD_CODE_TEXT_EN = ("✅ Code Sent to you\n"
                                "Now Send me the code you received from telegram ...\n"
                                "This code is only used for the purpose of getting APP ID from my.telegram.org\n"
                                "if you don't trust this bot, just take it manually ⚡️"
                                "\n<code>Use </code>/cancel<code> to cancel the operation</code>")
    AFTER_RECVD_CODE_TEXT_FA = ("✅ کد برات فرستاده شد"
                                "حالا کدی که از طرف تلگرام برات ارسال شده رو برام بفرست ...\n"
                                "این کد فقط به منظور دریافت APP Id از my.telegram.org استفاده میشه\n"
                                "اگه به این ربات اعتماد ندارید، خب میتونید دستی انجامش بدید ⚡️ \n"
                                "<code>برای لغو از دستور</code> /cancel <code>استفاده کنید</code>")
    BEFORE_SUCC_LOGIN_EN = ("Code Received ✅\n"
                            "Scrapping API Id & Hash ...")
    BEFORE_SUCC_LOGIN_FA = ("کد دریافت شد ✅\n"
                            "در حال دریافت API Id و Api Hash ...")

    ERRED_PAGE_EN = "Failed to get app id ❌"
    ERRED_PAGE_FA = "دریافت app id با مشکل مواجه شد ❌"

    CANCELLED_MESG_EN = "Bye! Please /start again if you want to get Api id & Hash later"
    CANCELLED_MESG_FA = "کنسل شد! اگه بعدا خواستی دوباره از ربات استفاده کنی /start رو بزن"
    IN_VALID_CODE_PVDED_EN = "Invalid Code ❌\nPlease send me code you received from telegram!\nThat is really stupid!!"
    IN_VALID_CODE_PVDED_FA = "کدی که فرستادید اشتباهه ❌\n\nدوباره سعی کنید!"
    IN_VALID_PHNO_PVDED_EN = """Invalid Phone number ❌\nPlease send a correct Telegram Phone number!\n\nuse this format:
    """ "+(```country code```) (```number```)\nfor example:  +10123456789"
    IN_VALID_PHNO_PVDED_FA = "شماره تلفنی که فرستادید اشتباهه ❌\nلطفا یک شماره تلفن درست وارد کنید!\n\nشماره باید با این فرمت وارد بشه:\n \n"
    "    +(```کد کشور```) (```شماره تلفن```)\n"
    "    مثلا:\n"
    "    +989901234567"
