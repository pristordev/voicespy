import nextcord
from nextcord.ext import commands
import json
import os
import dotenv

dotenv.load_dotenv()

# Параметры подключения
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SHEET_NAME = "users_audit"  # Укажи имя таблицы, куда будет происходить запись
COGS_FOLDER = "cogs"  # Папка с COGs
CONFIG_FILE = "config.json"  # Файл конфигурации
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

def load_tracked_channels():
    if os.path.exists("tracked_channels.json"):
        with open("tracked_channels.json", "r") as file:
            return set(json.load(file))
    return set()

# Функция сохранения отслеживаемых каналов
def save_tracked_channels(channels):
    with open("tracked_channels.json", "w") as file:
        json.dump(list(channels), file, indent=4)

# Инициализация отслеживаемых каналов
tracked_channels = load_tracked_channels()