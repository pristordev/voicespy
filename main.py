
# ==============================
# ИМПОРТЫ
# ==============================
from const import *  
import nextcord
from nextcord.ext import commands
import os
import logging
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ==============================
# НАСТРОЙКА ЛОГГЕРА
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 📋 %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True  # Принудительное включение логирования
)

# ==============================
# СОЗДАНИЕ ОБЪЕКТА БОТА
# ==============================
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)



@bot.slash_command(name="addvoice", description="Добавить голосовой канал в отслеживаемые")
async def addvoice(interaction: nextcord.Interaction, channel: nextcord.VoiceChannel):
    if not interaction.user.guild_permissions.administrator:
        # Проверка прав администратора
        embed = nextcord.Embed(
                title="❌ Ошибка",
                description="У вас нет прав для использования этой команды.",
                color=nextcord.Color.red()
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    tracked_channels.add(channel.id)
    save_tracked_channels(tracked_channels)
        
    # Уведомление об успешном добавлении канала
    embed = nextcord.Embed(
            title="✅ Канал добавлен",
            description=f"Голосовой канал `{channel.name}` был успешно добавлен в отслеживаемые.",
            color=nextcord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.slash_command(name="removevoice", description="Удалить голосовой канал из отслеживаемых")
async def removevoice(interaction: nextcord.Interaction, channel: nextcord.VoiceChannel):
    if not interaction.user.guild_permissions.administrator:
        # Проверка прав администратора
        embed = nextcord.Embed(
                title="❌ Ошибка",
                description="У вас нет прав для использования этой команды.",
                color=nextcord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    if channel.id in tracked_channels:
        tracked_channels.remove(channel.id)
        save_tracked_channels(tracked_channels)
            
        # Уведомление об успешном удалении канала
        embed = nextcord.Embed(
                title="✅ Канал удалён",
                description=f"Голосовой канал `{channel.name}` был успешно удалён из отслеживаемых.",
                color=nextcord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        # Канал не найден в списке
        embed = nextcord.Embed(
                title="⚠ Ошибка",
                description=f"Голосовой канал `{channel.name}` не найден в списке отслеживаемых.",
                color=nextcord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)




# ==============================
# ФУНКЦИЯ: bot_ready()
# Выводит информацию о запуске бота
# ==============================
def bot_ready(bot):
    header = "🚀 БОТ ГОТОВ К РАБОТЕ 🚀"
    author = "@pristordev"
    separator = "═" * 30

    logging.info(f"{author} | {header}\n{separator}\n"
                 f"🤖 Бот: {bot.user}\n"
                 f"🆔 ID: {bot.user.id}\n"
                 f"📅 Подключён к {len(bot.guilds)} серверам\n"
                 f"👥 Всего пользователей: {sum(g.member_count for g in bot.guilds)}\n {separator}\n")
    print(f"✅ Бот {bot.user} успешно запущен!")

# ==============================
# ОБРАБОТЧИК СОБЫТИЯ on_ready
# ==============================
@bot.event
async def on_ready():
    try:
        logging.info("✅ Слэш-команды успешно синхронизированы!")
        bot.add_application_command(addvoice, overwrite=True)
        bot.add_application_command(removevoice, overwrite=True)
    except Exception as e:
        logging.error(f"❌ Ошибка синхронизации слэш-команд: {e}")

    bot_ready(bot)

# ==============================
# ОБРАБОТЧИК СОБЫТИЯ on_voice_state_update
# ==============================
@bot.event
async def on_voice_state_update(member, before, after):
    # Проверка на отслеживаемые каналы
    if after.channel and after.channel.id in load_tracked_channels():
        # Время подключения
        join_time = datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y-%m-%d %H:%M:%S")
        leave_time = "N/A"  # Пока не оставил канал

        # Логирование в Google Sheets
        log_to_google_sheets(member.display_name, str(member.id), after.channel.name, "Зашёл", join_time, leave_time)

    if before.channel and before.channel.id in load_tracked_channels() and not after.channel:
        # Время отключения
        leave_time = datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y-%m-%d %H:%M:%S")
        join_time = "N/A"  # Пока не подключился

        # Логирование в Google Sheets
        log_to_google_sheets(member.display_name, str(member.id), before.channel.name, "Вышел", join_time, leave_time)

# ==============================
# ФУНКЦИЯ: log_to_google_sheets
# Запись данных в таблицу
# ==============================
def log_to_google_sheets(display_name, discord_id, channel_name, action, join_time, leave_time):
    try:
        sheet = connect_to_google_sheets()
        if sheet:
            row = [display_name, discord_id, channel_name, action, join_time, leave_time]  # Данные в виде списка
            sheet.append_row(row)  # Записывает данные в таблицу
            logging.info(f"✅ Данные записаны в таблицу: {row}")
        else:
            logging.error("❌ Не удалось записать данные, подключение к Google Sheets не установлено.")
    except Exception as e:
        logging.error(f"❌ Ошибка записи в Google Sheets: {e}")

# ==============================
# ФУНКЦИЯ: connect_to_google_sheets
# Подключение к Google Sheets
# ==============================
def connect_to_google_sheets():
    try:
        # Устанавливаем соединение с Google Sheets
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1  # Открываем таблицу по имени
        logging.info("✅ Успешное подключение к Google Sheets.")
        return sheet
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к Google Sheets: {e}")
        return None

# ==============================
# Запуск бота
# ==============================
print("🚀 Бот запускается...")
bot.run(TOKEN)