import json
import os
import time
from io import BytesIO

from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler

# from gabby.gabby_modules.sql import warns_sql as warnssql
import gabby.gabby_modules.sql.blacklist_sql as blacklistsql
# from gabby.gabby_modules.sql import cust_filters_sql as filtersql
# import gabby.gabby_modules.sql.welcome_sql as welcsql
import gabby.gabby_modules.sql.locks_sql as locksql
import gabby.gabby_modules.sql.notes_sql as sql
# from gabby.gabby_modules.rules import get_rules
import gabby.gabby_modules.sql.rules_sql as rulessql
from gabby import JOIN_LOGGER, LOGGER, OWNER_ID, SUPPORT_CHAT, dispatcher
from gabby.__main__ import DATA_IMPORT
from gabby.gabby_modules.connection import connected
from gabby.gabby_modules.helper_funcs.alternate import typing_action
from gabby.gabby_modules.helper_funcs.chat_status import user_admin
from gabby.gabby_modules.sql import disable_sql as disabledsql


@user_admin
@typing_action
def import_data(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    # TODO: allow uploading doc with command, not just as reply
    # only work with a doc

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            update.effective_message.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ғᴏʀ ɢʀᴏᴜᴘ !")
            return ""

        chat = update.effective_chat
        chat_name = update.effective_message.chat.title

    if msg.reply_to_message and msg.reply_to_message.document:
        try:
            file_info = context.bot.get_file(msg.reply_to_message.document.file_id)
        except BadRequest:
            msg.reply_text(
                "ᴛʀʏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀɴᴅ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛʜᴇ ғɪʟᴇ ʏᴏᴜʀsᴇʟғ ᴀɢᴀɪɴ, ᴛʜɪs ᴏɴᴇ sᴇᴇᴍ ʙʀᴏᴋᴇɴ ᴛᴏ ᴍᴇ!",
            )
            return

        with BytesIO() as file:
            file_info.download(out=file)
            file.seek(0)
            data = json.load(file)

        # only import one group
        if len(data) > 1 and str(chat.id) not in data:
            msg.reply_text(
                "ᴛʜᴇʀᴇ ᴀʀᴇ ᴍᴏʀᴇ ᴛʜᴀɴ ᴏɴᴇ ɢʀᴏᴜᴘ ɪɴ ᴛʜɪs ғɪʟᴇ ᴀɴᴅ ᴛʜᴇ chat.id ɪs ɴᴏᴛ sᴀᴍᴇ! ʜᴏᴡ ᴀᴍ ɪ sᴜᴘᴘᴏsᴇᴅ ᴛᴏ ɪᴍᴘᴏʀᴛ ɪᴛ?",
            )
            return

        # Check if backup is this chat
        try:
            if data.get(str(chat.id)) is None:
                if conn:
                    text = f"ʙᴀᴄᴋᴜᴘ ᴄᴏᴍᴇs ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀᴛ, ɪ ᴄᴀɴ'ᴛ ʀᴇᴛᴜʀɴ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀᴛ ᴛᴏ ᴄʜᴀᴛ *{chat_name}*"
                else:
                    text = "ʙᴀᴄᴋᴜᴘ ᴄᴏᴍᴇs ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀᴛ, I ᴄᴀɴ'ᴛ ʀᴇᴛᴜʀɴ another ᴄʜᴀᴛ ᴛᴏ ᴛʜɪs ᴄʜᴀᴛ"
                return msg.reply_text(text, parse_mode="markdown")
        except Exception:
            return msg.reply_text("ᴛʜᴇʀᴇ ᴡᴀs ᴀ ᴘʀᴏʙʟᴇᴍ ᴡʜɪʟᴇ ɪᴍᴘᴏʀᴛɪɴɢ ᴛʜᴇ ᴅᴀᴛᴀ!")
        # Check if backup is from self
        try:
            if str(context.bot.id) != str(data[str(chat.id)]["bot"]):
                return msg.reply_text(
                    "ʙᴀᴄᴋᴜᴘ ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ʙᴏᴛ ᴛʜᴀᴛ ɪs ɴᴏᴛ sᴜɢɢᴇsᴛᴇᴅ ᴍɪɢʜᴛ ᴄᴀᴜsᴇ ᴛʜᴇ ᴘʀᴏʙʟᴇᴍ, ᴅᴏᴄᴜᴍᴇɴᴛs, ᴘʜᴏᴛᴏs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏs, ʀᴇᴄᴏʀᴅs ᴍɪɢʜᴛ ɴᴏᴛ ᴡᴏʀᴋ ᴀs ɪᴛ sʜᴏᴜʟᴅ ʙᴇ.",
                )
        except Exception:
            pass
        # Select data source
        if str(chat.id) in data:
            data = data[str(chat.id)]["hashes"]
        else:
            data = data[list(data.keys())[0]]["hashes"]

        try:
            for mod in DATA_IMPORT:
                mod.__import_data__(str(chat.id), data)
        except Exception:
            msg.reply_text(
                f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʀᴇᴄᴏᴠᴇʀɪɴɢ ʏᴏᴜʀ ᴅᴀᴛᴀ. ᴛʜᴇ ᴘʀᴏᴄᴇss ғᴀɪʟᴇᴅ. ɪғ ʏᴏᴜ ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴀ ᴘʀᴏʙʟᴇᴍ ᴡɪᴛʜ ᴛʜɪs, ᴘʟᴇᴀsᴇ ᴛᴀᴋᴇ ɪᴛ ᴛᴏ @{SUPPORT_CHAT}",
            )

            LOGGER.exception(
                "ɪᴍᴘᴏʀᴛ ғᴏʀ ᴛʜᴇ ᴄʜᴀᴛ %s ᴡɪᴛʜ ᴛʜᴇ ɴᴀᴍᴇ %s ғᴀɪʟᴇᴅ.",
                str(chat.id),
                str(chat.title),
            )
            return

        # TODO: some of that link logic
        # NOTE: consider default permissions stuff?
        if conn:
            text = f"ʙᴀᴄᴋᴜᴘ ғᴜʟʟʏ ʀᴇsᴛᴏʀᴇᴅ ᴏɴ *{chat_name}*."
        else:
            text = "ʙᴀᴄᴋᴜᴘ ғᴜʟʟʏ ʀᴇsᴛᴏʀᴇᴅ"
        msg.reply_text(text, parse_mode="markdown")


@user_admin
def export_data(update, context):
    chat_data = context.chat_data
    msg = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    current_chat_id = update.effective_chat.id
    if conn := connected(context.bot, update, chat, user.id, need_admin=True):
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
    else:
        if update.effective_message.chat.type == "private":
            update.effective_message.reply_text("ᴛʜɪs ɪs ᴀ ɢʀᴏᴜᴘ ᴄᴏᴍᴍᴀɴᴅ!")
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
    jam = time.time()
    new_jam = jam + 10800
    checkchat = get_chat(chat_id, chat_data)
    if checkchat.get("status") and jam <= int(checkchat.get("value")):
        timeformatt = time.strftime(
            "%H:%M:%S %d/%m/%Y",
            time.localtime(checkchat.get("value")),
        )
        update.effective_message.reply_text(
            f"ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ʙᴀᴄᴋᴜᴘ ᴏɴᴄᴇ ᴀ ᴅᴀʏ!\nʏᴏᴜ ᴄᴀɴ ʙᴀᴄᴋᴜᴘ ᴀɢᴀɪɴ ɪɴ ᴀʙᴏᴜᴛ `{timeformatt}`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    if user.id != OWNER_ID:
        put_chat(chat_id, new_jam, chat_data)
    note_list = sql.get_all_chat_notes(chat_id)
    # button = ""
    buttonlist = []
    namacat = ""
    isicat = ""
    rules = ""
    count = 0
    countbtn = 0
    # Notes
    for note in note_list:
        count += 1
        # getnote = sql.get_note(chat_id, note.name)
        namacat += f"{note.name}<###splitter###>"
        if note.msgtype == 1:
            tombol = sql.get_buttons(chat_id, note.name)
            # keyb = []
            for btn in tombol:
                countbtn += 1
                if btn.same_line:
                    buttonlist.append((f"{btn.name}", f"{btn.url}", True))
                else:
                    buttonlist.append((f"{btn.name}", f"{btn.url}", False))
            isicat += f"###button###: {note.value}<###button###>{buttonlist}<###splitter###>"
            buttonlist.clear()
        elif note.msgtype == 2:
            isicat += f"###sticker###:{note.file}<###splitter###>"
        elif note.msgtype == 3:
            isicat += f"###file###:{note.file}<###TYPESPLIT###>{note.value}<###splitter###>"
        elif note.msgtype == 4:
            isicat += f"###photo###:{note.file}<###TYPESPLIT###>{note.value}<###splitter###>"
        elif note.msgtype == 5:
            isicat += f"###audio###:{note.file}<###TYPESPLIT###>{note.value}<###splitter###>"
        elif note.msgtype == 6:
            isicat += f"###voice###:{note.file}<###TYPESPLIT###>{note.value}<###splitter###>"
        elif note.msgtype == 7:
            isicat += f"###video###:{note.file}<###TYPESPLIT###>{note.value}<###splitter###>"
        elif note.msgtype == 8:
            isicat += f"###video_note###:{note.file}<###TYPESPLIT###>{note.value}<###splitter###>"
        else:
            isicat += f"{note.value}<###splitter###>"
    notes = {
        f'#{namacat.split("<###splitter###>")[x]}': f'{isicat.split("<###splitter###>")[x]}'
        for x in range(count)
    }
    # Rules
    rules = rulessql.get_rules(chat_id)
    # Blacklist
    bl = list(blacklistsql.get_chat_blacklist(chat_id))
    # Disabled command
    disabledcmd = list(disabledsql.get_all_disabled(chat_id))
    # Filters (TODO)
    """
	all_filters = list(filtersql.get_chat_triggers(chat_id))
	export_filters = {}
	for filters in all_filters:
		filt = filtersql.get_filter(chat_id, filters)
		# print(vars(filt))
		if filt.is_sticker:
			tipefilt = "sticker"
		elif filt.is_document:
			tipefilt = "doc"
		elif filt.is_image:
			tipefilt = "img"
		elif filt.is_audio:
			tipefilt = "audio"
		elif filt.is_voice:
			tipefilt = "voice"
		elif filt.is_video:
			tipefilt = "video"
		elif filt.has_buttons:
			tipefilt = "button"
			buttons = filtersql.get_buttons(chat.id, filt.keyword)
			print(vars(buttons))
		elif filt.has_markdown:
			tipefilt = "text"
		if tipefilt == "button":
			content = "{}#=#{}|btn|{}".format(tipefilt, filt.reply, buttons)
		else:
			content = "{}#=#{}".format(tipefilt, filt.reply)
		print(content)
		export_filters[filters] = content
	print(export_filters)
	"""
    # Welcome (TODO)
    # welc = welcsql.get_welc_pref(chat_id)
    # Locked
    curr_locks = locksql.get_locks(chat_id)
    curr_restr = locksql.get_restr(chat_id)

    if curr_locks:
        locked_lock = {
            "sticker": curr_locks.sticker,
            "audio": curr_locks.audio,
            "voice": curr_locks.voice,
            "document": curr_locks.document,
            "video": curr_locks.video,
            "contact": curr_locks.contact,
            "photo": curr_locks.photo,
            "gif": curr_locks.gif,
            "url": curr_locks.url,
            "bots": curr_locks.bots,
            "forward": curr_locks.forward,
            "game": curr_locks.game,
            "location": curr_locks.location,
            "rtl": curr_locks.rtl,
        }
    else:
        locked_lock = {}

    if curr_restr:
        locked_restr = {
            "messages": curr_restr.messages,
            "media": curr_restr.media,
            "other": curr_restr.other,
            "previews": curr_restr.preview,
            "all": all(
                [
                    curr_restr.messages,
                    curr_restr.media,
                    curr_restr.other,
                    curr_restr.preview,
                ],
            ),
        }
    else:
        locked_restr = {}

    locks = {"locks": locked_lock, "restrict": locked_restr}
    backup = {
        chat_id: {
            "bot": context.bot.id,
            "hashes": {
                "info": {"rules": rules},
                "extra": notes,
                "blacklist": bl,
                "disabled": disabledcmd,
                "locks": locks,
            },
        }
    }
    baccinfo = json.dumps(backup, indent=4)
    with open(f"gabby-gabby{chat_id}.backup", "w") as f:
        f.write(baccinfo)
    context.bot.sendChatAction(current_chat_id, "upload_document")
    tgl = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime(time.time()))
    try:
        context.bot.sendMessage(
            JOIN_LOGGER,
            f"*sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ʙᴀᴄᴋᴜᴘ:*\nᴄʜᴀᴛ: `{chat.title}`\nᴄʜᴀᴛ ɪᴅ: `{chat_id}`\nᴏɴ: `{tgl}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except BadRequest:
        pass
    context.bot.sendDocument(
        current_chat_id,
        document=open(f"gabby-gabby{chat_id}.backup", "rb"),
        caption=f"*sᴜᴄᴄᴇssғᴜʟʟʏ ᴇxᴘᴏʀᴛᴇᴅ ʙᴀᴄᴋᴜᴘ:*\nᴄʜᴀᴛ: `{chat.title}`\nᴄʜᴀᴛ ɪᴅ: `{chat_id}`\nᴏɴ: `{tgl}`\n\nɴᴏᴛᴇ: ᴛʜɪs `gabby-gabby-Backup` ᴡᴀs sᴘᴇᴄɪᴀʟʟʏ ᴍᴀᴅᴇ ғᴏʀ ɴᴏᴛᴇs.",
        timeout=360,
        reply_to_message_id=msg.message_id,
        parse_mode=ParseMode.MARKDOWN,
    )
    os.remove(f"gabby-gabby{chat_id}.backup")


# Temporary data
def put_chat(chat_id, value, chat_data):
    # print(chat_data)
    status = value is not False
    chat_data[chat_id] = {"backups": {"status": status, "value": value}}


def get_chat(chat_id, chat_data):
    # print(chat_data)
    try:
        return chat_data[chat_id]["backups"]
    except KeyError:
        return {"status": False, "value": False}


__mod_name__ = "𝐁ᴀᴄᴋᴜᴘ"

IMPORT_HANDLER = CommandHandler(["import", "backup"], import_data, run_async=True)
EXPORT_HANDLER = CommandHandler(
    "export", export_data, pass_chat_data=True, run_async=True
)

dispatcher.add_handler(IMPORT_HANDLER)
dispatcher.add_handler(EXPORT_HANDLER)

# ғᴏʀ ʜᴇʟᴘ ᴍᴇɴᴜ
# """
from gabby.modules11.language import gs


def get_help(chat):
    return gs(chat, "backup_help")

# """
