import importlib
from typing import Union

from future.utils import string_types
from telegram import ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    RegexHandler,
)
from telegram.utils.helpers import escape_markdown

from gabby import dispatcher
from .modules.helper_funcs.handlers import CMD_STARTERS, SpamChecker
from .modules.helper_funcs.misc import is_module_loaded

FILENAME = __name__.rsplit(".", 1)[-1]

# If module is due to be loaded, then setup all the magical handlers
if is_module_loaded(FILENAME):
    from gabby.gabby_modules.helper_funcs.chat_status import (
        connection_status,
        is_user_admin,
        user_admin,
    )
    from gabby.gabby_modules.sql import disable_sql as sql

    DISABLE_CMDS = []
    DISABLE_OTHER = []
    ADMIN_CMDS = []


    class DisableAbleCommandHandler(CommandHandler):
        def __init__(self, command, callback, admin_ok=False, **kwargs):
            super().__init__(command, callback, **kwargs)
            self.admin_ok = admin_ok
            if isinstance(command, string_types):
                DISABLE_CMDS.append(command)
                if admin_ok:
                    ADMIN_CMDS.append(command)
            else:
                DISABLE_CMDS.extend(command)
                if admin_ok:
                    ADMIN_CMDS.extend(command)

        def check_update(self, update):
            if not isinstance(update, Update) or not update.effective_message:
                return
            message = update.effective_message

            if message.text and len(message.text) > 1:
                fst_word = message.text.split(None, 1)[0]
                if len(fst_word) > 1 and any(
                        fst_word.startswith(start) for start in CMD_STARTERS
                ):
                    args = message.text.split()[1:]
                    command = fst_word[1:].split("@")
                    command.append(message.bot.username)

                    if (
                            command[0].lower() not in self.command
                            or command[1].lower() != message.bot.username.lower()
                    ):
                        return None
                    chat = update.effective_chat
                    user = update.effective_user
                    user_id = chat.id if user.id == 1087968824 else user.id
                    if SpamChecker.check_user(user_id):
                        return None
                    if filter_result := self.filters(update):
                        # disabled, admincmd, user admin
                        if sql.is_command_disabled(chat.id, command[0].lower()):
                            # check if command was disabled
                            is_disabled = command[0] in ADMIN_CMDS and is_user_admin(
                                chat, user.id
                            )
                            return (args, filter_result) if is_disabled else None
                        return args, filter_result
                    return False


    class DisableAbleMessageHandler(MessageHandler):
        def __init__(self, filters, callback, friendly, **kwargs):
            super().__init__(filters, callback, **kwargs)
            DISABLE_OTHER.append(friendly)
            self.friendly = friendly
            if filters:
                self.filters = Filters.update.messages & filters
            else:
                self.filters = Filters.update.messages

        def check_update(self, update):
            chat = update.effective_chat
            message = update.effective_message
            filter_result = self.filters(update)

            try:
                args = message.text.split()[1:]
            except Exception:
                args = []

            if super().check_update(update):
                if sql.is_command_disabled(chat.id, self.friendly):
                    return False
                return args, filter_result


    class DisableAbleRegexHandler(RegexHandler):
        def __init__(self, pattern, callback, friendly="", filters=None, **kwargs):
            super().__init__(pattern, callback, filters, **kwargs)
            DISABLE_OTHER.append(friendly)
            self.friendly = friendly

        def check_update(self, update):
            chat = update.effective_chat
            if super().check_update(update):
                return not sql.is_command_disabled(chat.id, self.friendly)


    @connection_status
    @user_admin
    def disable(update: Update, context: CallbackContext):
        args = context.args
        if len(args) >= 1:
            disable_cmd = args[0]
            if disable_cmd.startswith(CMD_STARTERS):
                disable_cmd = disable_cmd[1:]

            if disable_cmd in set(DISABLE_CMDS + DISABLE_OTHER):
                chat = update.effective_chat
                sql.disable_command(chat.id, str(disable_cmd).lower())
                update.effective_message.reply_text(
                    f"Disabled the use of `{disable_cmd}`",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                update.effective_message.reply_text("That command can't be disabled")

        else:
            update.effective_message.reply_text("What should I disable?")


    @connection_status
    @user_admin
    def disable_module(update: Update, context: CallbackContext):
        args = context.args
        if len(args) >= 1:
            disable_module = "gabby.gabby_modules." + args[0].rsplit(".", 1)[0]

            try:
                module = importlib.import_module(disable_module)
            except Exception:
                update.effective_message.reply_text("Does that module even exist?")
                return

            try:
                command_list = module.__command_list__
            except Exception:
                update.effective_message.reply_text(
                    "Module does not contain command list!",
                )
                return

            disabled_cmds = []
            failed_disabled_cmds = []

            chat = update.effective_chat
            for disable_cmd in command_list:
                if disable_cmd.startswith(CMD_STARTERS):
                    disable_cmd = disable_cmd[1:]

                if disable_cmd in set(DISABLE_CMDS + DISABLE_OTHER):
                    sql.disable_command(chat.id, str(disable_cmd).lower())
                    disabled_cmds.append(disable_cmd)
                else:
                    failed_disabled_cmds.append(disable_cmd)

            if disabled_cmds:
                disabled_cmds_string = ", ".join(disabled_cmds)
                update.effective_message.reply_text(
                    f"Disabled the uses of `{disabled_cmds_string}`",
                    parse_mode=ParseMode.MARKDOWN,
                )

            if failed_disabled_cmds:
                failed_disabled_cmds_string = ", ".join(failed_disabled_cmds)
                update.effective_message.reply_text(
                    f"Commands `{failed_disabled_cmds_string}` can't be disabled",
                    parse_mode=ParseMode.MARKDOWN,
                )

        else:
            update.effective_message.reply_text("What should I disable?")


    @connection_status
    @user_admin
    def enable(update: Update, context: CallbackContext):
        args = context.args
        if len(args) >= 1:
            enable_cmd = args[0]
            if enable_cmd.startswith(CMD_STARTERS):
                enable_cmd = enable_cmd[1:]

            chat = update.effective_chat
            if sql.enable_command(chat.id, enable_cmd):
                update.effective_message.reply_text(
                    f"Enabled the use of `{enable_cmd}`",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                update.effective_message.reply_text("Is that even disabled?")

        else:
            update.effective_message.reply_text("What should I enable?")


    @connection_status
    @user_admin
    def enable_module(update: Update, context: CallbackContext):
        args = context.args
        if len(args) >= 1:
            enable_module = "gabby.gabby_modules." + args[0].rsplit(".", 1)[0]

            try:
                module = importlib.import_module(enable_module)
            except Exception:
                update.effective_message.reply_text("Does that module even exist?")
                return

            try:
                command_list = module.__command_list__
            except Exception:
                update.effective_message.reply_text(
                    "Module does not contain command list!",
                )
                return

            enabled_cmds = []
            failed_enabled_cmds = []

            chat = update.effective_chat

            for enable_cmd in command_list:
                if enable_cmd.startswith(CMD_STARTERS):
                    enable_cmd = enable_cmd[1:]

                if sql.enable_command(chat.id, enable_cmd):
                    enabled_cmds.append(enable_cmd)
                else:
                    failed_enabled_cmds.append(enable_cmd)

            if enabled_cmds:
                enabled_cmds_string = ", ".join(enabled_cmds)
                update.effective_message.reply_text(
                    f"Enabled the uses of `{enabled_cmds_string}`",
                    parse_mode=ParseMode.MARKDOWN,
                )

            if failed_enabled_cmds:
                failed_enabled_cmds_string = ", ".join(failed_enabled_cmds)
                update.effective_message.reply_text(
                    f"Are the commands `{failed_enabled_cmds_string}` even disabled?",
                    parse_mode=ParseMode.MARKDOWN,
                )

        else:
            update.effective_message.reply_text("What should I enable?")


    @connection_status
    @user_admin
    def list_cmds(update: Update, context: CallbackContext):
        if DISABLE_CMDS + DISABLE_OTHER:
            result = "".join(
                f" - `{escape_markdown(cmd)}`\n"
                for cmd in set(DISABLE_CMDS + DISABLE_OTHER)
            )

            update.effective_message.reply_text(
                f"The following commands are toggleable:\n{result}",
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            update.effective_message.reply_text("No commands can be disabled.")


    # do not async
    def build_curr_disabled(chat_id: Union[str, int]) -> str:
        disabled = sql.get_all_disabled(chat_id)
        if not disabled:
            return "No commands are disabled!"

        result = "".join(f" - `{escape_markdown(cmd)}`\n" for cmd in disabled)
        return f"The following commands are currently restricted:\n{result}"


    @connection_status
    def commands(update: Update, context: CallbackContext):
        chat = update.effective_chat
        update.effective_message.reply_text(
            build_curr_disabled(chat.id),
            parse_mode=ParseMode.MARKDOWN,
        )


    def __stats__():
        return f"× {sql.num_disabled()} ᴅɪsᴀʙʟᴇᴅ ɪᴛᴇᴍs, ᴀᴄʀᴏss {sql.num_chats()} ᴄʜᴀᴛs."


    def __migrate__(old_chat_id, new_chat_id):
        sql.migrate_chat(old_chat_id, new_chat_id)


    def __chat_settings__(chat_id, user_id):
        return build_curr_disabled(chat_id)


    DISABLE_HANDLER = CommandHandler("disable", disable, run_async=True)
    DISABLE_MODULE_HANDLER = CommandHandler(
        "disablemodule", disable_module, run_async=True
    )
    ENABLE_HANDLER = CommandHandler("enable", enable, run_async=True)
    ENABLE_MODULE_HANDLER = CommandHandler(
        "enablemodule", enable_module, run_async=True
    )
    COMMANDS_HANDLER = CommandHandler(["cmds", "disabled"], commands, run_async=True)
    TOGGLE_HANDLER = CommandHandler("listcmds", list_cmds, run_async=True)

    dispatcher.add_handler(DISABLE_HANDLER)
    dispatcher.add_handler(DISABLE_MODULE_HANDLER)
    dispatcher.add_handler(ENABLE_HANDLER)
    dispatcher.add_handler(ENABLE_MODULE_HANDLER)
    dispatcher.add_handler(COMMANDS_HANDLER)
    dispatcher.add_handler(TOGGLE_HANDLER)


else:
    DisableAbleCommandHandler = CommandHandler
    DisableAbleRegexHandler = RegexHandler
    DisableAbleMessageHandler = MessageHandler
