import random, asyncio, json, hashlib, uuid, os
from datetime import datetime, timedelta
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# --- CONFIGURATION ---
TOKEN = "8595752857:AAE-snKxRbSau0OP9rw22p_Jkzus5qu0NC8"
ADMIN_USERNAME = "Merejigarketukde" # Apna username yahan sahi rakhein

BASE = Path(__file__).parent
DATA_FILE = BASE / "bot_data.json"
# Images path ensure karein ki sahi hai
CLIENT_IMG = BASE / "images/client_seed.jpg"
SERVER_IMG = BASE / "images/server_seed.jpg"

# --- DATA MANAGEMENT ---
def load_data():
    if DATA_FILE.exists():
        try: return json.load(open(DATA_FILE, "r"))
        except: return {"users": {}, "keys": {}, "banned": []}
    return {"users": {}, "keys": {}, "banned": []}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- KEYBOARDS ---
def main_menu():
    return ReplyKeyboardMarkup([["🎯 Limbo", "💣 Mines"], ["🎲 Dice", "🔢 Keno"]], resize_keyboard=True)

def win_loss_kb():
    return ReplyKeyboardMarkup([["✅ Win", "❌ Loss"]], resize_keyboard=True)

def mines_count_kb():
    # 1 to 24 buttons
    rows, row = [], []
    for i in range(1, 25):
        row.append(str(i))
        if len(row) == 6: rows.append(row); row = []
    if row: rows.append(row)
    rows.append(["🔙 Menu"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def open_count_kb():
    # 1 to 10 buttons
    rows, row = [], []
    for i in range(1, 11):
        row.append(str(i))
        if len(row) == 5: rows.append(row); row = []
    if row: rows.append(row)
    rows.append(["🔙 Menu"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

# --- AUTH & ANIMATIONS ---
async def check_auth(update: Update):
    data = load_data()
    uid = str(update.effective_user.id)
    
    # Check Ban
    if uid in data.get("banned", []):
        await update.message.reply_text("🚫 You are BANNED by Admin.")
        return False

    # Check License Existence
    if uid not in data["users"]:
        await update.message.reply_text("🔒 **LOCKED**\n\nBuy Key from Admin: @Merejigarketukde\nUse: `/activate KEY`", parse_mode="Markdown")
        return False
    
    # Check Expiry
    expiry = datetime.fromisoformat(data["users"][uid])
    if datetime.now() > expiry:
        await update.message.reply_text("⚠️ License Expired!\nContact @Merejigarketukde for new key.")
        return False
    
    return True

async def show_verified_animation(update, seed_type):
    # Fake loading animation for realism
    msg = await update.message.reply_text(f"⏳ **Verifying {seed_type} Seed...**", parse_mode="Markdown")
    await asyncio.sleep(1.5)
    
    # Generate random hash for look
    fake_hash = hashlib.sha256(str(random.random()).encode()).hexdigest()[:12].upper()
    await msg.edit_text(f"✅ **{seed_type} Verified!**\nHash: `{fake_hash}`\nStatus: 🛡️ Authenticated", parse_mode="Markdown")
    await asyncio.sleep(1.5)
    await msg.delete()

# --- ADVANCED GAME LOGIC ---

async def get_limbo_res(update, context):
    # Ultra Logic: Target vs Result
    target = random.choices([1.5, 2.0, 3.0, 10.0], [40, 30, 20, 10])[0]
    # Roll is slightly higher than target mostly to show win potential
    roll = target + round(random.uniform(0.1, 15.0), 2)
    
    msg = (f"🎯 **LIMBO PREDICTION**\n\n"
           f"🎯 Target: `{target}x`\n"
           f"🚀 Roll: `{roll}x`\n\n"
           f"👉 **Bet on {target}x or lower**")
    
    context.user_data["last_func"] = "limbo"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

async def get_dice_res(update, context):
    # Ultra Logic: Roll Number
    roll = random.randint(40, 98)
    condition = "Over 40" if roll > 40 else "Under 40"
    
    msg = (f"🎲 **DICE PREDICTION**\n\n"
           f"🎰 Prediction: **{condition}**\n"
           f"🎲 Expected Roll: `{roll}`\n\n"
           f"⚡ Drag slider to secure zone.")
           
    context.user_data["last_func"] = "dice"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

async def get_keno_res(update, context):
    nums = random.sample(range(1, 41), 4)
    msg = (f"🔢 **KENO PREDICTION**\n\n"
           f"🔮 **Numbers:** `{', '.join(map(str, nums))}`\n"
           f"🔥 Risk: High\n\n"
           f"Play these 4 numbers.")
    context.user_data["last_func"] = "keno"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

async def get_mines_res(update, context):
    mines = context.user_data.get("mines", 3)
    opens = context.user_data.get("opens", 3)
    
    # Random Board Generation
    cells = random.sample(range(25), opens)
    grid = ["⬜"] * 25
    for c in cells: grid[c] = "⭐" # Star for safe spot
    
    # Format 5x5 Grid
    board_str = ""
    for i in range(0, 25, 5):
        board_str += "  ".join(grid[i:i+5]) + "\n"
        
    msg = (f"💣 **MINES PREDICTION**\n"
           f"💣 Mines: `{mines}` | 💎 Open: `{opens}`\n\n"
           f"{board_str}")
           
    context.user_data["last_func"] = "mines"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

# --- HANDLER FLOW ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Start par user data clear mat karo, bas check karo
    if await check_auth(update):
        await update.message.reply_text("👑 **Welcome Back Boss!**", reply_markup=main_menu(), parse_mode="Markdown")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Sabse pehle license check
    if not await check_auth(update): return
    
    text = update.message.text
    ud = context.user_data
    
    # 2. Main Menu Logic
    if text == "🔙 Menu":
        ud.clear() # Reset game state
        await update.message.reply_text("🏠 **Main Menu**", reply_markup=main_menu(), parse_mode="Markdown")
        return

    # 3. Game Selection -> Ask Client Seed
    if text in ["🎯 Limbo", "💣 Mines", "🎲 Dice", "🔢 Keno"]:
        ud.clear() # Purana game data saaf karo
        ud["game"] = text
        
        # Check if image exists, else send text
        if CLIENT_IMG.exists():
            await update.message.reply_photo(CLIENT_IMG, caption="📌 **Send Active Client Seed**\n(Copy from game settings)", parse_mode="Markdown")
        else:
            await update.message.reply_text("📌 **Send Active Client Seed**", parse_mode="Markdown")
            
        ud["step"] = "wait_client"
        return

    # 4. Handle Client Seed -> Ask Server Seed
    if ud.get("step") == "wait_client":
        # Fake verification time
        await show_verified_animation(update, "Client")
        
        if SERVER_IMG.exists():
            await update.message.reply_photo(SERVER_IMG, caption="📌 **Send Active Server Seed**\n(Copy from game settings)", parse_mode="Markdown")
        else:
            await update.message.reply_text("📌 **Send Active Server Seed**", parse_mode="Markdown")
            
        ud["step"] = "wait_server"
        return

    # 5. Handle Server Seed -> Decide Game Path
    if ud.get("step") == "wait_server":
        await show_verified_animation(update, "Server")
        
        game = ud.get("game")
        
        if game == "💣 Mines":
            await update.message.reply_text("💣 **How many Mines?**\nSelect from 1 to 24:", reply_markup=mines_count_kb(), parse_mode="Markdown")
            ud["step"] = "wait_mines_cnt"
            
        elif game == "🎯 Limbo":
            await get_limbo_res(update, context)
            ud["step"] = "result"
            
        elif game == "🎲 Dice":
            await get_dice_res(update, context)
            ud["step"] = "result"
            
        elif game == "🔢 Keno":
            await get_keno_res(update, context)
            ud["step"] = "result"
        return

    # 6. Mines Specific Flow
    if ud.get("step") == "wait_mines_cnt":
        if not text.isdigit() or not (1 <= int(text) <= 24):
            await update.message.reply_text("⚠️ Please select number between 1-24")
            return
        ud["mines"] = int(text)
        await update.message.reply_text(f"💎 **Mines: {text}**\nHow many tiles to open?", reply_markup=open_count_kb(), parse_mode="Markdown")
        ud["step"] = "wait_open_cnt"
        return

    if ud.get("step") == "wait_open_cnt":
        if not text.isdigit():
            await update.message.reply_text("⚠️ Please select a number.")
            return
        ud["opens"] = int(text)
        await get_mines_res(update, context)
        ud["step"] = "result"
        return

    # 7. Result Handling (Win/Loss)
    if ud.get("step") == "result":
        if text == "❌ Loss":
            await update.message.reply_text("🔄 **Re-Analyzing Pattern...**", parse_mode="Markdown")
            await asyncio.sleep(2)
            
            # Re-run the last game function with NEW random result
            func_type = ud.get("last_func")
            if func_type == "limbo": await get_limbo_res(update, context)
            elif func_type == "dice": await get_dice_res(update, context)
            elif func_type == "keno": await get_keno_res(update, context)
            elif func_type == "mines": await get_mines_res(update, context)
            
        elif text == "✅ Win":
            ud.clear()
            await update.message.reply_text("🎉 **Profit Secured!**\nReturning to Menu...", reply_markup=main_menu(), parse_mode="Markdown")
        return

# --- ADMIN COMMANDS ---
async def gen_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: return
    
    try: days = int(context.args[0])
    except: days = 1 # Default
    
    key = "KEY-" + str(uuid.uuid4())[:8].upper()
    data = load_data()
    data["keys"][key] = days
    save_data(data)
    
    await update.message.reply_text(f"💎 **Premium Key Generated**\n\n🔑 `{key}`\n⏳ Validity: {days} Days", parse_mode="Markdown")

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/activate KEY`", parse_mode="Markdown")
        return
        
    key = context.args[0].strip()
    data = load_data()
    user_id = str(update.effective_user.id)
    
    if key in data["keys"]:
        days = data["keys"][key]
        # Calculate new expiry
        new_expiry = datetime.now() + timedelta(days=days)
        data["users"][user_id] = new_expiry.isoformat()
        
        del data["keys"][key] # Burn key
        save_data(data)
        
        await update.message.reply_text(f"✅ **Activation Successful!**\n\n📅 Expires on: {new_expiry.strftime('%d-%b-%Y')}\nEnjoy the game!", reply_markup=main_menu(), parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ **Invalid or Used Key**", parse_mode="Markdown")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: return
    if not context.args: return
    
    target = context.args[0]
    data = load_data()
    if "banned" not in data: data["banned"] = []
    
    if target not in data["banned"]:
        data["banned"].append(target)
        save_data(data)
        await update.message.reply_text(f"🚫 User {target} Banned.")
    else:
        await update.message.reply_text("Already Banned.")

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: return
    msg = ("👑 **GOD PANEL**\n"
           "/gen <days> - Create Key\n"
           "/ban <id> - Ban User\n"
           "/users - Check Users")
    await update.message.reply_text(msg)

# --- MAIN ---
def main():
    print("🚀 Bot Starting...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen_key))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("admin", admin_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    app.run_polling()

if __name__ == "__main__":
    main()
