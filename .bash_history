allow-setup-storage
# Update & upgrade
pkg update -y && pkg upgrade -y
# Install Python
pkg install python -y
# Install bot library
pip install python-telegram-bot
# Create bot directory
mkdir ~/telegram-bot && cd ~/telegram-bot
# Create bot file
curl -o bot.py https://raw.githubusercontent.com/your-repo/bot.py
pkg update -y
pkg upgrade -y
pkg install python -y
pip install python-telegram-bot
mkdir ~/telegram-bot
cd ~/telegram-bot
# Create file with echo commands
echo 'import random' > bot.py
echo 'from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup' >> bot.py
echo 'from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext' >> bot.py
echo '' >> bot.py
echo 'TOKEN = "8595752857:AAHdNF1EWZQ9HDZkf2DQOGTfl7tOyKzPurg"' >> bot.py
echo '' >> bot.py
echo 'def start(update, context):' >> bot.py
echo '    keyboard = [' >> bot.py
echo '        [InlineKeyboardButton("🎲 DICE", callback_data="dice")],' >> bot.py
echo '        [InlineKeyboardButton("🚀 LIMBO", callback_data="limbo")],' >> bot.py
echo '        [InlineKeyboardButton("🔒 FAIRNESS", callback_data="fair")]' >> bot.py
echo '    ]' >> bot.py
echo '    reply = InlineKeyboardMarkup(keyboard)' >> bot.py
echo '    update.message.reply_text("🎮 GAME BOT\\nClick buttons:", reply_markup=reply)' >> bot.py
echo '' >> bot.py
echo 'def button_click(update, context):' >> bot.py
echo '    query = update.callback_query' >> bot.py
echo '    query.answer()' >> bot.py
echo '    ' >> bot.py
echo '    if query.data == "dice":' >> bot.py
echo '        num = random.randint(1,6)' >> bot.py
echo '        query.edit_message_text(f"🎲 DICE: {num}\\n┌───┐\\n│ {num} │\\n└───┘")' >> bot.py
echo '    elif query.data == "limbo":' >> bot.py
echo '        crash = round(random.uniform(1.0, 10.0), 2)' >> bot.py
echo '        query.edit_message_text(f"🚀 LIMBO\\nCrash: {crash}x\\n┌───────┐\\n│ {crash}x │\\n└───────┘")' >> bot.py
echo '    elif query.data == "fair":' >> bot.py
echo '        query.edit_message_text("🔒 FAIRNESS CHECK\\n✅ Provably Fair\\nSHA256: a1b2c3...")' >> bot.py
echo '' >> bot.py
echo 'def main():' >> bot.py
echo '    print("🤖 Starting bot...")' >> bot.py
echo '    updater = Updater(TOKEN, use_context=True)' >> bot.py
echo '    dp = updater.dispatcher' >> bot.py
echo '    dp.add_handler(CommandHandler("start", start))' >> bot.py
echo '    dp.add_handler(CallbackQueryHandler(button_click))' >> bot.py
echo '    print("✅ Bot running! Send /start on Telegram")' >> bot.py
echo '    updater.start_polling()' >> bot.py
echo '    updater.idle()' >> bot.py
echo '' >> bot.py
echo 'if __name__ == "__main__":' >> bot.py
echo '    main()' >> bot.py
# Create file with echo commands
echo 'import random' > bot.py
echo 'from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup' >> bot.py
echo 'from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext' >> bot.py
echo '' >> bot.py
echo 'TOKEN = "8595752857:AAHdNF1EWZQ9HDZkf2DQOGTfl7tOyKzPurg"' >> bot.py
echo '' >> bot.py
echo 'def start(update, context):' >> bot.py
echo '    keyboard = [' >> bot.py
echo '        [InlineKeyboardButton("🎲 DICE", callback_data="dice")],' >> bot.py
echo '        [InlineKeyboardButton("🚀 LIMBO", callback_data="limbo")],' >> bot.py
echo '        [InlineKeyboardButton("🔒 FAIRNESS", callback_data="fair")]' >> bot.py
echo '    ]' >> bot.py
echo '    reply = InlineKeyboardMarkup(keyboard)' >> bot.py
echo '    update.message.reply_text("🎮 GAME BOT\\nClick buttons:", reply_markup=reply)' >> bot.py
echo '' >> bot.py
echo 'def button_click(update, context):' >> bot.py
echo '    query = update.callback_query' >> bot.py
echo '    query.answer()' >> bot.py
echo '    ' >> bot.py
echo '    if query.data == "dice":' >> bot.py
echo '        num = random.randint(1,6)' >> bot.py
echo '        query.edit_message_text(f"🎲 DICE: {num}\\n┌───┐\\n│ {num} │\\n└───┘")' >> bot.py
echo '    elif query.data == "limbo":' >> bot.py
echo '        crash = round(random.uniform(1.0, 10.0), 2)' >> bot.py
echo '        query.edit_message_text(f"🚀 LIMBO\\nCrash: {crash}x\\n┌───────┐\\n│ {crash}x │\\n└───────┘")' >> bot.py
echo '    elif query.data == "fair":' >> bot.py
echo '        query.edit_message_text("🔒 FAIRNESS CHECK\\n✅ Provably Fair\\nSHA256: a1b2c3...")' >> bot.py
echo '' >> bot.py
echo 'def main():' >> bot.py
echo '    print("🤖 Starting bot...")' >> bot.py
echo '    updater = Updater(TOKEN, use_context=True)' >> bot.py
echo '    dp = updater.dispatcher' >> bot.py
echo '    dp.add_handler(CommandHandler("start", start))' >> bot.py
echo '    dp.add_handler(CallbackQueryHandler(button_click))' >> bot.py
echo '    print("✅ Bot running! Send /start on Telegram")' >> bot.py
echo '    updater.start_polling()' >> bot.py
echo '    updater.idle()' >> bot.py
echo '' >> bot.py
echo 'if __name__ == "__main__":' >> bot.py
echo '    main()' >> bot.py
echo '' >> bot.py
pkg update -y && pkg upgrade -y
pkg install python -y
pip install python-telegram-bot
mkdir ~/telegram-bot && cd ~/telegram-bot
cat > bot.py << 'EOF'
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "8595752857:AAHdNF1EWZQ9HDZkf2DQOGTfl7tOyKzPurg"

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🎲 DICE", callback_data="dice")],
        [InlineKeyboardButton("🚀 LIMBO", callback_data="limbo")],
        [InlineKeyboardButton("🔒 FAIRNESS", callback_data="fairness")],
        [InlineKeyboardButton("📊 STATUS", callback_data="status")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎮 GAME BOT\nChoose game:", reply_markup=reply)

def button_click(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == "dice":
        num = random.randint(1, 6)
        dice_board = f"""┌─────┐
│  {num}  │
└─────┘"""
        query.edit_message_text(f"🎲 DICE\n{dice_board}\nResult: {num}")
    
    elif query.data == "limbo":
        crash = random.uniform(1.0, 10.0)
        query.edit_message_text(f"🚀 LIMBO\nCrash Point: {crash:.2f}x\nStatus: {'WIN 🎉' if crash >= 2.0 else 'LOSE 💥'}")
    
    elif query.data == "fairness":
        query.edit_message_text("🔒 PROVABLY FAIR\nClient Seed: USER123\nServer Seed: SHA256:abc123...\n✅ Verified")
    
    elif query.data == "status":
        query.edit_message_text("📊 BOT STATUS\n✅ Online\nUsers: 127\nGames: 548\nVIP: Active")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
EOF

python bot.py
cd ~/telegram-bot && rm bot.py
cat > bot.py << 'EOF'
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "8595752857:AAHdNF1EWZQ9HDZkf2DQOGTfl7tOyKzPurg"

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🎲 DICE", callback_data="dice")],
        [InlineKeyboardButton("🚀 LIMBO", callback_data="limbo")],
        [InlineKeyboardButton("🔒 FAIRNESS", callback_data="fairness")],
        [InlineKeyboardButton("📊 STATUS", callback_data="status")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎮 GAME BOT\nChoose game:", reply_markup=reply)

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "dice":
        num = random.randint(1, 6)
        dice_board = f"""┌─────┐
│  {num}  │
└─────┘"""
        query.edit_message_text(f"🎲 DICE\n{dice_board}\nResult: {num}")
    
    elif query.data == "limbo":
        crash = random.uniform(1.0, 10.0)
        query.edit_message_text(f"🚀 LIMBO\nCrash Point: {crash:.2f}x\nStatus: {'WIN 🎉' if crash >= 2.0 else 'LOSE 💥'}")
    
    elif query.data == "fairness":
        query.edit_message_text("🔒 PROVABLY FAIR\nClient Seed: USER123\nServer Seed: SHA256:abc123...\n✅ Verified")
    
    elif query.data == "status":
        query.edit_message_text("📊 BOT STATUS\n✅ Online\nUsers: 127\nGames: 548\nVIP: Active")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))
    print("✅ Bot running! Send /start on Telegram")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
EOF

python bot.py
cd ~/telegram-bot && rm bot.py
python bot.py
cd ~
rm -rf telegram-bot
mkdir telegram-bot
cd telegram-bot
cd ~
rm -rf telegram-bot
mkdir telegram-bot
cd telegram-bot
end
exit
cd ~
rm -rf telegram-bot
mkdir telegram-bot
cd telegram-bot
cat > bot.py << 'EOF'
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8595752857:AAHdNF1EWZQ9HDZkf2DQOGTfl7tOyKzPurg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎲 DICE", callback_data="dice")],
        [InlineKeyboardButton("🚀 LIMBO", callback_data="limbo")],
        [InlineKeyboardButton("🔒 FAIRNESS", callback_data="fairness")],
        [InlineKeyboardButton("📊 STATUS", callback_data="status")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎮 GAME BOT\nChoose game:", reply_markup=reply)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "dice":
        num = random.randint(1, 6)
        await query.edit_message_text(f"🎲 DICE\n┌─────┐\n│  {num}  │\n└─────┘\nResult: {num}")
    
    elif query.data == "limbo":
        crash = random.uniform(1.0, 10.0)
        await query.edit_message_text(f"🚀 LIMBO\nCrash: {crash:.2f}x\nStatus: {'WIN 🎉' if crash >= 2.0 else 'LOSE 💥'}")
    
    elif query.data == "fairness":
        await query.edit_message_text("🔒 PROVABLY FAIR\nClient Seed: USER123\nServer Seed: SHA256:abc123\n✅ Verified")
    
    elif query.data == "status":
        await query.edit_message_text("📊 BOT STATUS\n✅ Online\nUsers: 127\nGames: 548\nVIP: Active")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("🤖 Bot starting...")
    print("✅ Bot is running! Send /start on Telegram")
    app.run_polling()

if __name__ == "__main__":
    main()
EOF

cat > bot.py << 'EOF'
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8595752857:AAHdNF1EWZQ9HDZkf2DQOGTfl7tOyKzPurg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎲 DICE", callback_data="dice")],
        [InlineKeyboardButton("🚀 LIMBO", callback_data="limbo")],
        [InlineKeyboardButton("🔒 FAIRNESS", callback_data="fairness")],
        [InlineKeyboardButton("📊 STATUS", callback_data="status")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎮 GAME BOT\nChoose game:", reply_markup=reply)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "dice":
        num = random.randint(1, 6)
        await query.edit_message_text(f"🎲 DICE\n┌─────┐\n│  {num}  │\n└─────┘\nResult: {num}")
    
    elif query.data == "limbo":
        crash = random.uniform(1.0, 10.0)
        await query.edit_message_text(f"🚀 LIMBO\nCrash: {crash:.2f}x\nStatus: {'WIN 🎉' if crash >= 2.0 else 'LOSE 💥'}")
    
    elif query.data == "fairness":
        await query.edit_message_text("🔒 PROVABLY FAIR\nClient Seed: USER123\nServer Seed: SHA256:abc123\n✅ Verified")
    
    elif query.data == "status":
        await query.edit_message_text("📊 BOT STATUS\n✅ Online\nUsers: 127\nGames: 548\nVIP: Active")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("🤖 Bot starting...")
    print("✅ Bot is running! Send /start on Telegram")
    app.run_polling()

if __name__ == "__main__":
    main()
EOF

exit
cp ~/telegram-bot/bot.py /storage/emulated/0/Download/bot.py
pkg install termux-apitermux-setup-storage
cd ~
ls
pwd
mkdir -p telegram-bot
cd telegram-bot
ls -la bot.py
cat bot.py
cat > bot.py << 'EOF'
import random
import time
import requests

TOKEN = "8595752857:AAHdNF1EWZQ9HDZkf2DQOGTfl7tOyKzPurg"
URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = 0

while True:
    try:
        response = requests.get(f"{URL}/getUpdates", params={"offset": last_update_id + 1}).json()
        
        if response.get("ok"):
            for update in response["result"]:
                last_update_id = update["update_id"]
                
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "").strip()
                    
                    if text == "/start":
                        keyboard = {
                            "keyboard": [
                                [{"text": "🎲 DICE"}, {"text": "🚀 LIMBO"}],
                                [{"text": "💣 MINES"}, {"text": "📊 STATUS"}]
                            ],
                            "resize_keyboard": True
                        }
                        requests.post(f"{URL}/sendMessage", json={
                            "chat_id": chat_id,
                            "text": "🎮 GAME BOT\nChoose game:",
                            "reply_markup": keyboard,
                            "parse_mode": "Markdown"
                        })
                    
                    elif text == "🎲 DICE":
                        num = random.randint(1, 6)
                        requests.post(f"{URL}/sendMessage", json={
                            "chat_id": chat_id,
                            "text": f"🎲 DICE\nResult: {num}",
                            "parse_mode": "Markdown"
                        })
                    
                    elif text == "🚀 LIMBO":
                        crash = round(random.uniform(1.0, 10.0), 2)
                        requests.post(f"{URL}/sendMessage", json={
                            "chat_id": chat_id,
                            "text": f"🚀 LIMBO\nCrash: {crash}x",
                            "parse_mode": "Markdown"
                        })
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
EOF

mkdir -p telegram-bot
cd telegram-bot
python bot.py
exit
cd ~
mkdir aswad_bot
cd aswad_bot
aswad_bot/
mkdir images
ls
nano bot.py
nano requirements.txt
cp /storage/emulated/0/Download/client_seed.jpg ~/aswad_bot/images/
cp /storage/emulated/0/Download/server_seed.jpg ~/aswad_bot/images/
ls image
ls images
nano bot.py
exit
pwd
cd ~/aswad_bot
ls
nano bot.py
exit
