import random

from telegram import ParseMode
from telethon import Button

from Exon import OWNER_ID, SUPPORT_CHAT
from Exon import telethn as tbot
from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    Exon = (
        "https://telegra.ph/file/753bfe51f0e0314f1f3ff.jpg",
        "https://telegra.ph/file/20bab4a499d6dccd823f1.jpg",
        "https://telegra.ph/file/2ef1c255ac51d9febb3f4.jpg",
        "https://telegra.ph/file/bc3a10df7c66e6333bba6.jpg",
        "https://telegra.ph/file/bf283996f928a6ab5b625.jpg",
        "https://telegra.ph/file/bf283996f928a6ab5b625.jpg",
        "https://telegra.ph/file/43b4f5a5645ab1cd1dd7c.jpg",
        "https://telegra.ph/file/0f5240ad4d50d5dac57fe.jpg",
        "https://telegra.ph/file/f6128a7a197cf088ba5e0.jpg",
        "https://telegra.ph/file/53d0320dcaa0d21da19c0.jpg",
        "https://telegra.ph/file/fc988e9441acfb5fe71a7.jpg",
        "https://telegra.ph/file/731387573fd96e3cfc2f5.jpg",
        "https://telegra.ph/file/6c9951e14cece66f2fc3a.jpg",
    )
    NATFEED = ("https://telegra.ph/file/2dd04f407b16bc2cfdf76.jpg",)
    BUTTON = [[Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "ᴛʜᴀɴᴋꜱ ꜰᴏʀ ʏᴏᴜʀ ꜰᴇᴇᴅʙᴀᴄᴋ, ɪ ʜᴏᴘᴇ ʏᴏᴜ ʜᴀᴘᴘʏ ᴡɪᴛʜ ᴏᴜʀ ꜱᴇʀᴠɪᴄᴇ."
    logger_text = f"""
**ɴᴇᴡ ꜰᴇᴇᴅʙᴀᴄᴋ**

**ꜰʀᴏᴍ ᴜꜱᴇʀ:** {mention}
**ᴜꜱᴇʀɴᴀᴍᴇ:** @{e.sender.username}
**ᴜꜱᴇʀ ɪᴅ:** `{e.sender.id}`
**ꜰᴇᴇᴅʙᴀᴄᴋ:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        GIVE = "ɢɪᴠᴇ ꜱᴏᴍᴇ ᴛᴇxᴛ ꜰᴏʀ ꜰᴇᴇᴅʙᴄᴋ ✨"
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(NATFEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(Exon),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(Exon), buttons=BUTTON)
