import re
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    LOGGER = True
    # Telegram API
    API_ID = int(getenv("27127173", 12345))
    API_HASH = getenv("3f27c305ecc299c385bdf619a4805f1d", "")
    TOKEN = getenv("TOKEN", getenv("7948653467:AAFEEmG-oACMJ9koHM6LRh0nW5X-8jwqbos", ""))
    OWNER_ID = int(getenv("7458177381", 0))
    OWNER_USERNAME = getenv("@Gabby_Ssno", "Gabby")
    SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+2eSB8BA91UFmZGI1")
    LOGGER_ID = int(getenv("LOGGER_ID", 0))
    START_IMG = getenv("START_IMG", "https://a.imgfoto.host/2025/05/22/renantee_-photo-DJoHpcYRbgSZ56iz7MbRHhdltZX0Ke4FayIzdw0-20250514_161341_4968605931.jpeg")
    BOT_NAME = getenv("BOT_NAME", "Gabby")

    # Database
    MONGO_DB_URI = getenv("MONGO_DB_URI", None)
    DATABASE_URL = getenv("DATABASE_URL", None)
    DB_NAME = getenv("DB_NAME", "GabbyBot")
    REDIS_URL = getenv("REDIS_URL", None)

    # API Keys
    ARQ_API_KEY = getenv("ARQ_API_KEY", None)
    CASH_API_KEY = getenv("CASH_API_KEY", None)
    TIME_API_KEY = getenv("TIME_API_KEY", None)
    SPAMWATCH_API = getenv("SPAMWATCH_API", None)
    SPOTIFY_CLIENT_ID = getenv("f52ec79b8126404c874413b9eaffe415")
    SPOTIFY_CLIENT_SECRET = getenv("7b2555b0d4ea4000adca41d15d3e6c60")

    # Heroku
    HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
    HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)

    # Limits & Features
    DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))
    AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = int(getenv("WORKERS", 8))
    BL_CHATS = []
    DRAGONS = []
    DEV_USERS = []
    DEMONS = []
    TIGERS = []
    WOLVES = []

class Production(Config):
    LOGGER = True

class Development(Config):
    LOGGER = True
