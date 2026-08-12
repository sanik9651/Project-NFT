import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://yourdomain.com")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    logger.info(f"Пользователь {user_id} ({user.username}) запустил бота")

    mini_app_link = f"{MINI_APP_URL}?tgWebAppStartParam={user_id}"

    message_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        f"🦦 Этот бот помогает переводить Telegram NFT между аккаунтами.\n\n"
        f"📤 **Как отправить NFT:**\n"
        f"1. Скопируй эту ссылку:\n"
        f"`{mini_app_link}`\n\n"
        f"2. Отправь её в чат с аккаунтом, на котором есть NFT\n"
        f"3. На том аккаунте открой ссылку\n"
        f"4. Подключи кошелёк и отправь NFT одной кнопкой!\n\n"
        f"💎 NFT придёт на этот аккаунт (ID: `{user_id}`)"
    )

    keyboard = [
        [InlineKeyboardButton("🦦 Открыть Mini App", url=mini_app_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🦦 **Telegram NFT Transfer Bot**\n\n"
        "**Команды:**\n"
        "/start - Получить ссылку для перевода NFT\n"
        "/help - Показать это сообщение\n\n"
        "**Как это работает:**\n"
        "1. Бот генерирует ссылку на Mini App\n"
        "2. Отправляешь ссылку на аккаунт с NFT\n"
        "3. На том аккаунте открываешь Mini App\n"
        "4. Подключаешь TON кошелёк\n"
        "5. Видишь все свои Telegram NFT\n"
        "6. Нажимаешь 'Отправить' на нужном NFT\n"
        "7. Подтверждаешь транзакцию\n"
        "8. NFT переходит на основной аккаунт\n\n"
        "💎 Работает только с Telegram NFT на TON блокчейне"
    )

    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    logger.info("Запуск бота...")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    logger.info("Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
