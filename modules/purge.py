from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError
from pyrogram.types import Message

from gabby_main import LOGGER, Abishnoi


@gabby.on_cmd("purge")
@gabby.adminsOnly(permissions="can_delete_messages", is_both=True)
async def purge(c: Abishnoi, m: Message):
    if m.chat.type != ChatType.SUPERGROUP:
        await m.reply_text(text="ᴄᴀɴɴᴏᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ")
        return

    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.id, m.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i: i + n]

        # Dielete messages in chunks of 100 messages
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text(
                text="ᴄᴀɴɴᴏᴛ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇs. ᴛʜᴇ ᴍᴇssᴀɢᴇs ᴍᴀʏ ʙᴇ ᴛᴏᴏ ᴏʟᴅ, I ᴍɪɢʜᴛ ɴᴏᴛ ʜᴀᴠᴇ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs, ᴏʀ ᴛʜɪs ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ."
            )
            return
        except RPCError as ef:
            LOGGER.info(f"ERROR on purge {ef}")

        count_del_msg = len(message_ids)

        z = await m.reply_text(text=f"ᴅᴇʟᴇᴛᴇᴅ <i>{count_del_msg}</i> messages")
        return
    await m.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢᴇ !")
    return


@gabby.on_cmd("spurge")
@gabby.adminsOnly(permissions="can_delete_messages", is_both=True)
async def spurge(c: Abishnoi, m: Message):
    if m.chat.type != ChatType.SUPERGROUP:
        await m.reply_text(text="ᴄᴀɴɴᴏᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ")
        return

    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.id, m.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i: i + n]

        # Dielete messages in chunks of 100 messages
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text(
                text="ᴄᴀɴɴᴏᴛ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇs. ᴛʜᴇ ᴍᴇssᴀɢᴇs ᴍᴀʏ ʙᴇ ᴛᴏᴏ ᴏʟᴅ, I ᴍɪɢʜᴛ ɴᴏᴛ ʜᴀᴠᴇ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs, ᴏʀ ᴛʜɪs ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ."
            )
            return
        except RPCError as ef:
            LOGGER.info(f"ERROR on purge {ef}")
        return
    await m.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ sᴘᴜʀɢᴇ !")
    return


@gabby.on_cmd("del")
@gabby.adminsOnly(permissions="can_delete_messages", is_both=True)
async def del_msg(c: Abishnoi, m: Message):
    if m.reply_to_message:
        await m.delete()
        await c.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.reply_to_message.id,
        )
    else:
        await m.reply_text(text="ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴇʟᴇᴛᴇ?")
    return


__PLUGIN__ = "Pᴜʀɢᴇ"

__alt_name__ = ["purge", "del", "spurge"]

__HELP__ = """
• /purge: ᴅᴇʟᴇᴛᴇs ᴍᴇssᴀɢᴇs ᴜᴘᴛᴏ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.
• /spurge: ᴅᴇʟᴇᴛᴇs ᴍᴇssᴀɢᴇs ᴜᴘᴛᴏ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ᴡɪᴛʜᴏᴜᴛ ᴀ sᴜᴄᴄᴇss ᴍᴇssᴀɢᴇ.
• /del: ᴅᴇʟᴇᴛᴇs ᴀ sɪɴɢʟᴇ ᴍᴇssᴀɢᴇ, ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ.
"""

__mod_name__ = "𝐏ᴜʀɢᴇ"

# ғᴏʀ ʜᴇʟᴘ ᴍᴇɴᴜ

def get_help(chat):
    return gs(chat, "purge_help")

# """
