import asyncio
import logging
from asyncio
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,  
    ContextTypes
)

TOKEN = "
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



KEYWORD_RESPONSES = {
    "привет": "Приветствую! 👋",
    "как дела": "Отлично! Как сам?",
    "пока": "До скорой встречи!",
    "кнопки": "Вот варианты:",
}


def get_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Привет"), KeyboardButton("Пока")],
            [KeyboardButton("Помощь")]
        ],
        resize_keyboard=True
    )


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Я бот-пример! Напиши мне что-нибудь или используй кнопки:",
        reply_markup=get_keyboard()
    )


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать диалог\n"
        "/help - помощь\n\n"
        "Ключевые слова: " + ", ".join(KEYWORD_RESPONSES.keys())
    )


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    

    for keyword, response in KEYWORD_RESPONSES.items():
        if keyword in text:
            update.message.reply_text(response)
            return
    
    
    update.message.reply_text(
        "Я не понял. Попробуй:\n" + "\n".join([f"- {kw}" for kw in KEYWORD_RESPONSES.keys()]),
        reply_markup=get_keyboard()
    )



def error(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error {context.error}')


# Запуск бота
# def main():
#     updater = Updater(TOKEN, use_context=True)
#     dp = updater.dispatcher

async def main():
    logger.add("file.log",
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation="3 days",
            backtrace=True,
            diagnose=True)

    bot = Bot(TOKEN)
    logger.info("Бот создан")
    dp = Dispatcher()
    logger.info("Диспетчер создан")

    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    
    dp.add_handler(MessageHandler(filters.text & ~filters.command, handle_message))

    
    dp.add_error_handler(error)

    
    updater.start_polling()
    logger.info("Бот запущен!")
    updater.idle()

if __name__ == '__main__':
    asyncio.run(main())
