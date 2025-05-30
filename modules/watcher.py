import re
import time

from Abg.helpers.human_read import get_readable_time
from pyrogram import filters
from pyrogram.enums import MessageEntityType

from gabby_main import Abishnoi as app

chat_watcher_group = 1


@app.on_message(
    ~filters.me & ~filters.bot & ~filters.via_bot,
    group=chat_watcher_group,
)
async def chat_watcher_func(c: app, message):
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.first_name
    if message.entities:
        possible = ["/afk", f"/afk@{c.me.username}"]
        message_text = message.text or message.caption
        for entity in message.entities:
            if entity.type == MessageEntityType.BOT_COMMAND and message_text[: 0 + entity.length].lower() in possible:
                return

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "animation":
                send = (
                    await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n",
                    )
                    if str(reasonafk) == "None"
                    else await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                    )
                )
            elif afktype == "photo":
                send = (
                    await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n",
                    )
                    if str(reasonafk) == "None"
                    else await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                    )
                )
            elif afktype == "text":
                msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n"
            elif afktype == "text_reason":
                msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
        except Exception:
            msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ\n\n"

    # Replied to a User which is AFK
    if message.reply_to_message:
        try:
            replied_first_name = message.reply_to_message.from_user.first_name
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time((int(time.time() - timeafk)))
                    if afktype == "animation":
                        send = (
                            await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",
                            )
                            if str(reasonafk) == "None"
                            else await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                            )
                        )
                    elif afktype == "photo":
                        send = (
                            await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",
                            )
                            if str(reasonafk) == "None"
                            else await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                            )
                        )
                    elif afktype == "text":
                        msg += (
                            f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                        )
                    elif afktype == "text_reason":
                        msg += f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
                except Exception:
                    msg += f"**{replied_first_name}** ɪs ᴀғᴋ,\nᴩᴀᴛᴀ ɴɪ ʙᴄ ᴋᴀʙ sᴇ\n\n"
        except Exception:
            pass

    if message.entities:
        entity = message.entities
        j = 0
        for _ in range(len(entity)):
            if (entity[j].type) == MessageEntityType.MENTION:
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except Exception:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        if afktype == "animation":
                            send = (
                                await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",
                                )
                                if str(reasonafk) == "None"
                                else await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                                )
                            )
                        elif afktype == "photo":
                            send = (
                                await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",
                                )
                                if str(reasonafk) == "None"
                                else await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                                )
                            )
                        elif afktype == "text":
                            msg += (
                                f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                            )
                        elif afktype == "text_reason":
                            msg += f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
                    except Exception:
                        msg += f"**{user.first_name[:25]}** ɪs ᴀғᴋ\n\n"
            elif (entity[j].type) == MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except Exception:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        if afktype == "animation":
                            send = (
                                await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",
                                )
                                if str(reasonafk) == "None"
                                else await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]}** ɪs AFK sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                                )
                            )
                        elif afktype == "photo":
                            send = (
                                await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",
                                )
                                if str(reasonafk) == "None"
                                else await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n",
                                )
                            )
                        elif afktype == "text":
                            msg += f"**{first_name[:25]}** is ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                        elif afktype == "text_reason":
                            msg += f"**{first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
                    except Exception:
                        msg += f"**{first_name[:25]}** ɪs ᴀғᴋ\n\n"
            j += 1
    if msg != "":
        try:
            send = await message.reply_text(msg, disable_web_page_preview=True)
        except Exception:
            return
