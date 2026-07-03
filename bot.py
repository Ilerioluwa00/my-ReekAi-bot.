import os
import requests
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- 1. Background Web Server for Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Reekiel AI is running online! 🚀"

def run_flask():
    # Render automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- 2. Live Data Mapping ---
CITIES = {
    "nigeria": {"name": "Lagos", "lat": 6.52, "lon": 3.37, "zone": "Africa/Lagos", "flag": "🇳🇬"},
    "usa": {"name": "New York", "lat": 40.71, "lon": -74.00, "zone": "America/New_York", "flag": "🇺🇸"},
    "china": {"name": "Shanghai", "lat": 31.23, "lon": 121.47, "zone": "Asia/Shanghai", "flag": "🇨🇳"},
    "south korea": {"name": "Seoul", "lat": 37.56, "lon": 126.97, "zone": "Asia/Seoul", "flag": "🇰🇷"},
    "japan": {"name": "Tokyo", "lat": 35.67, "lon": 139.65, "zone": "Asia/Tokyo", "flag": "🇯🇵"},
    "india": {"name": "New Delhi", "lat": 28.61, "lon": 77.20, "zone": "Asia/Kolkata", "flag": "🇮🇳"}
}

NEWS_FEEDS = {
    "ukraine": "https://api.rss2json.com/v1/api.json?rss_url=https://news.un.org/feed/subscribe/en/news/region/europe/feed/rss.xml",
    "middle east": "https://api.rss2json.com/v1/api.json?rss_url=https://news.un.org/feed/subscribe/en/news/region/middle-east/feed/rss.xml",
    "crypto": "https://api.rss2json.com/v1/api.json?rss_url=https://www.coindesk.com/arc/outboundfeeds/rss/",
    "usa": "https://api.rss2json.com/v1/api.json?rss_url=https://www.bostonglobe.com/rss/nation"
}

# --- 3. Telegram Message Handler ---
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower().strip()
    
    if user_text == "hello":
        await update.message.reply_text("🤖 Reekiel AI: How are you doing? I'm ready to assist.")
        return

    # Check for Live News
    if "news" in user_text:
        for category, url in NEWS_FEEDS.items():
            if category in user_text:
                try:
                    response = requests.get(url).json()
                    articles = response.get("items", [])[:3]
                    if not articles:
                        await update.message.reply_text("📰 Reekiel AI: No recent updates found.")
                        return
                    reply = f"🌍 **Reekiel AI Live News: {category.upper()}**\n\n"
                    for item in articles:
                        reply += f"🔹 *{item['title']}*\n🔗 {item['link']}\n\n"
                    await update.message.reply_text(reply, parse_mode="Markdown")
                    return
                except Exception:
                    await update.message.reply_text("⚠️ Reekiel AI: I had trouble connecting to the news network.")
                    return

    # Check for Live Weather and Time
    for country, info in CITIES.items():
        if country in user_text:
            if "weather" in user_text:
                try:
                    url = f"https://api.open-meteo.com/v1/forecast?latitude={info['lat']}&longitude={info['lon']}&current_weather=true"
                    response = requests.get(url).json()
                    temp = response["current_weather"]["temperature"]
                    await update.message.reply_text(f"{info['flag']} Live Weather for {info['name']}:\n🌡️ Temperature: {temp}°C")
                    return
                except Exception:
                    await update.message.reply_text("⚠️ Reekiel AI: Couldn't fetch live weather data.")
                    return
            elif "time" in user_text:
                current_time = datetime.now(ZoneInfo(info["zone"])).strftime("%I:%M %p")
                await update.message.reply_text(f"{info['flag']} The current time in {info['name']} is {current_time}.")
                return

    await update.message.reply_text(f"🤖 Reekiel AI: You said '{update.message.text}'")

# --- 4. Main Application Startup ---
if __name__ == '__main__':
    # 🔴 PASTE YOUR TELEGRAM BOT TOKEN BETWEEN THE QUOTES BELOW 🔴
    TOKEN = "8385196888:AAFYrzi-v5Lwv_19vNaLwfs95wthEoX5EZY"
    
    # Start the Flask web server in a background thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Start the Telegram Bot
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_handler))
    
    print("Running python bot.py")
    application.run_polling()
