import random, asyncio, json, hashlib, uuid
from datetime import datetime, timedelta
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# --- CONFIGURATION ---
TOKEN = "8595752857:AAE-snKxRbSau0OP9rw22p_Jkzus5qu0NC8"
ADMIN_USERNAME = "Merejigarketukde"  # @ hata kar likha hai, yahi sahi hai

BASE = Path(__file__).parent
DATA_FILE = BASE / "bot_data.json"
CLIENT_IMG = BASE / "images/client_seed.jpg"
SERVER_IMG = BASE / "images/server_seed.jpg"

# --- DATA MANAGEMENT ---
def load_data():
    if DATA_FILE.exists():
        try:
            return json.load(open(DATA_FILE, "r"))
        except:
            return {"users": {}, "keys": {}, "banned": []}
    return {"users": {}, "keys": {}, "banned": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- KEYBOARDS ---
def main_menu():
    return ReplyKeyboardMarkup([["🎯 Limbo", "💣 Mines"], ["🎲 Dice", "🔢 Keno"]], resize_keyboard=True)

def win_loss_kb():
    return ReplyKeyboardMarkup([["✅ Win", "❌ Loss"]], resize_keyboard=True)

def mines_kb():
    return ReplyKeyboardMarkup([["💣 1 Mine", "💣 3 Mines"], ["💣 5 Mines", "🔙 Back"]], resize_keyboard=True)

# --- SECURITY CHECKS ---
async def check_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    uid = str(user.id)

    # 1. Check if Banned
    if uid in data.get("banned", []):
        await update.message.reply_text("🚫 You are BANNED from using this bot.\nContact Admin: @Merejigarketukde")
        return False

    # 2. Check License
    if uid not in data["users"]:
        await update.message.reply_text("🔒 Locked!\n\nAccess lene ke liye Key kharidein.\nContact Owner: @Merejigarketukde")
        return False
    
    # 3. Check Expiry
    expiry = datetime.fromisoformat(data["users"][uid])
    if datetime.now() > expiry:
        await update.message.reply_text("⚠️ License Expired!\nNaya key kharidein: @Merejigarketukde")
        return False
        
    return True

async def is_admin(update: Update):
    if update.effective_user.username == ADMIN_USERNAME:
        return True
    await update.message.reply_text("❌ Sirf Boss (@Merejigarketukde) ye command chala sakta hai!")
    return False

# --- FAKE ANALYSIS ANIMATION ---
async def analyzing(update, game_name):
    msg = await update.message.reply_text(f"🔄 Connecting to {game_name} Server...")
    await asyncio.sleep(1)
    
    seed = ''.join(random.choices('ABCDEF0123456789', k=16))
    fake_hash = hashlib.sha256(seed.encode()).hexdigest()[:14].upper()
    
    await msg.edit_text(f"🔓 **Server Seed Decrypted**\n`{fake_hash}`\n\n⚙️ Calculating Safe Spots...")
    await asyncio.sleep(2)
    await msg.delete()

# --- ADMIN COMMANDS (GOD MODE) ---

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    msg = (
        "👑 **GODFATHER ADMIN PANEL** 👑\n\n"
        "1️⃣ `/gen <days>` - Key banaye (Eg: `/gen 7`)\n"
        "2️⃣ `/users` - Sabhi active users dekhein\n"
        "3️⃣ `/keys` - Pending keys dekhein\n"
        "4️⃣ `/ban <id>` - User ko block karein\n"
        "5️⃣ `/unban <id>` - User ko unblock karein\n"
        "6️⃣ `/info <id>` - Kisi user ki detail nikalein"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def generate_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    try:
        days = int(context.args[0])
    except:
        days = 1 # Default 1 day agar kuch na likho
        
    key = "KEY-" + str(uuid.uuid4())[:8].upper()
    data = load_data()
    data["keys"][key] = days
    save_data(data)
    
    await update.message.reply_text(f"🆕 **New Key Generated**\n\n🔑 Key: `{key}`\n⏳ Validity: {days} Days\n\nCopy karke user ko bhejein.", parse_mode="Markdown")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    data = load_data()
    
    if not data["users"]:
        await update.message.reply_text("📂 Koi user active nahi hai.")
        return

    msg = "👥 **Active Users List:**\n"
    for uid, date_str in data["users"].items():
        expiry = datetime.fromisoformat(date_str).strftime("%d-%b %H:%M")
        status = "🔴 Expired" if datetime.now() > datetime.fromisoformat(date_str) else "🟢 Active"
        msg += f"🆔 `{uid}` | {status} | Exp: {expiry}\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    if not context.args:
        await update.message.reply_text("🆔 User ID to likho! Eg: `/ban 12345678`")
        return
        
    target_id = context.args[0]
    data = load_data()
    
    if "banned" not in data: data["banned"] = []
    
    if target_id not in data["banned"]:
        data["banned"].append(target_id)
        # Optional: Remove from active users too
        if target_id in data["users"]:
            del data["users"][target_id]
        save_data(data)
        await update.message.reply_text(f"🚫 User `{target_id}` ko **BAN** kar diya gaya hai!", parse_mode="Markdown")
    else:
        await update.message.reply_text("Ye pehle se hi banned hai.")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    target_id = context.args[0]
    data = load_data()
    
    if "banned" in data and target_id in data["banned"]:
        data["banned"].remove(target_id)
        save_data(data)
        await update.message.reply_text(f"✅ User `{target_id}` ko **UNBAN** kar diya.", parse_mode="Markdown")
    else:
        await update.message.reply_text("Ye user banned list mein nahi hai.")

async def list_keys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    data = load_data()
    if not data["keys"]:
        await update.message.reply_text("📭 Koi pending key nahi hai.")
        return
        
    msg = "🔑 **Unused Keys:**\n"
    for key, days in data["keys"].items():
        msg += f"- `{key}` ({days} Days)\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

# --- USER COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 **Aswad Godfather Bot**\n\n"
        "Ye premium bot hai. Access lene ke liye Admin se Key lein.\n"
        "Owner: @Merejigarketukde\n\n"
        "Key Activate karne ke liye:\n"
        "`/activate KEY_HERE`", 
        parse_mode="Markdown"
    )

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Key kahan hai? Aise likho:\n`/activate KEY-1234...`", parse_mode="Markdown")
        return
    
    key = context.args[0]
    data = load_data()
    
    # Check if banned
    if str(update.effective_user.id) in data.get("banned", []):
        await update.message.reply_text("🚫 Aap banned ho!")
        return

    if key in data["keys"]:
        days = data["keys"][key]
        expiry = datetime.now() + timedelta(days=days)
        data["users"][str(update.effective_user.id)] = expiry.isoformat()
        del data["keys"][key]
        save_data(data)
        await update.message.reply_text(f"✅ **Activation Successful!**\n\nValid for: {days} Days\nExpiry: {expiry.strftime('%d-%b-%Y')}", reply_markup=main_menu(), parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Ye Key galat hai ya use ho chuki hai.")

# --- GAME HANDLERS ---

async def mines_logic(update, context):
    await analyzing(update, "Mines")
    # Advance Pattern (Diamond Shape Example)
    grid = "⬜ ⬜ 💎 ⬜ ⬜\n⬜ 💎 💎 💎 ⬜\n💎 💎 💎 💎 💎\n⬜ 💎 💎 💎 ⬜\n⬜ ⬜ 💎 ⬜ ⬜"
    await update.message.reply_text(f"💣 **Mines Prediction**\nRisk: Safe Mode\n\n{grid}", reply_markup=win_loss_kb(), parse_mode="Markdown")

async def limbo_logic(update, context):
    await analyzing(update, "Limbo")
    mult = random.choices([1.1, 1.5, 2.0, 5.0], [50, 30, 15, 5])[0]
    await update.message.reply_text(f"🎯 **Limbo Target**\n\n👉 Bet on: `{mult}x`", reply_markup=win_loss_kb(), parse_mode="Markdown")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update, context): return
    
    text = update.message.text
    
    if text == "🎯 Limbo":
        await limbo_logic(update, context)
    elif text == "💣 Mines":
        await update.message.reply_text("Select Mines Count:", reply_markup=mines_kb())
    elif "Mine" in text: # Handle 1 Mine, 3 Mines etc
        await mines_logic(update, context)
    elif text == "🎲 Dice":
        await update.message.reply_text("🎲 Dice: Bet on **RIGHT** (48-100)", reply_markup=win_loss_kb())
    elif text == "🔢 Keno":
        await update.message.reply_text("🔢 Keno: 4, 12, 28, 35 (High Risk)", reply_markup=win_loss_kb())

# --- MAIN SETUP ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Admin Handlers
    app.add_handler(CommandHandler("admin", admin_help))
    app.add_handler(CommandHandler("gen", generate_key))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("keys", list_keys))
    
    # User Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    print("🤖 God Mode Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
