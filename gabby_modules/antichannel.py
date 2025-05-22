import html

import requests
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

import Exon.modules.sql.antilinkedchannel_sql as sql
from Exon import SUPPORT_CHAT, TOKEN, dispatcher
from Exon.modules.helper_funcs.anonymous import AdminPerms, user_admin
from Exon.modules.helper_funcs.chat_status import bot_admin, bot_can_delete
from Exon.modules.helper_funcs.chat_status import user_admin as u_admin
from Exon.modules.helper_funcs.decorators import Exoncmd, Exonmsg
from Exon.modules.sql import acm_sql


@Exoncmd(command="antilinkedchan", group=112)
@bot_can_delete
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antilinkedchannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            if sql.status_pin(chat.id):
                sql.disable_pin(chat.id)
                sql.enable_pin(chat.id)
                message.reply_html(
                    f"ᴇɴᴀʙʟᴇᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴅᴇʟᴇᴛɪᴏɴ ᴀɴᴅ ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}"
                )
            else:
                sql.enable_linked(chat.id)
                message.reply_html(f"ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ɪɴ {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            sql.disable_linked(chat.id)
            message.reply_html(
                f"ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ɪɴ {html.escape(chat.title)}"
            )
        else:
            message.reply_text(f"ᴜɴʀᴇᴄᴏɢɴɪᴢᴇᴅ ᴀʀɢᴜᴍᴇɴᴛs {s}")
        return
    message.reply_html(
        f"ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴅᴇʟᴇᴛɪᴏɴ ɪs ᴄᴜʀʀᴇɴᴛʟʏ {sql.status_linked(chat.id)} ɪɴ {html.escape(chat.title)}"
    )


@Exonmsg(Filters.is_automatic_forward, group=111)
def eliminate_linked_channel_msg(update: Update, _: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not sql.status_linked(chat.id):
        return
    try:
        message.delete()
    except TelegramError:
        return


@bot_admin
@u_admin
def antichannelmode(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    if args := context.args:
        if len(args) != 1:
            msg.reply_text("Invalid arguments!")
            return
        param = args[0]
        if param in ("on", "true", "yes", "On", "Yes", "True"):
            acm_sql.setCleanLinked(chat.id, True)
            msg.reply_text(
                f"*ᴇɴᴀʙʟᴇᴅ* ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ɪɴ {chat.title}. ᴍᴇssᴀɢᴇs sᴇɴᴛ ʙʏ ᴄʜᴀɴɴᴇʟ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return
        if param in ("off", "false", "no", "No", "Off", "False"):
            acm_sql.setCleanLinked(chat.id, False)
            msg.reply_text(
                f"*ᴅɪsᴀʙʟᴇᴅ* ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ɪɴ {chat.title}.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return
        msg.reply_text(
            "Your input was not recognised as one of: yes/no/on/off"
        )  # on or off ffs
    else:
        if stat := acm_sql.getCleanLinked(str(chat.id)):
            msg.reply_text(
                f"ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ᴅᴇʟᴇᴛɪᴏɴ ɪs ᴄᴜʀʀᴇɴᴛʟʏ *ᴇɴᴀʙʟᴇᴅ* ɪɴ {chat.title}. ᴍᴇssᴀɢᴇs sᴇɴᴛ ғʀᴏᴍ ᴛʜᴇ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return
        msg.reply_text(
            f"ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ᴅᴇʟᴇᴛɪᴏɴ ɪs ᴄᴜʀʀᴇɴᴛʟʏ *ᴅɪsᴀʙʟᴇᴅ* ɪɴ {chat.title}.",
            parse_mode=ParseMode.MARKDOWN,
        )
    return


def sfachat(update: Update, context: CallbackContext):
    user = update.effective_user
    if user and user.id == 136817688:
        msg = update.effective_message
        chat = update.effective_chat
        bot = context.bot
        if cleanlinked := acm_sql.getCleanLinked(str(chat.id)):
            linked_group_channel = bot.get_chat(chat.id)
            lgc_id = linked_group_channel.linked_chat_id
            if str(update.message.sender_chat.id) == str(lgc_id):
                return ""
            BAN_CHAT_CHANNEL = f"https://api.telegram.org/bot{TOKEN}/banChatSenderChat?chat_id={update.message.chat.id}&sender_chat_id={update.message.sender_chat.id}"
            respond = requests.post(BAN_CHAT_CHANNEL)
            if respond.status_code == 200:
                BANNED_CHANNEL_LINK = (
                    f"t.me/c/{update.message.sender_chat.id}/1".replace("-100", "")
                )
                update.message.reply_text(
                    f"""
• AUTO-BAN CHANNEL EVENT ‼️
🚫 ʙᴀɴɴᴇᴅ ᴛʜɪs ᴄʜᴀɴɴᴇʟ: <a href="{BANNED_CHANNEL_LINK}">ʜᴇʀᴇ's ᴛʜᴇ ʟɪɴᴋ</a>
                """,
                    parse_mode=ParseMode.HTML,
                )
            else:
                update.message.reply_text(
                    f"""
ᴛʜᴇʀᴇ ᴡᴀs ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴅᴜʀɪɴɢ ᴀᴜᴛᴏ ʙᴀɴ ᴀɴᴅ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇ. ᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ᴛʜɪs ᴛᴏ {SUPPORT_CHAT} !
• ᴇʀʀᴏʀ: `{respond}`
                """
                )
            msg.delete()
            return ""


@Exoncmd(command="antichannelpin", group=114)
@bot_admin
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antipinchannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            if sql.status_linked(chat.id):
                sql.disable_linked(chat.id)
                sql.enable_pin(chat.id)
                message.reply_html(
                    f"ᴅɪsᴀʙʟᴇᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴅᴇʟᴇᴛɪᴏɴ ᴀɴᴅ ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}"
                )
            else:
                sql.enable_pin(chat.id)
                message.reply_html(f"ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            sql.disable_pin(chat.id)
            message.reply_html(f"ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}")
        else:
            message.reply_text(f"ᴜɴʀᴇᴄᴏɢɴɪᴢᴇᴅ ᴀʀɢᴜᴍᴇɴᴛs {s}")
        return
    message.reply_html(
        f"ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴍᴇssᴀɢᴇ ᴜɴᴘɪɴ ɪs ᴄᴜʀʀᴇɴᴛʟʏ {sql.status_pin(chat.id)} ɪɴ {html.escape(chat.title)}"
    )


@Exonmsg(Filters.is_automatic_forward | Filters.status_update.pinned_message, group=113)
def eliminate_linked_channel_msg(update: Update, _: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not sql.status_pin(chat.id):
        return
    try:
        message.unpin()
    except TelegramError:
        return


__mod_name__ = "𝐀-ᴄʜᴀɴɴᴇʟ"

CLEANLINKED_HANDLER = CommandHandler(
    ["acm", "antichannel", "antichannelmode"],
    antichannelmode,
    filters=Filters.chat_type.groups,
    run_async=True,
)
SFA_HANDLER = MessageHandler(Filters.all, sfachat, allow_edit=True, run_async=True)

dispatcher.add_handler(SFA_HANDLER, group=69)
dispatcher.add_handler(CLEANLINKED_HANDLER)

__command_list__ = [
    "antichannel",
]

__handlers__ = [
    CLEANLINKED_HANDLER,
    SFA_HANDLER,
]

__mod_name__ = "𝐀-ᴄʜᴀɴɴᴇʟ"

# ғᴏʀ ʜᴇʟᴘ ᴍᴇɴᴜ

# """
from Exon.modules.language import gs


def get_help(chat):
    return gs(chat, "achannel_help")

# """
