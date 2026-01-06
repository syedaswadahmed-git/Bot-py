import random, asyncio, json, uuid, os
from datetime import datetime, timedelta
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# --- CONFIGURATION ---
TOKEN = "8595752857:AAE-snKxRbSau0OP9rw22p_Jkzus5qu0NC8"
ADMIN_USERNAME = "Merejigarketukde"

BASE = Path(__file__).parent
DATA_FILE = BASE / "bot_data.json"
CLIENT_IMG = BASE / "images/client_seed.jpg"
SERVER_IMG = BASE / "images/server_seed.jpg"

# --- DATA MANAGEMENT ---
def load_data():
    if DATA_FILE.exists():
        try: return json.load(open(DATA_FILE, "r"))
        except: return {"users": {}, "keys": {}, "banned": [], "history": []}
    return {"users": {}, "keys": {}, "banned": [], "history": []}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- KEYBOARDS ---
def main_menu():
    return ReplyKeyboardMarkup([["🎯 Limbo", "💣 Mines"], ["🎲 Dice", "🔢 Keno"]], resize_keyboard=True)

def win_loss_kb():
    return ReplyKeyboardMarkup([["✅ Win", "❌ Loss"]], resize_keyboard=True)

def mines_count_kb():
    rows, row = [], []
    for i in range(1, 25):
        row.append(str(i))
        if len(row) == 6: rows.append(row); row = []
    if row: rows.append(row)
    rows.append(["🔙 Menu"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def open_count_kb():
    rows, row = [], []
    for i in range(1, 11):
        row.append(str(i))
        if len(row) == 5: rows.append(row); row = []
    if row: rows.append(row)
    rows.append(["🔙 Menu"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def keno_amt_kb():
    return ReplyKeyboardMarkup([["1", "2", "3", "4"], ["5", "6", "7", "8"], ["🔙 Menu"]], resize_keyboard=True)

def keno_risk_kb():
    return ReplyKeyboardMarkup([["🟢 Low", "🟡 Medium"], ["🔴 High", "🔙 Menu"]], resize_keyboard=True)

# --- AUTH & SECURITY ---
async def check_auth(update: Update):
    data = load_data()
    uid = str(update.effective_user.id)
    
    # 1. Check Ban
    if uid in data.get("banned", []):
        await update.message.reply_text("🚫 **ACCESS DENIED**\nAdmin ne tumhe BAN kar diya hai.")
        return False
        
    # 2. Check License Existence
    if uid not in data["users"]:
        # Agar user ke paas license nahi hai, toh use lock message bhejo
        # Lekin agar ye /start command hai, toh hum wahan alag handle karenge
        return False
        
    user_info = data["users"][uid]
    
    # CRASH FIX: Check if data is dict or string (Old Data Support)
    if isinstance(user_info, str):
        # Old format detected, force user to re-login or clean db
        del data["users"][uid]
        save_data(data)
        return False

    expiry = datetime.fromisoformat(user_info["expiry"])
    
    if datetime.now() > expiry:
        await update.message.reply_text("⚠️ **License Expired!**\nRenew: @Merejigarketukde")
        return False
        
    return True

async def unauthorized_alert(update: Update):
    await update.message.reply_text(
        "⛔ **TERI AUKAAT NAHI HAI!** ⛔\n\n"
        "Ye command sirf **Baap (@Merejigarketukde)** chala sakta hai.",
        parse_mode="Markdown"
    )

# --- ANIMATIONS ---
async def show_verified_animation(update, seed_type, user_input):
    msg = await update.message.reply_text(f"⏳ **Verifying {seed_type}...**", parse_mode="Markdown")
    await asyncio.sleep(1)
    await msg.edit_text(f"✅ **{seed_type} Verified!**\nInput: `{user_input}`\nStatus: 🛡️ Authenticated", parse_mode="Markdown")
    await asyncio.sleep(1)
    await msg.delete()

async def play_hacker_animation(update):
    msg = await update.message.reply_text("⚡ **Establishing Connection...**", parse_mode="Markdown")
    await asyncio.sleep(0.5)
    await msg.edit_text("👨‍💻 **Decrypting Algorithm...**", parse_mode="Markdown")
    await asyncio.sleep(0.5)
    await msg.edit_text("🔓 **PATTERN FOUND!**", parse_mode="Markdown")
    await asyncio.sleep(0.5)
    await msg.delete()

# --- GAME LOGIC ---
async def get_limbo_res(update, context):
    await play_hacker_animation(update)
    target = random.choices([1.5, 2.0, 3.0, 10.0], [40, 30, 20, 10])[0]
    roll = target + round(random.uniform(0.1, 15.0), 2)
    msg = (f"🎯 **LIMBO PREDICTION**\n\n🎯 Target: `{target}x`\n🚀 Roll: `{roll}x`\n👉 **Bet on {target}x or lower**")
    context.user_data["last_func"] = "limbo"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

async def get_dice_res(update, context):
    await play_hacker_animation(update)
    roll = random.randint(40, 98)
    condition = "Over 40" if roll > 40 else "Under 40"
    msg = (f"🎲 **DICE PREDICTION**\n\n🎰 Prediction: **{condition}**\n🎲 Expected Roll: `{roll}`\n⚡ Drag slider to secure zone.")
    context.user_data["last_func"] = "dice"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

async def get_keno_res(update, context):
    await play_hacker_animation(update)
    amt = context.user_data.get("keno_amt", 4)
    risk = context.user_data.get("keno_risk", "High")
    nums = random.sample(range(1, 41), amt)
    nums.sort()
    msg = (f"🔢 **KENO PREDICTION**\n\n🔮 Numbers: `{', '.join(map(str, nums))}`\n🔥 Risk: {risk}\n\nPlay these numbers.")
    context.user_data["last_func"] = "keno"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

async def get_mines_res(update, context):
    await play_hacker_animation(update)
    mines = context.user_data.get("mines", 3)
    opens = context.user_data.get("opens", 3)
    cells = random.sample(range(25), opens)
    grid = ["⬜"] * 25
    for c in cells: grid[c] = "⭐"
    board_str = ""
    for i in range(0, 25, 5): board_str += "  ".join(grid[i:i+5]) + "\n"
    msg = (f"💣 **MINES PREDICTION**\n💣 Mines: `{mines}` | 💎 Open: `{opens}`\n\n{board_str}")
    context.user_data["last_func"] = "mines"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

# --- HANDLERS (GAME FLOW) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Agar Authorized hai to seedha Games dikhao
    if await check_auth(update):
        await update.message.reply_text("👑 **Welcome Boss! Ready to earn?**", reply_markup=main_menu(), parse_mode="Markdown")
    else:
        # Agar Authorized nahi hai to Lock Message
        await update.message.reply_text("🔒 **LOCKED**\n\nAccess lene ke liye Key kharidein.\nAdmin: @Merejigarketukde\n\nUse: `/activate KEY`", parse_mode="Markdown")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        # Agar koi bina license ke button dabaye ya baat kare
        await update.message.reply_text("🔒 **Access Denied**\nKey Activate karein: `/activate KEY`", parse_mode="Markdown")
        return

    text = update.message.text
    ud = context.user_data

    if text == "🔙 Menu":
        ud.clear()
        await update.message.reply_text("🏠 **Main Menu**", reply_markup=main_menu(), parse_mode="Markdown")
        return

    if text in ["🎯 Limbo", "💣 Mines", "🎲 Dice", "🔢 Keno"]:
        ud.clear()
        ud["game"] = text
        if CLIENT_IMG.exists():
            await update.message.reply_photo(CLIENT_IMG, caption="📌 **Send Active Client Seed**", parse_mode="Markdown")
        else:
            await update.message.reply_text("📌 **Send Active Client Seed**", parse_mode="Markdown")
        ud["step"] = "wait_client"
        return

    if ud.get("step") == "wait_client":
        await show_verified_animation(update, "Client Seed", text)
        if SERVER_IMG.exists():
            await update.message.reply_photo(SERVER_IMG, caption="📌 **Send Active Server Seed**", parse_mode="Markdown")
        else:
            await update.message.reply_text("📌 **Send Active Server Seed**", parse_mode="Markdown")
        ud["step"] = "wait_server"
        return

    if ud.get("step") == "wait_server":
        await show_verified_animation(update, "Server Seed", text)
        game = ud.get("game")
        if game == "💣 Mines":
            await update.message.reply_text("💣 **How many Mines?**\nSelect 1-24:", reply_markup=mines_count_kb(), parse_mode="Markdown")
            ud["step"] = "wait_mines_cnt"
        elif game == "🔢 Keno":
            await update.message.reply_text("🔢 **How many numbers?**", reply_markup=keno_amt_kb(), parse_mode="Markdown")
            ud["step"] = "wait_keno_amt"
        elif game == "🎯 Limbo":
            await get_limbo_res(update, context)
            ud["step"] = "result"
        elif game == "🎲 Dice":
            await get_dice_res(update, context)
            ud["step"] = "result"
        return

    if ud.get("step") == "wait_mines_cnt":
        if not text.isdigit() or not (1 <= int(text) <= 24):
            await update.message.reply_text("⚠️ Select 1-24")
            return
        ud["mines"] = int(text)
        await update.message.reply_text("💎 **How many tiles to open?**", reply_markup=open_count_kb(), parse_mode="Markdown")
        ud["step"] = "wait_open_cnt"
        return

    if ud.get("step") == "wait_open_cnt":
        if not text.isdigit(): return
        ud["opens"] = int(text)
        await get_mines_res(update, context)
        ud["step"] = "result"
        return

    if ud.get("step") == "wait_keno_amt":
        if not text.isdigit(): return
        ud["keno_amt"] = int(text)
        await update.message.reply_text("⚠ **Select Risk Level**", reply_markup=keno_risk_kb(), parse_mode="Markdown")
        ud["step"] = "wait_keno_risk"
        return

    if ud.get("step") == "wait_keno_risk":
        ud["keno_risk"] = text
        await get_keno_res(update, context)
        ud["step"] = "result"
        return

    if ud.get("step") == "result":
        if text == "❌ Loss":
            await update.message.reply_text("🔄 **Re-Analyzing...**", parse_mode="Markdown")
            func = ud.get("last_func")
            if func == "limbo": await get_limbo_res(update, context)
            elif func == "dice": await get_dice_res(update, context)
            elif func == "keno": await get_keno_res(update, context)
            elif func == "mines": await get_mines_res(update, context)
        elif text == "✅ Win":
            ud.clear()
            await update.message.reply_text("🎉 **Profit!** Back to Menu.", reply_markup=main_menu(), parse_mode="Markdown")
        return

# --- ADMIN COMMANDS ---

async def gen_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME:
        await unauthorized_alert(update)
        return

    if not context.args:
        await update.message.reply_text("Usage: `/gen 30m`, `/gen 2h`, `/gen 1d`", parse_mode="Markdown")
        return

    duration_str = context.args[0].lower()
    minutes = 0
    if duration_str.endswith('m'): minutes = int(duration_str[:-1])
    elif duration_str.endswith('h'): minutes = int(duration_str[:-1]) * 60
    elif duration_str.endswith('d'): minutes = int(duration_str[:-1]) * 1440
    else: minutes = int(duration_str) * 1440

    key = "KEY-" + str(uuid.uuid4())[:8].upper()
    data = load_data()
    data["keys"][key] = minutes
    save_data(data)

    dur_txt = f"{minutes}m" if minutes<60 else f"{minutes//60}h" if minutes<1440 else f"{minutes//1440}d"
    await update.message.reply_text(f"💎 **Key Generated**\n🔑 `{key}`\n⏳ {dur_txt}", parse_mode="Markdown")

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    key = context.args[0].strip()
    data = load_data()
    uid = str(update.effective_user.id)
    name = update.effective_user.first_name

    if key in data["keys"]:
        mins = data["keys"][key]
        expiry = datetime.now() + timedelta(minutes=mins)
        data["users"][uid] = {
            "expiry": expiry.isoformat(),
            "name": name,
            "joined": datetime.now().isoformat()
        }
        if "history" not in data: data["history"] = []
        if uid not in [h["uid"] for h in data["history"]]:
            data["history"].append({"uid": uid, "date": datetime.now().isoformat()})
            
        del data["keys"][key]
        save_data(data)
        # Activation ke baad seedha Menu dikhao
        await update.message.reply_text(f"✅ **Activated ({mins}m)!**\nWelcome {name}", reply_markup=main_menu())
    else:
        await update.message.reply_text("❌ Invalid Key")

async def end_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # User apna session khud end kar sake
    data = load_data()
    uid = str(update.effective_user.id)
    if uid in data["users"]:
        del data["users"][uid]
        save_data(data)
        await update.message.reply_text("🛑 **Session Ended.**\nApka license device se hata diya gaya hai.", reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("Aapke paas koi active license nahi hai.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME:
        await unauthorized_alert(update)
        return
    if not context.args: return
    msg = ' '.join(context.args)
    data = load_data()
    for uid in data["users"]:
        try: await context.bot.send_message(chat_id=uid, text=f"📢 {msg}", parse_mode="Markdown")
        except: pass
    await update.message.reply_text("✅ Broadcast Sent!")

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: return
    if not context.args: return
    uid = context.args[0]
    data = load_data()
    if uid in data["users"]:
        u = data["users"][uid]
        exp = datetime.fromisoformat(u["expiry"]).strftime("%d-%b %H:%M")
        await update.message.reply_text(f"👤 Name: {u['name']}\n⏳ Expiry: {exp}")
    else:
        await update.message.reply_text("User Not Found")

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: return
    await update.message.reply_text("👑 Admin: /gen, /broadcast, /info")

def main():
    print("🚀 Bot Starting...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen_key))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CommandHandler("end", end_session)) # New Command for Users
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("info", user_info))
    app.add_handler(CommandHandler("admin", admin_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    app.run_polling()

if __name__ == "__main__":
    main()
