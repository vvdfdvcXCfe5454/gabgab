import html
import io
import random
import sys
import traceback

import pretty_errors
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext

from gabby_config import DEV_USERS
from gabby_config import LOG_GROUP_ID as ERROR_LOGS
from gabby import dispatcher
from gabby.modules.helper_funcs.decorators import gabbycmd

pretty_errors.mono()


class ErrorsDict(dict):
    """A custom dict to store errors and their count"""

    def __init__(self, *args, **kwargs):
        self.raw = []
        super().__init__(*args, **kwargs)

    def __contains__(self, error):
        self.raw.append(error)
        error.identifier = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))
        for e in self:
            if type(e) is type(error) and e.args == error.args:
                self[e] += 1
                return True
        self[error] = 0
        return False

    def __len__(self):
        return len(self.raw)


errors = ErrorsDict()


def error_callback(update: Update, context: CallbackContext):
    if not update:
        return
    if context.error not in errors:
        try:
            stringio = io.StringIO()
            pretty_errors.output_stderr = stringio
            output = pretty_errors.excepthook(
                type(context.error),
                context.error,
                context.error.__traceback__,
            )
            pretty_errors.output_stderr = sys.stderr
            pretty_error = stringio.getvalue()
            stringio.close()
        except Exception:
            pretty_error = "Failed to create pretty error."
        tb_list = traceback.format_exception(
            None,
            context.error,
            context.error.__traceback__,
        )
        tb = "".join(tb_list)
        pretty_message = f'{pretty_error}\n-------------------------------------------------------------------------------\nAn exception was raised while handling an update\nUser: {update.effective_user.id}\nChat: {update.effective_chat.title if update.effective_chat else ""} {update.effective_chat.id if update.effective_chat else ""}\nCallback data: {update.callback_query.data if update.callback_query else "None"}\nMessage: {update.effective_message.text if update.effective_message else "No message"}\n\nFull Traceback: {tb}'
        extension = "txt"
        url = "https://spaceb.in/api/v1/documents/"
        try:
            response = requests.post(
                url, data={"content": pretty_message, "extension": extension}
            )
        except Exception as e:
            return {"error": str(e)}
        response = response.json()
        e = html.escape(f"{context.error}")
        if not response:
            with open("error.txt", "w+") as f:
                f.write(pretty_message)
            context.bot.send_document(
                ERROR_LOGS,
                open("error.txt", "rb"),
                caption=f"#{context.error.identifier}\n<b>ʏᴏᴜʀ ᴄᴜᴛᴇ ᴇxᴏɴ ʜᴀᴠᴇ ᴀɴ ᴇʀʀᴏʀ ғᴏʀ ʏᴏᴜ:"
                        f"</b>\n<code>{e}</code>",
                parse_mode="html",
            )
            return

        url = f"https://spaceb.in/{response['payload']['id']}"
        context.bot.send_message(
            ERROR_LOGS,
            text=f"#{context.error.identifier}\n<b>Your Cute gabby Nagisa Have An Error For You:"
                 f"</b>\n<code>{e}</code>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("sᴇxʏ ᴇxᴏɴ ᴇʀʀᴏʀ ʟᴏɢs", url=url)]],
            ),
            parse_mode=ParseMode.HTML,
        )


@gabbycmd(command="errors")
def list_errors(update: Update, context: CallbackContext):
    if update.effective_user.id not in DEV_USERS:
        return
    e = dict(sorted(errors.items(), key=lambda item: item[1], reverse=True))
    msg = "<b>Errors List:</b>\n"
    for x, value in e.items():
        msg += f"× <code>{x}:</code> <b>{value}</b> #{x.identifier}\n"
    msg += f"{len(errors)} have occurred since startup."
    if len(msg) > 4096:
        with open("errors_msg.txt", "w+") as f:
            f.write(msg)
        context.bot.send_document(
            update.effective_chat.id,
            open("errors_msg.txt", "rb"),
            caption="Too many errors have occured..",
            parse_mode="html",
        )
        return
    update.effective_message.reply_text(msg, parse_mode="html")


dispatcher.add_error_handler(error_callback)
