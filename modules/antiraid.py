import html
from datetime import timedelta
from typing import Optional

from pytimeparse.timeparse import timeparse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

import gabby_main.gabby_modules.sql.welcome_sql as sql
from gabby_main import LOGGER as log
from gabby_main.gabby_modules.cron_jobs import j
from gabby_main.gabby_modules.helper_funcs.anonymous import AdminPerms
from gabby_main.gabby_modules.helper_funcs.anonymous import resolve_user as res_user
from gabby_main.gabby_modules.helper_funcs.anonymous import user_admin as u_admin
from gabby_main.gabby_modules.helper_funcs.chat_status import connection_status, user_admin_no_reply
from gabby_main.gabby_modules.helper_funcs.decorators igabby_maint gabby_magabby_mainllback, gabby_maincmd
from gabby_main.gabby_modules.log_channel import loggable


def get_time(time: str) -> int:
    try:
        return timeparse(time)
    except Exception:
        return 0


def get_readable_time(time: int) -> str:
    t = f"{timedelta(seconds=time)}".split(":")
    if time == 86400:
        return "1 day"
    return f"{t[0]} ʜᴏᴜʀ(s)" if time >= 3600 else f"{t[1]} ᴍɪɴᴜᴛᴇs"


@gabby_maincmd(command="raid", pass_args=True)
@connection_status
@loggable
@u_admin(AdminPerms.CAN_CHANGE_INFO)
def setRaid(update: Update, context: CallbackContext) -> Optional[str]:
    args = context.args
    chat = update.effective_chat
    msg = update.effective_message
    u = update.effective_user
    user = res_user(u, msg.message_id, chat)
    if chat.type == "private":
        context.bot.sendMessage(chat.id, "ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴘᴍs.")
        return
    stat, time, acttime = sql.getDefenseStatus(chat.id)
    readable_time = get_readable_time(time)
    if len(args) == 0:
        if stat:
            text = "ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ <code>ᴇɴᴀʙʟᴇᴅ</code>\nᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ <code>ᴅɪsᴀʙʟᴇ</code> ʀᴀɪᴅ?"
            keyboard = [
                [
                    InlineKeyboardButton(
                        "ᴅɪsᴀʙʟᴇ ʀᴀɪᴅ",
                        callback_data=f"disable_raid={chat.id}={time}",
                    ),
                    InlineKeyboardButton(
                        "ᴄᴀɴᴄᴇʟ", callback_data="cancel_raid=1"
                    ),
                ]
            ]
        else:
            text = f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ <code>ᴅɪsᴀʙʟᴇᴅ</code>\nᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ <code>ᴇɴᴀʙʟᴇ</code> ʀᴀɪᴅ ғᴏʀ {readable_time}?"
            keyboard = [
                [
                    InlineKeyboardButton(
                        "ᴇɴᴀʙʟᴇ ʀᴀɪᴅ",
                        callback_data=f"enable_raid={chat.id}={time}",
                    ),
                    InlineKeyboardButton(
                        "ᴄᴀɴᴄᴇʟ", callback_data="cancel_raid=0"
                    ),
                ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    elif args[0] == "off":
        if stat:
            sql.setDefenseStatus(chat.id, False, time, acttime)
            text = "ʀᴀɪᴅ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ <code>ᴅɪsᴀʙʟᴇᴅ</code>, ᴍᴇᴍʙᴇʀs ᴛʜᴀᴛ ᴊᴏɪɴ ᴡɪʟʟ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ᴋɪᴄᴋᴇᴅ."
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            return f"<b>{html.escape(chat.title)}:</b>\n#𝐑𝐀𝐈𝐃\nᴅɪsᴀʙʟᴇᴅ\n<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
    else:
        args_time = args[0].lower()
        if time := get_time(args_time):
            readable_time = get_readable_time(time)
            if time >= 300 and time < 86400:
                text = f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ <code>ᴅɪsᴀʙʟᴇᴅ</code>\nᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ <code>ᴇɴᴀʙʟᴇ</code> ʀᴀɪᴅ ғᴏʀ {readable_time}?"
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "ᴇɴᴀʙʟᴇ ʀᴀɪᴅ",
                            callback_data=f"enable_raid={chat.id}={time}",
                        ),
                        InlineKeyboardButton(
                            "ᴄᴀɴᴄᴇʟ", callback_data="cancel_raid=0"
                        ),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                msg.reply_text(
                    text, parse_mode=ParseMode.HTML, reply_markup=reply_markup
                )
            else:
                msg.reply_text(
                    "ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 5 ᴍɪɴᴜᴛᴇs ᴀɴᴅ 1 ᴅᴀʏ",
                    parse_mode=ParseMode.HTML,
                )

        else:
            msg.reply_text(
                "ᴜɴᴋɴᴏᴡɴ ᴛɪᴍᴇ ɢɪᴠᴇɴ, ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ʟɪᴋᴇ 5m ᴏʀ 1h",
                parse_mode=ParseMode.HTML,
            )


@gabby_maincallback(pattern="enable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def enable_raid_cb(update: Update, _: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("enable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = int(args[1])
    readable_time = get_readable_time(time)
    _, t, acttime = sql.getDefenseStatus(chat_id)
    sql.setDefenseStatus(chat_id, True, time, acttime)
    update.effective_message.edit_text(
        f"ʀᴀɪᴅ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ <code>ᴇɴᴀʙʟᴇᴅ</code> ғᴏʀ {readable_time}.",
        parse_mode=ParseMode.HTML,
    )
    log.info("ᴇɴᴀʙʟᴇᴅ ʀᴀɪᴅ ᴍᴏᴅᴇ ɪɴ {} ғᴏʀ {}".format(chat_id, readable_time))

    def disable_raid(_):
        sql.setDefenseStatus(chat_id, False, t, acttime)
        log.info("ᴅɪsʙʟᴇᴅ ʀᴀɪᴅ ᴍᴏᴅᴇ ɪɴ {}".format(chat_id))
        logmsg = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#𝐑𝐀𝐈𝐃\n"
            f"ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅɪsᴀʙʟᴇᴅ\n"
        )
        return logmsg

    j.run_once(disable_raid, time)
    logmsg = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#𝐑𝐀𝐈𝐃\n"
        f"ᴇɴᴀʙʟʙᴇᴅ ғᴏʀ {readable_time}\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
    )
    return logmsg


@gabby_maincallback(pattern="disable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def disable_raid_cb(update: Update, _: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("disable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = args[1]
    _, t, acttime = sql.getDefenseStatus(chat_id)
    sql.setDefenseStatus(chat_id, False, time, acttime)
    update.effective_message.edit_text(
        "ʀᴀɪᴅ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ <code>Disabled</code>, ᴊᴏɪɴɪɢ ᴍᴇᴍʙᴇʀs ᴡɪʟʟ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ᴋɪᴄᴋᴇᴅ.",
        parse_mode=ParseMode.HTML,
    )
    return f"<b>{html.escape(chat.title)}:</b>\n#𝐑𝐀𝐈𝐃\nᴅɪsᴀʙʟᴇᴅ\n<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"


@gabby_maincallback(pattern="cancel_raid=")
@connection_status
@user_admin_no_reply
def disable_raid_cb(update: Update, context: CallbackContext):
    args = update.callback_query.data.split("=")
    what = args[0]
    update.effective_message.edit_text(
        f"ᴀᴄᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ, ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ sᴛᴀʏ <code>{'Enabled' if what == 1 else 'Disabled'}</code>.",
        parse_mode=ParseMode.HTML,
    )


@gabby_maincmd(command="raidtime")
@connection_status
@loggable
@u_admin(AdminPerms.CAN_CHANGE_INFO)
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, time, acttime = sql.getDefenseStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    u = update.effective_user
    chat = update.effective_chat
    user = res_user(u, msg.message_id, chat)
    if not args:
        msg.reply_text(
            f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {get_readable_time(time)}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ ʟᴀsᴛ ғᴏʀ {get_readable_time(time)} ᴛʜᴇɴ ᴛᴜʀɴ ᴏғғ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ",
            parse_mode=ParseMode.HTML,
        )
        return
    args_time = args[0].lower()
    if time := get_time(args_time):
        readable_time = get_readable_time(time)
        if time >= 300 and time < 86400:
            text = f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {readable_time}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ ʟᴀsᴛ ғᴏʀ {readable_time} ᴛʜᴇɴ ᴛᴜʀɴ ᴏғғ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ"
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setDefenseStatus(chat.id, what, time, acttime)
            return f"<b>{html.escape(chat.title)}:</b>\n#𝐑𝐀𝐈𝐃\nsᴇᴛ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴛɪᴍᴇ ᴛᴏ {readable_time}\n<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        else:
            msg.reply_text(
                "ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 5 ᴍɪɴᴜᴛᴇs ᴀɴᴅ 1 ᴅᴀʏ",
                parse_mode=ParseMode.HTML,
            )
    else:
        msg.reply_text(
            "ᴜɴᴋɴᴏᴡɴ ᴛɪᴍᴇ ɢɪᴠᴇɴ, give ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ʟɪᴋᴇ 5ᴍ ᴏʀ 1ʜ",
            parse_mode=ParseMode.HTML,
        )


@gabby_maincmd(command="raidactiontime", pass_args=True)
@connection_status
@u_admin(AdminPerms.CAN_CHANGE_INFO)
@loggable
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, t, time = sql.getDefenseStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    u = update.effective_user
    chat = update.effective_chat
    user = res_user(u, msg.message_id, chat)
    if not args:
        msg.reply_text(
            f"ʀᴀɪᴅ ᴀᴄᴛᴏɪɴ ᴛɪᴍᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {get_readable_time(time)}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ᴍᴇᴍʙᴇʀs ᴛʜᴀᴛ ᴊᴏɪɴ ᴡɪʟʟ ʙᴇ ᴛᴇᴍᴘ ʙᴀɴɴᴇᴅ ғᴏʀ {get_readable_time(time)}",
            parse_mode=ParseMode.HTML,
        )
        return
    args_time = args[0].lower()
    if time := get_time(args_time):
        readable_time = get_readable_time(time)
        if time >= 300 and time < 86400:
            text = f"ʀᴀɪᴅ ᴀᴄᴛᴏɪɴ ᴛɪᴍᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {get_readable_time(time)}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ᴍᴇᴍʙᴇʀs ᴛʜᴀᴛ ᴊᴏɪɴ ᴡɪʟʟ ʙᴇ ᴛᴇᴍᴘ ʙᴀɴɴᴇᴅ ғᴏʀ {readable_time}"
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setDefenseStatus(chat.id, what, t, time)
            return f"<b>{html.escape(chat.title)}:</b>\n#𝐑𝐀𝐈𝐃\nsᴇᴛ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴀᴄᴛɪᴏɴ ᴛɪᴍᴇ ᴛᴏ {readable_time}\n<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        else:
            msg.reply_text(
                "ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 5 ᴍɪɴᴜᴛᴇs ᴀɴᴅ 1 ᴅᴀʏ",
                parse_mode=ParseMode.HTML,
            )
    else:
        msg.reply_text(
            "ᴜɴᴋɴᴏᴡɴ ᴛɪᴍᴇ ɢɪᴠᴇɴ, ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ʟɪᴋᴇ 5m ᴏʀ 1h",
            parse_mode=ParseMode.HTML,
        )

def get_help(chat):
    return gs(chat, "raid_help")


# """

__mod_name__ = "𝐀-ʀᴀɪᴅ"
