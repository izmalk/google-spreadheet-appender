#!/usr/bin/env python
import logging
import re
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import gspread_asyncio
from google.oauth2.service_account import Credentials


def find_urls(text):
    # Regular expression for matching URLs
    url_pattern = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    # Find all matches in the text
    urls = re.findall(url_pattern, text)
    # Return the URLs separated by whitespace
    return '\n'.join(urls)


async def add_row_async(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Set up the credentials
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('google-api-token.json', scopes=scope)

    agcm = gspread_asyncio.AsyncioGspreadClientManager(lambda: creds)
    agc = await agcm.authorize()
    # Open the spreadsheet
    spreadsheet = await agc.open('TW_searching_2024')
    sheet = await spreadsheet.get_worksheet(0)

    # Add a new line
    message = update.message.text
    links = find_urls(message)
    row = [None, None, None, None, None, None, None, None, None, None, links, message]
    await sheet.append_row(row)
    print(f"Message {message} added to the table.")
    # await update.message.reply_text(update.message.text)
    await update.message.reply_text("Запись успешно добавлена.")


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Every message is added in a Comments column on a new row.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print(update.message.text)
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Read token to access the bot
    with open("bot-token.txt", "r") as file:
        API_TOKEN = file.read()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_row_async))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, print_msg()))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
