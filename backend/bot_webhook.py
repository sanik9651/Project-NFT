import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import uvicorn

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://yourdomain.com")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://project-nft.onrender.com")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

# FastAPI app
app = FastAPI()

# Telegram bot
telegram_app = Application.builder().token(BOT_TOKEN).build()

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

    await update.message.reply_text(message_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🦦 **Telegram NFT Transfer Bot**\n\n"
        "**Команды:**\n"
        "/start - Получить ссылку для перевода NFT\n"
        "/help - Показать это сообщение\n\n"
        "💎 Работает только с Telegram NFT на TON блокчейне"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))

@app.post(f"/telegram-webhook/{BOT_TOKEN}")
async def telegram_webhook(request: Request):
    """Обработка webhook от Telegram"""
    json_data = await request.json()
    update = Update.de_json(json_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    """Установка webhook при запуске"""
    webhook_url = f"{WEBHOOK_URL}/telegram-webhook/{BOT_TOKEN}"
    await telegram_app.bot.set_webhook(url=webhook_url)
    await telegram_app.initialize()
    logger.info(f"Webhook установлен: {webhook_url}")

@app.on_event("shutdown")
async def on_shutdown():
    """Удаление webhook при остановке"""
    await telegram_app.bot.delete_webhook()
    await telegram_app.shutdown()
    logger.info("Webhook удалён")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
