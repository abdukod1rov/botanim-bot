import os

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import message_texts
from dotenv import load_dotenv
from books import get_all_books

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logger = logging.getLogger(__name__)

if not TELEGRAM_BOT_TOKEN:
    exit("PROVIDE the TELEGRAM_BOT_TOKEN!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning("effective_chat is None in /start")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_texts.GREETINGS)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning("effective_chat is None in /help")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_texts.HELP)


async def all_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning("effective_chat is None in /allbooks")
        return
    books_all_chunks = await get_all_books(chunk_size=60)
    for chunk in books_all_chunks:
        response = "\n".join((book.name for book in chunk))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    all_book_handler = CommandHandler('allbooks', all_books)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(all_book_handler)

    application.run_polling()
