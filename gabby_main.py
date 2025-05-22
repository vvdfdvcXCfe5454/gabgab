import re
import sys
import time
from sys import argv, version_info
from os import path
import os
import importlib
from gabby_config import Config

ASSISTANT_TOKEN = Config.ASSISTANT_TOKEN  

from modules.userinfo import get_readable_time
from modules.misc import *  # For future helpers
import subprocess

TOKEN = Config.TOKEN
OWNER_ID = Config.OWNER_ID
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Forbidden,  #
)
from telegram.ext import CallbackContext, filters
from telegram.helpers import escape_markdown
from typing import Optional
from telegram import Chat, User, Message
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler

import logging
import traceback
import html
import json
import asyncio

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("Gabby")


PM_START_TEX = """
Hey there, `{}` 😘\nGabby is getting all dolled up for you... just a sec! 💋
"""

buttons = [
    [
        InlineKeyboardButton(
            text="💖 Add Gabby to your group 💖", url=f"t.me/{Config.OWNER_USERNAME}?startgroup=new"
        ),
    ],
    [
        InlineKeyboardButton(text="💋 Flirty Help 💋", callback_data="help_back"),
        InlineKeyboardButton(text="🔥 Gabby Stats 🔥", callback_data="stats_callback"),
    ],
    [
        InlineKeyboardButton(text="🌹 About Gabby 🌹", callback_data="GABBY_ABOUT"),
        InlineKeyboardButton(
            text="👠 Gabby's Dev 👠", url=f"tg://user?id={Config.OWNER_ID}"
        ),
    ],
]

HELP_STRINGS = f"""
» *Gabby — tap the button below to get all the steamy details about my hottest commands, babe!*"""

DONATE_STRING = f"""Hey baby,
So happy you wanna support me! 💋

You can slide into my developer's DMs to donate, or visit my support chat and ask about donations there. Every little bit helps keep me sexy and online for you! 😘
"""

MODULES_DIR = os.path.join(os.path.dirname(__file__), "gabby_modules")
ALL_MODULES = [
    f[:-3] for f in os.listdir(MODULES_DIR)
    if f.endswith(".py") and not f.startswith("__")
]

IMPORTED = {}
for module_name in ALL_MODULES:
    imported_module = importlib.import_module(f"gabby_modules.{module_name}")
    IMPORTED[module_name] = imported_module

HELPABLE = {}
START_IMG = "https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4"
BOT_NAME = "Gabby"
SUPPORT_CHAT = "GabbySupport"
StartTime = time.time()
def paginate_modules(page, module1, prefix, chat=None):
    return [[InlineKeyboardButton("Module", callback_data=f"{prefix}_module")] for _ in range(3)]

# Load Gabby assistant
# from Gabbybot.module1 import assistant
# assistant.setup(dispatcher)

# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    updater.bot.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["extras"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAI33mLYLNLilbRI-sKAAob0P7koTEJNAAIOBAACl42QVKnra4sdzC_uKQQ")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.3)
            lol.edit_text("💋")
            time.sleep(0.2)
            lol.edit_text("Getting hot for you... 🔥")
            time.sleep(0.2)
            lol.delete()
            update.effective_message.reply_photo(
                START_IMG,
                PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption=f"I'm alive and ready to play, baby! 😘\n<b>I've been up for:</b> <code>{uptime}</code>",
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Forbidden:
        print("Forbidden error (was Unauthorized)")
    except BadRequest:
        print("BadRequest caught")
    except TimedOut:
        print("TimedOut error")
    except NetworkError:
        print("NetworkError")
    except ChatMigrated as err:
        print("ChatMigrated", err)
    except TelegramError:
        print(error)


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                f"» *Hot commands for* *{HELPABLE[module].__mod_name__}* :\n"
                + HELPABLE[module].__help__
            )
            query.message.edit_caption(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back", callback_data="help_back"), InlineKeyboardButton(text="Support", callback_data="babe_support")]]
                ),
            )
        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_caption(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )
        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_caption(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )
        elif back_match:
            query.message.edit_caption(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
    except BadRequest:
        pass


def Babe_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "babe_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_caption(
            f"*Hey hot stuff!* 😘\n  *This is {updater.bot.first_name}*"
            "\n*Your sexy group and music management bot, built to make your chats sizzle and keep the creeps away!*"
            "\n*Written in Python with SQLAlchemy and MongoDB as my secret sauce.*"
            "\n\n────────────────────"
            f"\n*➻ Uptime:* {uptime}"
            f"\n*Users:* {len(get_served_users())} "
            f"\n*Chats:* {len(get_served_chats())} "
            "\n────────────────────"
            "\n\n➲  I can restrict users, keep things hot and safe."
            "\n➲  Advanced anti-flood system to keep the party smooth."
            "\n➲  Custom welcomes and group rules, just how you like it."
            "\n➲  Warn, ban, mute, kick, all the spicy admin tools."
            "\n➲  Notes, blacklists, and hot keyword replies."
            f"\n\n➻ Tap the buttons below for more info about {updater.bot.first_name}, babe.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🏠", callback_data="babe_back"),
                        InlineKeyboardButton(text="💎", callback_data="source_"),
                        InlineKeyboardButton(text="👄", url=f"tg://user?id={OWNER_ID}"),
                        InlineKeyboardButton(text="🔥", callback_data="Main_help"),
                    ],
                    [
                        InlineKeyboardButton(text="Support 💌", callback_data="babe_support"),
                        InlineKeyboardButton(text="Commands 💁", callback_data="Main_help"),
                    ],
                    [
                        InlineKeyboardButton(text="Dev Daddy 😏", url=f"tg://user?id={OWNER_ID}"),
                        InlineKeyboardButton(text="Source 💦", callback_data="source_"),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="babe_back"),
                    ],
                ]
            ),
        )
    elif query.data == "babe_support":
        query.message.edit_caption(
            f"**Need a little help, baby?**\n\nIf you found a bug in {updater.bot.first_name} or want to give some feedback, come to my support chat and let's talk! 💋",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🏠", callback_data="babe_back"),
                        InlineKeyboardButton(text="💋", callback_data="babe_"),
                        InlineKeyboardButton(text="💎", callback_data="source_"),
                        InlineKeyboardButton(text="👄", url=f"tg://user?id={OWNER_ID}"),
                        InlineKeyboardButton(text="🔥", callback_data="Main_help"),
                    ],
                    [
                        InlineKeyboardButton(text="Support Group 💌", url=f"https://t.me/{SUPPORT_CHAT}"),
                        InlineKeyboardButton(text="Updates 🍸", url="https://t.me/mukeshbotzone"),
                    ],
                    [
                        InlineKeyboardButton(text="Dev Daddy 😏", url=f"tg://user?id={OWNER_ID}"),
                        InlineKeyboardButton(text="GitHub 🍹", url="https://github.com/noob-mukesh/MukeshRobot"),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="babe_"),
                    ],
                ]
            ),
        )
    elif query.data == "babe_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )


# --- Add missing stubs and patch unresolved references ---

# Dummy stubs for missing helpers and variables
PM_START_TEXT = PM_START_TEX
get_served_users = lambda: []
get_served_chats = lambda: []

# Dummy handler stubs
def Source_about_callback(update, context):
    pass

def Music_about_callback(update, context):
    pass

def MukeshRobot_Main_Callback(update, context):
    pass

def get_settings(update, context):
    pass

def settings_button(update, context):
    pass

# Dummy async stubs for assistant/music bot
async def assistant_sudo():
    pass
async def get_gbanned():
    return []
async def get_banned_users():
    return []
class DummyApp:
    async def start(self): pass
    async def stop(self): pass
assistant_app = DummyApp()
assistant_userbot = DummyApp()
class DummyCall:
    async def start(self): pass
    async def stream_call(self, url): pass
    async def decorators(self): pass
AssistantCall = DummyCall()
ASSISTANT_LOGGER = LOGGER
async def pyrogram_idle():
    pass
config = Config
BANNED_USERS = set()
ASSISTANT_MODULES = []
class NoActiveGroupCall(Exception):
    pass

def error_callback(update, context):
    pass

def send_settings(chat_id, user_id, user=False):
    pass

def migrate_chats(update, context):
    pass

def donate(update, context):
    pass

async def assistant_init():
    pass

def is_user_admin(chat, user_id):
    return True

# Moved Updater definition here
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def get_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(HELP_STRINGS, parse_mode=ParseMode.MARKDOWN)

def run_js_bot():
    js_path = os.path.join(os.path.dirname(__file__), 'index.js')
    try:
        # Use sys.executable to ensure correct environment, but call node
        subprocess.Popen(['node', js_path])
        print('Started JS bot (index.js) in background.')
    except Exception as e:
        print(f'Failed to start JS bot: {e}')

def main():
    run_js_bot()
    # Handler registration
    start_handler = CommandHandler("start", start, run_async=True)
    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*", run_async=True)
    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_", run_async=True)
    about_callback_handler = CallbackQueryHandler(Babe_about_callback, pattern=r"babe_", run_async=True)
    source_callback_handler = CallbackQueryHandler(Source_about_callback, pattern=r"source_", run_async=True)
    music_callback_handler = CallbackQueryHandler(Music_about_callback, pattern=r"Music_", run_async=True)
    main_menu_handler = CallbackQueryHandler(MukeshRobot_Main_Callback, pattern=r".*_help", run_async=True)
    migrate_handler = MessageHandler(filters.StatusUpdate.MIGRATE, migrate_chats)
    donate_handler = CommandHandler("donate", donate)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(main_menu_handler)
    dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(source_callback_handler)

    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)
    # Start assistant/music bot in background
    loop = asyncio.get_event_loop()
    loop.create_task(assistant_init())
    updater.idle()

if __name__ == "__main__":
    LOGGER.info("Successfully loaded module1: " + str(ALL_MODULES))
    main()