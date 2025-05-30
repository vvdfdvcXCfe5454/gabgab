import asyncio
import os

from telethon import types

from gabby_main import Abishnoi as gabby
from gabby_main import telethon as Client
from .events import register

TMP_DOWNLOAD_DIRECTORY = "./"

from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

wibu = "gabby_main_Robot"
telegraph = Telegraph()
data = telegraph.create_account(short_name=wibu)
auth_url = data["auth_url"]


@register(pattern="^/tm$")
async def _(event):
    loda = "use\n➥ `/tgm` (reply to media)\n➥ `/tgt` (reply to text)"
    lund = await event.reply(loda)
    await asyncio.sleep(10)
    await event.delete()
    await lund.delete()


@register(pattern="^/t(gm|gt) ?(.*)")
async def telegrap(event):
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_msg = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "gm":
            downloaded_file_name = await Client.download_media(
                reply_msg, TMP_DOWNLOAD_DIRECTORY
            )
            a = await asau.get_me()
            end = datetime.now()
            ms = (end - start).seconds
            if not downloaded_file_name:
                await Client.send_message(event.chat_id, "ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛ ᴍᴇᴅɪᴀ!")
                return
            else:
                if downloaded_file_name.endswith((".webp")):
                    resize_image(downloaded_file_name)
                try:
                    start = datetime.now()
                    media_urls = upload_file(downloaded_file_name)

                except exceptions.TelegraphException as exc:
                    await event.reply(f"ERROR: {str(exc)}")
                    os.remove(downloaded_file_name)
                else:
                    end = datetime.now()
                    ms_two = (end - start).seconds
                    os.remove(downloaded_file_name)
                    await Client.send_message(
                        event.chat_id,
                        f"`ᴅᴏɴᴇ`!\n**•ʀᴇϙᴜᴇꜱᴛᴇᴅ ʙʏ:**- [{event.sender.first_name}](tg://user?id={event.sender.id})\n**•ᴜᴘʟᴏᴀᴅ ʙʏ:** [{a.first_name}](tg://user?id={a.id})\n**•ʟɪɴᴋ: **`https://telegra.ph{media_urls[0]}` ",
                        buttons=[
                            [
                                types.KeyboardButtonUrl(
                                    "➡ ʙʀᴏᴡsᴇʀ ᴠɪᴇᴡ",
                                    f"https://telegra.ph{media_urls[0]}",
                                )
                            ]
                        ],
                    )
        elif input_str == "gt":
            user_object = await Client.get_entity(reply_msg.sender_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = reply_msg.message
            if reply_msg.media:
                if page_content != "":
                    title_of_page = page_content
                else:
                    await Client.send_message(
                        event.chat_id, "ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛ ᴛᴇxᴛ!"
                    )
                downloaded_file_name = await Client.download_media(
                    reply_msg, TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            a = await asau.get_me()
            end = datetime.now()
            ms = (end - start).seconds
            url = f'https://telegra.ph/{response["path"]}'
            await Client.send_message(
                event.chat_id,
                f"ᴅᴏɴᴇ!\n**•ʀᴇϙᴜᴇꜱᴛᴇᴅ ʙʏ:-** [{event.sender.first_name}](tg://user?id={event.sender.id})\n**•ᴜᴘʟᴏᴀᴅ ʙʏ:-** [{a.first_name}](tg://user?id={a.id})\n**•ʟɪɴᴋ:** `{url}`",
                buttons=[
                    [
                        types.KeyboardButtonUrl(
                            "➡ ʙʀᴏᴡsᴇʀ ᴠɪᴇᴡ ",
                            f'https://telegra.ph/{response["path"]}',
                        )
                    ]
                ],
            )
    else:
        await event.reply("`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ telegra.ph link`")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__mod_name__ = "𝐓-ɢᴀᴘʜ"
