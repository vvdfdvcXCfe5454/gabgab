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

from io import BytesIO
from time import sleep

from telegram import ParseMode, TelegramError, Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, Filters

from gabby_config import Config
from __init__ import MongoDB
import sys

USERS_GROUP = 4
CHAT_GROUP = 5


def get_user_id(username, context=None):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    users = MongoDB('users').find_all({"username": username})

    if not users:
        return None

    if len(users) == 1:
        return users[0]["_id"]

    for user_obj in users:
        try:
            if context:
                userdat = context.bot.get_chat(user_obj["_id"])
                if userdat.username == username:
                    return userdat.id

        except BadRequest as excp:
            if excp.message != "Chat not found":
                print("Error extracting user ID")

    return None


def broadcast(update: Update, context: CallbackContext):
    to_send = update.effective_message.text.split(None, 1)

    if len(to_send) >= 2:
        to_group = False
        to_user = False
        if to_send[0] == "/broadcastgroups":
            to_group = True
        if to_send[0] == "/broadcastusers":
            to_user = True
        else:
            to_group = to_user = True
        chats = MongoDB('chats').find_all() or []
        users = MongoDB('users').find_all() or []
        failed = 0
        failed_user = 0
        if to_group:
            for chat in chats:
                try:
                    context.bot.sendMessage(
                        int(chat["chat_id"]),
                        to_send[1],
                        parse_mode="MARKDOWN",
                        disable_web_page_preview=True,
                    )
                    sleep(0.1)
                except TelegramError:
                    failed += 1
        if to_user:
            for user in users:
                try:
                    context.bot.sendMessage(
                        int(user["_id"]),
                        to_send[1],
                        parse_mode="MARKDOWN",
                        disable_web_page_preview=True,
                    )
                    sleep(0.1)
                except TelegramError:
                    failed_user += 1
        update.effective_message.reply_text(
            f"Broadcast complete.\nGroups failed: <code>{failed}</code>.\nUsers failed: <code>{failed_user}</code>.",
            parse_mode=ParseMode.HTML,
        )


def log_user(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    MongoDB('users').update({"_id": msg.from_user.id}, {"username": msg.from_user.username, "chat_id": chat.id, "chat_title": chat.title})
    if msg.reply_to_message:
        MongoDB('users').update({"_id": msg.reply_to_message.from_user.id}, {"username": msg.reply_to_message.from_user.username, "chat_id": chat.id, "chat_title": chat.title})
    if msg.forward_from:
        MongoDB('users').update({"_id": msg.forward_from.id}, {"username": msg.forward_from.username})


def chats(update: Update, context: CallbackContext):
    all_chats = MongoDB('chats').find_all() or []
    chatfile = "List of chats.\n0. Chat name | Chat ID | Members count\n"
    P = 1
    for chat in all_chats:
        try:
            curr_chat = context.bot.getChat(chat['chat_id'])
            chat_members = curr_chat.get_member_count()
            chatfile += f"{P}. {chat.get('chat_title', '')} | {chat['chat_id']} | {chat_members}\n"
            P += 1
        except Exception:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "groups_list.txt"
        update.effective_message.reply_document(
            document=output,
            filename="groups_list.txt",
            caption="ʜᴇʀᴇ ʙᴇ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ɢʀᴏᴜᴘꜱ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ.",
        )


def chat_checker(update: Update, context: CallbackContext):
    bot = context.bot
    try:
        if update.effective_message.chat.get_member(bot.id).can_send_messages is False:
            bot.leaveChat(update.effective_message.chat.id)
    except Unauthorized:
        pass


def __user_info__(user_id):
    if user_id in [777000, 1087968824]:
        return """╘══「 ɢʀᴏᴜᴘꜱ ᴄᴏᴜɴᴛ: <code>???</code> 」"""
    # Replace dispatcher.bot.id with a static check or context if needed
    num_chats = len(MongoDB('chats').find_all({"user_id": user_id}))
    return f"""╘══「 ɢʀᴏᴜᴘꜱ ᴄᴏᴜɴᴛ: <code>{num_chats}</code> 」"""


def __stats__():
    return f"× 0{MongoDB('users').count()} ᴜsᴇʀs, ᴀᴄʀᴏss 0{MongoDB('chats').count()} ᴄʜᴀᴛs"


def __migrate__(old_chat_id, new_chat_id):
    MongoDB('chats').update({"chat_id": old_chat_id}, {"chat_id": new_chat_id})

__mod_name__ = "𝐆-ᴄᴀsᴛ"

# ғᴏʀ ʜᴇʟᴘ ᴍᴇɴᴜ
