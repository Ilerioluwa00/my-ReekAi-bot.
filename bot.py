import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Setup Flask web server for Render
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🤖 Bot is running 24/7!"

def run_flask():
    # Render provides a PORT environment variable automatically
    import os
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# 2. Setup Telegram Bot Logic
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I am your mobile-built bot. Send me a message!")

# This handles your custom text replies!
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower() # Converts to lowercase to catch "Hello" or "HELLO"
    
    if user_text == "hello":
        reply_text = "how are you doing? I'm good."
    else:
        reply_text = f"🤖 You said: '{update.message.text}'"
        
    await update.message.reply_text(reply_text)

def main():
    # Put your actual token from BotFather inside the quotes below
    TOKEN = '8385196888:AAFYrzi-v5Lwv_19vNaLwfs95wthEoX5EZY'
    
    # Start the Flask web server in a separate background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start the Telegram bot application
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_handler))
    
    print("⚡ Bot and Web Server are starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
