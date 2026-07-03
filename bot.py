import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging so we can see errors in Pydroid's terminal
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the /start command response
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I am your mobile-built bot. Send me a message and I will reply!")

# Define how the bot echoes back your messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply_text = f"🤖 You said: '{user_text}'"
    await update.message.reply_text(reply_text)

def main():
    # Insert your token here
    TOKEN = '8385196888:AAFYrzi-v5Lwv_19vNaLwfs95wthEoX5EZY'
    
    # Build the application
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers for commands and messages
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Start the bot
    print("⚡ Bot is starting... Press the stop button in Pydroid to turn it off.")
    app.run_polling()

if __name__ == '__main__':
    main()
