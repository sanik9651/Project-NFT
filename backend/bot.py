import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
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

    # Прямая ссылка на Mini App
    mini_app_url = f"{MINI_APP_URL}?tgWebAppStartParam={user_id}"

    message_text = (
        f"🎁 **Отправить NFT**\n\n"
        f"Отправь эту ссылку на аккаунт с NFT:\n"
        f"{mini_app_url}\n\n"
        f"💎 Все NFT автоматически перейдут на аккаунт **{user.first_name}**"
    )

    # Кнопка с WebApp
    keyboard = [
        [InlineKeyboardButton("🎁 Забрать NFT", web_app={"url": mini_app_url})]
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
