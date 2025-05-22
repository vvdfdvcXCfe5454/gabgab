"""
MIT License

Copyright (c) 2022 AshokShau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @AshokShau
#     UPDATE   :- Abishnoi_bots
#     GITHUB :- AshokShau ""
import ast
import html

from alphabet_detector import AlphabetDetector
from telegram import ChatPermissions, MessageEntity, ParseMode, TelegramError, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters
from telegram.utils.helpers import mention_html

import Exon.modules.sql.locks_sql as sql
from Exon import LOGGER as log
from Exon import dispatcher
from Exon.modules.connection import connected
from Exon.modules.helper_funcs.alternate import send_message, typing_action
from Exon.modules.helper_funcs.anonymous import AdminPerms, user_admin
from Exon.modules.helper_funcs.chat_status import can_delete, is_bot_admin
from Exon.modules.helper_funcs.chat_status import user_admin as u_admin
from Exon.modules.helper_funcs.chat_status import user_not_admin
from Exon.modules.helper_funcs.decorators import Exoncmd as natsunagicmd
from Exon.modules.helper_funcs.decorators import Exonmsg as natsunagimsg
from Exon.modules.log_channel import loggable
from Exon.modules.sql.approve_sql import is_approved

ad = AlphabetDetector()

LOCK_TYPES = {
    "audio": Filters.audio,
    "voice": Filters.voice,
    "document": Filters.document,
    "video": Filters.video,
    "contact": Filters.contact,
    "photo": Filters.photo,
    "url": Filters.entity(MessageEntity.URL)
           | Filters.caption_entity(MessageEntity.URL),
    "bots": Filters.status_update.new_chat_members,
    "forward": Filters.forwarded & ~Filters.is_automatic_forward,
    "game": Filters.game,
    "location": Filters.location,
    "egame": Filters.dice,
    "rtl": "rtl",
    "button": "button",
    "inline": "inline",
    "apk": Filters.document.mime_type("application/vnd.android.package-archive"),
    "doc": Filters.document.mime_type("application/msword"),
    "exe": Filters.document.mime_type("application/x-ms-dos-executable"),
    "gif": Filters.document.mime_type("video/mp4"),
    "jpg": Filters.document.mime_type("image/jpeg"),
    "mp3": Filters.document.mime_type("audio/mpeg"),
    "pdf": Filters.document.mime_type("application/pdf"),
    "txt": Filters.document.mime_type("text/plain"),
    "xml": Filters.document.mime_type("application/xml"),
    "zip": Filters.document.mime_type("application/zip"),
    "docx": Filters.document.mime_type(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ),
    "py": Filters.document.mime_type("text/x-python"),
    "svg": Filters.document.mime_type("image/svg+xml"),
    "targz": Filters.document.mime_type("application/x-compressed-tar"),
    "wav": Filters.document.mime_type("audio/x-wav"),
}

LOCK_CHAT_RESTRICTION = {
    "all": {
        "can_send_messages": False,
        "can_send_media_messages": False,
        "can_send_polls": False,
        "can_send_other_messages": False,
        "can_add_web_page_previews": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
    },
    "messages": {"can_send_messages": False},
    "media": {"can_send_media_messages": False},
    "sticker": {"can_send_other_messages": False},
    "gif": {"can_send_other_messages": False},
    "poll": {"can_send_polls": False},
    "other": {"can_send_other_messages": False},
    "previews": {"can_add_web_page_previews": False},
    "info": {"can_change_info": False},
    "invite": {"can_invite_users": False},
    "pin": {"can_pin_messages": False},
}

UNLOCK_CHAT_RESTRICTION = {
    "all": {
        "can_send_messages": True,
        "can_send_media_messages": True,
        "can_send_polls": True,
        "can_send_other_messages": True,
        "can_add_web_page_previews": True,
        "can_invite_users": True,
    },
    "messages": {"can_send_messages": True},
    "media": {"can_send_media_messages": True},
    "sticker": {"can_send_other_messages": True},
    "gif": {"can_send_other_messages": True},
    "poll": {"can_send_polls": True},
    "other": {"can_send_other_messages": True},
    "previews": {"can_add_web_page_previews": True},
    "info": {"can_change_info": True},
    "invite": {"can_invite_users": True},
    "pin": {"can_pin_messages": True},
}

PERM_GROUP = -8
REST_GROUP = -12


# NOT ASYNC
def restr_members(
        bot, chat_id, members, messages=False, media=False, other=False, previews=False
):
    for mem in members:
        try:
            bot.restrict_chat_member(
                chat_id,
                mem.user,
                can_send_messages=messages,
                can_send_media_messages=media,
                can_send_other_messages=other,
                can_add_web_page_previews=previews,
            )
        except TelegramError:
            pass


# NOT ASYNC
def unrestr_members(
        bot, chat_id, members, messages=True, media=True, other=True, previews=True
):
    for mem in members:
        try:
            bot.restrict_chat_member(
                chat_id,
                mem.user,
                can_send_messages=messages,
                can_send_media_messages=media,
                can_send_other_messages=other,
                can_add_web_page_previews=previews,
            )
        except TelegramError:
            pass


@natsunagicmd(command="locktypes")
def locktypes(update, _):
    update.effective_message.reply_text(
        "\n × ".join(
            ["Locks available: "]
            + sorted(list(LOCK_TYPES) + list(LOCK_CHAT_RESTRICTION))
        )
    )


@natsunagicmd(command="lock", pass_args=True)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
@loggable
@typing_action
def lock(update: Update, context: CallbackContext) -> str:  # sourcery no-metrics
    args = context.args
    chat = update.effective_chat
    user = update.effective_user

    if (
            can_delete(chat, context.bot.id)
            or update.effective_message.chat.type == "private"
    ):
        if len(args) >= 1:
            ltype = args[0].lower()
            if ltype in LOCK_TYPES:
                if conn := connected(
                        context.bot, update, chat, user.id, need_admin=True
                ):
                    chat = dispatcher.bot.getChat(conn)
                    # chat_id = conn
                    chat_name = chat.title
                    text = f"Locked {ltype} for non-admins in {chat_name}!"
                else:
                    if update.effective_message.chat.type == "private":
                        send_message(
                            update.effective_message,
                            "This command is meant to use in group not in PM",
                        )
                        return ""
                    chat = update.effective_chat
                    # chat_id = update.effective_chat.id
                    # chat_name = update.effective_message.chat.title
                    text = f"Locked {ltype} for non-admins!"
                sql.update_lock(chat.id, ltype, locked=True)
                send_message(update.effective_message, text, parse_mode="markdown")

                return f"<b>{html.escape(chat.title)}:</b>\n#LOCK\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\nLocked <code>{ltype}</code>."

            if ltype in LOCK_CHAT_RESTRICTION:
                if conn := connected(
                        context.bot, update, chat, user.id, need_admin=True
                ):
                    chat = dispatcher.bot.getChat(conn)
                    chat_id = conn
                    chat_name = chat.title
                    text = f"Locked {ltype} for all non-admins in {chat_name}!"
                else:
                    if update.effective_message.chat.type == "private":
                        send_message(
                            update.effective_message,
                            "This command is meant to use in group not in PM",
                        )
                        return ""
                    chat = update.effective_chat
                    chat_id = update.effective_chat.id
                    # chat_name = update.effective_message.chat.title
                    text = f"Locked {ltype} for all non-admins!"

                current_permission = context.bot.getChat(chat_id).permissions
                context.bot.set_chat_permissions(
                    chat_id=chat_id,
                    permissions=get_permission_list(
                        ast.literal_eval(str(current_permission)),
                        LOCK_CHAT_RESTRICTION[ltype.lower()],
                    ),
                )

                send_message(update.effective_message, text, parse_mode="markdown")
                return f"<b>{html.escape(chat.title)}:</b>\n#Permission_LOCK\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\nLocked <code>{ltype}</code>."

            send_message(
                update.effective_message,
                "What are you trying to lock...? Try /locktypes for the list of lockables",
            )
        else:
            send_message(update.effective_message, "What are you trying to lock...?")

    else:
        send_message(
            update.effective_message,
            "I am not administrator or haven't got enough rights.",
        )

    return ""


@natsunagicmd(command="unlock", pass_args=True)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
@loggable
@typing_action
def unlock(update: Update, context: CallbackContext) -> str:  # sourcery no-metrics
    args = context.args
    chat = update.effective_chat
    user = update.effective_user
    # message = update.effective_message
    if len(args) >= 1:
        ltype = args[0].lower()
        if ltype in LOCK_TYPES:
            if conn := connected(
                    context.bot, update, chat, user.id, need_admin=True
            ):
                chat = context.bot.getChat(conn)
                # chat_id = conn
                chat_name = chat.title
                text = f"Unlocked {ltype} for everyone in {chat_name}!"
            else:
                if update.effective_message.chat.type == "private":
                    send_message(
                        update.effective_message,
                        "This command is meant to use in group not in PM",
                    )
                    return ""
                chat = update.effective_chat
                # chat_id = update.effective_chat.id
                # chat_name = update.effective_message.chat.title
                text = f"Unlocked {ltype} for everyone!"
            sql.update_lock(chat.id, ltype, locked=False)
            send_message(update.effective_message, text, parse_mode="markdown")
            return f"<b>{html.escape(chat.title)}:</b>\n#UNLOCK\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\nUnlocked <code>{ltype}</code>."

        if ltype in UNLOCK_CHAT_RESTRICTION:
            if conn := connected(
                    context.bot, update, chat, user.id, need_admin=True
            ):
                chat = dispatcher.bot.getChat(conn)
                chat_id = conn
                chat_name = chat.title
                text = f"Unlocked {ltype} for everyone in {chat_name}!"
            else:
                if update.effective_message.chat.type == "private":
                    send_message(
                        update.effective_message,
                        "This command is meant to use in group not in PM",
                    )
                    return ""
                chat = update.effective_chat
                chat_id = update.effective_chat.id
                # chat_name = update.effective_message.chat.title
                text = f"Unlocked {ltype} for everyone!"

            current_permission = context.bot.getChat(chat_id).permissions
            context.bot.set_chat_permissions(
                chat_id=chat_id,
                permissions=get_permission_list(
                    ast.literal_eval(str(current_permission)),
                    UNLOCK_CHAT_RESTRICTION[ltype.lower()],
                ),
            )

            send_message(update.effective_message, text, parse_mode="markdown")

            return f"<b>{html.escape(chat.title)}:</b>\n#UNLOCK\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\nUnlocked <code>{ltype}</code>."
        send_message(
            update.effective_message,
            "What are you trying to unlock...? Try /locktypes for the list of lockables.",
        )

    else:
        send_message(update.effective_message, "What are you trying to unlock...?")

    return ""


@natsunagimsg((Filters.all & Filters.chat_type.groups), group=PERM_GROUP)
@user_not_admin
def del_lockables(update, context):  # sourcery no-metrics
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user
    if is_approved(chat.id, user.id):
        return
    for lockable, filter in LOCK_TYPES.items():
        if lockable == "rtl":
            if sql.is_locked(chat.id, lockable) and can_delete(chat, context.bot.id):
                if message.caption:
                    check = ad.detect_alphabet(f"{message.caption}")
                    if "ARABIC" in check:
                        try:
                            message.delete()
                        except BadRequest as excp:
                            if excp.message != "Message to delete not found":
                                log.exception("ERROR in lockables")
                        break
                if message.text:
                    check = ad.detect_alphabet(f"{message.text}")
                    if "ARABIC" in check:
                        try:
                            message.delete()
                        except BadRequest as excp:
                            if excp.message != "Message to delete not found":
                                log.exception("ERROR in lockables")
                        break
            continue
        if lockable == "button":
            if (
                    sql.is_locked(chat.id, lockable)
                    and can_delete(chat, context.bot.id)
                    and message.reply_markup
                    and message.reply_markup.inline_keyboard
            ):
                try:
                    message.delete()
                except BadRequest as excp:
                    if excp.message != "Message to delete not found":
                        log.exception("ERROR in lockables")
                break
            continue
        if lockable == "inline":
            if (
                    sql.is_locked(chat.id, lockable)
                    and can_delete(chat, context.bot.id)
                    and message
                    and message.via_bot
            ):
                try:
                    message.delete()
                except BadRequest as excp:
                    if excp.message != "Message to delete not found":
                        log.exception("ERROR in lockables")
                break
            continue
        if (
                filter(update)
                and sql.is_locked(chat.id, lockable)
                and can_delete(chat, context.bot.id)
        ):
            if lockable == "bots":
                new_members = update.effective_message.new_chat_members
                for new_mem in new_members:
                    if new_mem.is_bot:
                        if not is_bot_admin(chat, context.bot.id):
                            send_message(
                                update.effective_message,
                                "I see a bot and I've been told to stop them from joining..."
                                "but I'm not admin!",
                            )
                            return

                        chat.ban_member(new_mem.id)
                        send_message(
                            update.effective_message,
                            "Only admins are allowed to add bots in this chat! Get outta here.",
                        )
                        break
            else:
                try:
                    message.delete()
                except BadRequest as excp:
                    if excp.message != "Message to delete not found":
                        log.exception("ERROR in lockables")

                break


def build_lock_message(chat_id):
    locks = sql.get_locks(chat_id)
    res = ""
    locklist = []
    if locks:
        res += "*" + "These are the current locks in this Chat:" + "*"
        locklist.extend(
            (
                f"sticker = `{locks.sticker}`",
                f"audio = `{locks.audio}`",
                f"voice = `{locks.voice}`",
                f"document = `{locks.document}`",
                f"video = `{locks.video}`",
                f"contact = `{locks.contact}`",
                f"photo = `{locks.photo}`",
                f"gif = `{locks.gif}`",
                f"url = `{locks.url}`",
                f"bots = `{locks.bots}`",
                f"forward = `{locks.forward}`",
                f"game = `{locks.game}`",
                f"location = `{locks.location}`",
                f"rtl = `{locks.rtl}`",
                f"button = `{locks.button}`",
                f"egame = `{locks.egame}`",
                f"inline = `{locks.inline}`",
                f"apk = `{locks.apk}`",
                f"doc = `{locks.doc}`",
                f"exe = `{locks.exe}`",
                f"jpg = `{locks.jpg}`",
                f"mp3 = `{locks.mp3}`",
                f"pdf = `{locks.pdf}`",
                f"txt = `{locks.txt}`",
                f"xml = `{locks.xml}`",
                f"zip = `{locks.zip}`",
                f"docx = `{locks.docx}`",
                f"py = `{locks.py}`",
                f"svg = `{locks.svg}`",
                f"targz = `{locks.targz}`",
                f"wav = `{locks.wav}`",
            )
        )
    permissions = dispatcher.bot.get_chat(chat_id).permissions
    permslist = [
        f"messages = `{permissions.can_send_messages}`",
        f"media = `{permissions.can_send_media_messages}`",
        f"poll = `{permissions.can_send_polls}`",
        f"other = `{permissions.can_send_other_messages}`",
        f"previews = `{permissions.can_add_web_page_previews}`",
        f"info = `{permissions.can_change_info}`",
        f"invite = `{permissions.can_invite_users}`",
        f"pin = `{permissions.can_pin_messages}`",
    ]
    if locklist:
        # Ordering lock list
        locklist.sort()
        # Building lock list string
        for x in locklist:
            res += f"\n × {x}"
    res += "\n\n*" + "These are the current chat permissions:" + "*"
    for x in permslist:
        res += f"\n × {x}"
    return res


@natsunagicmd(command="locks")
@u_admin
@typing_action
def list_locks(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user

    # Connection check
    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_name = chat.title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "This command is meant to use in group not in PM",
            )
            return ""
        chat = update.effective_chat
        chat_name = update.effective_message.chat.title

    res = build_lock_message(chat.id)
    if conn:
        res = res.replace("Locks in", f"*{chat_name}*")

    send_message(update.effective_message, res, parse_mode=ParseMode.MARKDOWN)


def get_permission_list(current, new):
    permissions = {
        "can_send_messages": None,
        "can_send_media_messages": None,
        "can_send_polls": None,
        "can_send_other_messages": None,
        "can_add_web_page_previews": None,
        "can_change_info": None,
        "can_invite_users": None,
        "can_pin_messages": None,
    }
    permissions |= current
    permissions.update(new)
    return ChatPermissions(**permissions)


def __import_data__(chat_id, data):
    # set chat locks
    locks = data.get("locks", {})
    for itemlock in locks:
        if itemlock in LOCK_TYPES:
            sql.update_lock(chat_id, itemlock, locked=True)
        elif itemlock in LOCK_CHAT_RESTRICTION:
            sql.update_restriction(chat_id, itemlock, locked=True)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return build_lock_message(chat_id)


__mod_name__ = "𝐋ᴏᴄᴋs"

# ғᴏʀ ʜᴇʟᴘ ᴍᴇɴᴜ


# """
from Exon.modules.language import gs


def get_help(chat):
    return gs(chat, "locks_help")

# """
