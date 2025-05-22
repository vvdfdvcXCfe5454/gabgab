import re
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    LOGGER = True
    # Telegram API
    API_ID = int(getenv("27127173"))
    API_HASH = getenv("3f27c305ecc299c385bdf619a4805f1d")
    TOKEN = getenv("7948653467:AAFEEmG-oACMJ9koHM6LRh0nW5X-8jwqbos")
    OWNER_ID = getenv("7458177381")
    OWNER_USERNAME = getenv("@Gabby_Ssno")
    SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+2eSB8BA91UFmZGI1")
    LOGGER_ID = int(getenv("LOGGER_ID", 0))
    START_IMG = getenv("START_IMG", "https://a.imgfoto.host/2025/05/22/renantee_-photo-DJoHpcYRbgSZ56iz7MbRHhdltZX0Ke4FayIzdw0-20250514_161341_4968605931.jpeg")
    BOT_NAME = int(getenv("", ""))

    # Database
    MONGO_DB_URI = getenv("mongodb+srv://gabby:%40Drawing5112004@cluster0.e9udyr8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DATABASE_URL = getenv("https://cloud.mongodb.com/v2/682efb481692fc359303b636#/metrics/replicaSet/682efb9e5759cc1c2e1ce893/explorer/Gab_Games", "https://cloud.mongodb.com/v2/682efb481692fc359303b636#/metrics/replicaSet/682efb9e5759cc1c2e1ce893/explorer/Gab_Mod", "https://cloud.mongodb.com/v2/682efb481692fc359303b636#/metrics/replicaSet/682efb9e5759cc1c2e1ce893/explorer/Gab_Music")
    DB_NAME = getenv("Gab_Games", "Gab_Mod", "Gab_Music")

    #
    TIME_API_KEY = getenv("VWF2Y24GHC7G")
    SPOTIFY_CLIENT_ID = getenv("f52ec79b8126404c874413b9eaffe415")
    SPOTIFY_CLIENT_SECRET = getenv("7b2555b0d4ea4000adca41d15d3e6c60")


    # 
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

    # --- ASSISTANT BOT TOKEN PLACEHOLDER ---
    # To use the assistant bot, add your assistant bot token here or in your .env file as ASSISTANT_TOKEN
    ASSISTANT_TOKEN = getenv("ASSISTANT_TOKEN", "7444056348:AAH3xFILWDhq6F_62s26bPRHbzuLWuFJasY")  # <--- PUT YOUR ASSISTANT BOT TOKEN HERE

class Production(Config):
    LOGGER = True

class Development(Config):
    LOGGER = True
