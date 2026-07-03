import os
import requests
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. Background Web Server for Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Reekiel AI is running online! 🚀"

def run_flask():
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

# --- 3. Custom System Diagnostics Command ---
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    diagnostics = (
        "🖥️ **Reekiel AI Diagnostics**\n\n"
        "⚡ **Main Core:** ONLINE\n"
        "🛰️ **Satellite Uplink:** CONNECTED (Open-Meteo)\n"
        "📰 **News Matrix:** OPERATIONAL (RSS Streams)\n"
        "🧵 **Background Thread:** ACTIVE (Flask Port Open)\n\n"
        "All internal systems are nominal, boss. Standing by for commands."
    )
    await update.message.reply_text(diagnostics, parse_mode="Markdown")

# --- 4. Main Message Handler ---
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower().strip()
    
    if user_text == "hello":
        await update.message.reply_text("🤖 Reekiel AI: At your service, boss. How may I assist you today?")
        return

    # News Stream Matrix
    if "news" in user_text:
        for category, url in NEWS_FEEDS.items():
            if category in user_text:
                try:
                    await update.message.reply_text("🖥️ Accessing global news networks now, boss...")
                    response = requests.get(url).json()
                    articles = response.get("items", [])[:3]
                    if not articles:
                        await update.message.reply_text("📰 Reekiel AI: No recent updates found in the secure feeds, boss.")
                        return
                    reply = f"🌍 **Reekiel AI Intel Report: {category.upper()}**\n\n"
                    for item in articles:
                        reply += f"🔹 *{item['title']}*\n🔗 {item['link']}\n\n"
                    await update.message.reply_text(reply, parse_mode="Markdown")
                    return
                except Exception:
                    await update.message.reply_text("⚠️ Reekiel AI: Encryption error. News link unavailable, boss.")
                    return

    # Weather & Time Tracker
    for country, info in CITIES.items():
        if country in user_text:
            if "weather" in user_text:
                try:
                    await update.message.reply_text(f"🛰️ Scanning atmospheric data for {info['name']}...")
                    url = f"https://api.open-meteo.com/v1/forecast?latitude={info['lat']}&longitude={info['lon']}&current_weather=true"
                    response = requests.get(url).json()
                    temp = response["current_weather"]["temperature"]
                    
                    # Automated Thermal Alert Matrix
                    alert_msg = ""
                    if temp >= 35:
                        alert_msg = "\n🚨 **CRITICAL THERMAL ALERT:** Extreme high heat detected in this sector, boss. Advise staying indoors."
                    elif temp <= 5:
                        alert_msg = "\n🚨 **CRITICAL THERMAL ALERT:** Extreme low temperature detected in this sector, boss."
                    
                    await update.message.reply_text(
                        f"{info['flag']} Current conditions for {info['name']}:\n"
                        f"🌡️ Temperature: {temp}°C{alert_msg}\n"
                        f"All systems nominal, boss.",
                        parse_mode="Markdown"
                    )
                    return
                except Exception:
                    await update.message.reply_text("⚠️ Reekiel AI: Satellite link failed. Data missing, boss.")
                    return
            elif "time" in user_text:
                current_time = datetime.now(ZoneInfo(info["zone"])).strftime("%I:%M %p")
                await update.message.reply_text(f"{info['flag']} Chronometer update, boss: The current time in {info['name']} is {current_time}.")
                return

    await update.message.reply_text(f"🤖 Reekiel AI: Processed command: '{update.message.text}'. Standing by for instructions, boss.")

# --- 5. Application Startup ---
if __name__ == '__main__':
    # 🔴 PASTE YOUR TELEGRAM BOT TOKEN BETWEEN THE QUOTES BELOW 🔴
    TOKEN = "8385196888:AAFYrzi-v5Lwv_19vNaLwfs95wthEoX5EZY"
    
    # Run the background web port thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Start the application framework
    application = Application.builder().token(TOKEN).build()
    
    # Command & Message routing
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_handler))
    
    print("Running python bot.py")
    application.run_polling()
                    
