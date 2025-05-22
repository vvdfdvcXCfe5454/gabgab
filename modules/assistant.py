# Gabby Assistant Module
# This module provides flirty, sexy, and helpful assistant features for Gabby.

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from Gabby.gabby_config import Config

ASSISTANT_START_TEXT = (
    "Hey there, gorgeous! 😘\n"
    "I'm Gabby, your flirty, sexy, and oh-so-helpful assistant.\n"
    "Need something? Just ask! 💋"
)

ASSISTANT_BUTTONS = [
    [InlineKeyboardButton("💖 Gabby Help 💖", callback_data="help_back")],
    [InlineKeyboardButton("🌹 About Gabby 🌹", callback_data="GABBY_ABOUT")],
]

def assistant_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        ASSISTANT_START_TEXT,
        reply_markup=InlineKeyboardMarkup(ASSISTANT_BUTTONS),
        parse_mode=ParseMode.MARKDOWN,
    )

def setup(dispatcher):
    dispatcher.add_handler(CommandHandler("gabby", assistant_start))
    # Optionally, add more flirty/assistant commands here
