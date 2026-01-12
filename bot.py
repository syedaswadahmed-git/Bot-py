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
ADMIN_USERNAME = "Merejigarketukde"  # Apna username bina @ ke

BASE = Path(__file__).parent
DATA_FILE = BASE / "bot_data.json"
CLIENT_IMG = BASE / "images/client_seed.jpg"
SERVER_IMG = BASE / "images/server_seed.jpg"

# --- ZABARDAST DIALOGUES & PUNCHLINES ---
def get_hype_message():
    """Har result ke neeche ye random dialogues aayenge"""
    return random.choice([
        "🔥 **Abhi aayega na maza bhidu!**",
        "💣 **Pura Casino hila dalenge aaj!**",
        "🤑 **Loot lo, mauka haath se na jaye!**",
        "🚀 **System Hack successful raha boss!**",
        "💀 **Ye pattern kabhi fail nahi hota!**",
        "🦅 **Baaz ki nazar rakh, profit pakka hai!**"
    ])

# --- DATA MANAGEMENT ---
def load_data():
    if DATA_FILE.exists():
        try: return json.load(open(DATA_FILE, "r"))
        except: return {"users": {}, "keys": {}, "banned": [], "all_ids": []}
    return {"users": {}, "keys": {}, "banned": [], "all_ids": []}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

def add_id_to_db(chat_id):
    data = load_data()
    cid = str(chat_id)
    if "all_ids" not in data: data["all_ids"] = []
    if cid not in data["all_ids"]:
        data["all_ids"].append(cid)
        save_data(data)

# --- KEYBOARDS (ENGLISH BUTTONS - EASIER TO READ) ---
def main_menu():
    return ReplyKeyboardMarkup([
        ["🎯 Limbo", "💣 Mines"], 
        ["🎲 Dice", "🔢 Keno"],
        ["🐉 Dragon Tower"]
    ], resize_keyboard=True)

def win_loss_kb():
    return ReplyKeyboardMarkup([["✅ Win (Jeet Gaya)", "❌ Loss (Lag Gaye)"]], resize_keyboard=True)

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
    return ReplyKeyboardMarkup([["🟢 Low Risk", "🟡 Medium Risk"], ["🔴 High Risk", "🔙 Menu"]], resize_keyboard=True)

def dragon_diff_kb():
    return ReplyKeyboardMarkup([
        ["🟢 Easy", "🟡 Medium"],
        ["🔴 Hard", "🔥 Expert"],
        ["☠️ Master", "🔙 Menu"]
    ], resize_keyboard=True)

def dragon_steps_kb():
    return ReplyKeyboardMarkup([["3 Steps", "5 Steps"], ["8 Steps", "10 Steps"], ["🔙 Menu"]], resize_keyboard=True)

# --- KHATARNAK ANIMATIONS ---
async def show_verified_animation(update, seed_type, user_input):
    msg = await update.message.reply_text(f"⏳ **{seed_type} Check kar raha hu...**", parse_mode="Markdown")
    await asyncio.sleep(0.8)
    await msg.edit_text(f"✅ **{seed_type} Asli Hai!**\nInput: `{user_input}`\nStatus: 🛡️ **Verified Boss!**", parse_mode="Markdown")
    await asyncio.sleep(0.8)
    await msg.delete()

async def play_hacker_animation(update):
    msg = await update.message.reply_text("⚡ **Server se Connect kar raha hu...**", parse_mode="Markdown")
    await asyncio.sleep(0.5)
    await msg.edit_text("👨‍💻 **Algorithm Tod raha hu...**", parse_mode="Markdown")
    await asyncio.sleep(0.5)
    await msg.edit_text("🔍 **History Check kar raha hu...**", parse_mode="Markdown")
    await asyncio.sleep(0.5)
    await msg.edit_text("🔓 **JACKPOT PATTERN MIL GAYA!**", parse_mode="Markdown")
    await asyncio.sleep(0.5)
    await msg.delete()

# --- GAME LOGIC ---

# 1. Limbo
async def get_limbo_res(update, context):
    await play_hacker_animation(update)
    target = random.choices([1.5, 2.0, 3.0, 10.0], [40, 30, 20, 10])[0]
    roll = target + round(random.uniform(0.1, 15.0), 2)
    
    msg = (f"🎯 **LIMBO KA JAADU**\n\n"
           f"🎯 Target: `{target}x`\n"
           f"🚀 Roll Aayega: `{roll}x`\n"
           f"👉 **Chup chap {target}x par laga de!**\n\n"
           f"{get_hype_message()}")
           
    context.user_data["last_func"] = "limbo"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

# 2. Dice
async def get_dice_res(update, context):
    await play_hacker_animation(update)
    roll = random.randint(40, 98)
    condition = "Over 40" if roll > 40 else "Under 40"
    
    msg = (f"🎲 **DICE HACKING**\n\n"
           f"🎰 Prediction: **{condition}**\n"
           f"🎲 Expected Number: `{roll}`\n"
           f"⚡ Slider set kar aur paisa bana!\n\n"
           f"{get_hype_message()}")
           
    context.user_data["last_func"] = "dice"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

# 3. Keno
async def get_keno_res(update, context):
    await play_hacker_animation(update)
    amt = context.user_data.get("keno_amt", 4)
    risk = context.user_data.get("keno_risk", "High")
    nums = random.sample(range(1, 41), amt)
    nums.sort()
    
    msg = (f"🔢 **KENO LEAKED NUMBERS**\n\n"
           f"🔮 Numbers: `{', '.join(map(str, nums))}`\n"
           f"🔥 Risk Level: {risk}\n"
           f"Bina dare ye number laga de!\n\n"
           f"{get_hype_message()}")
           
    context.user_data["last_func"] = "keno"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

# 4. Mines
async def get_mines_res(update, context):
    await play_hacker_animation(update)
    mines = context.user_data.get("mines", 3)
    opens = context.user_data.get("opens", 3)
    cells = random.sample(range(25), opens)
    grid = ["⬜"] * 25
    for c in cells: grid[c] = "⭐"
    board_str = ""
    for i in range(0, 25, 5): board_str += "  ".join(grid[i:i+5]) + "\n"
    
    msg = (f"💣 **MINES KA BAAP**\n"
           f"💣 Mines: `{mines}` | 💎 Open: `{opens}`\n\n"
           f"{board_str}\n\n"
           f"{get_hype_message()}")
           
    context.user_data["last_func"] = "mines"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")

# 5. Dragon Tower
async def get_dragon_res(update, context):
    await play_hacker_animation(update)
    diff = context.user_data.get("dragon_diff", "Easy")
    steps_txt = context.user_data.get("dragon_steps", "5 Steps")
    
    cols = 4
    if "Easy" in diff: cols = 4
    elif "Medium" in diff: cols = 3
    elif "Hard" in diff: cols = 2
    elif "Expert" in diff: cols = 3
    elif "Master" in diff: cols = 4
    
    steps = int(steps_txt.split()[0])
    board = ""
    for i in range(steps):
        row = ["💣"] * cols
        safe_idx = random.randint(0, cols-1)
        row[safe_idx] = "🥚"
        board = " ".join(row) + "\n" + board
        
    msg = (f"🐉 **DRAGON TOWER HACK**\n"
           f"🔥 Mode: {diff}\n"
           f"👣 Steps: {steps}\n\n"
           f"{board}\n"
           f"👉 **Sirf Ande (Egg) pe kudna!**\n\n"
           f"{get_hype_message()}")
           
    context.user_data["last_func"] = "dragon"
    await update.message.reply_text(msg, reply_markup=win_loss_kb(), parse_mode="Markdown")


# --- REMINDER SYSTEM (Background Task) ---
async def check_expiry_reminders(context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    now = datetime.now()
    users_to_save = False
    
    for uid, info in data["users"].items():
        if isinstance(info, dict):
            try:
                expiry = datetime.fromisoformat(info["expiry"])
                time_left = expiry - now
                
                # 1 Day Reminder
                if timedelta(hours=23) < time_left < timedelta(hours=24):
                    if not info.get("reminded_24h"):
                        try:
                            await context.bot.send_message(uid, "⚠️ **WARNING BOSS:**\nSirf 24 Ghante bache hain! License renew kar lo warna service band ho jayegi.")
                            info["reminded_24h"] = True
                            users_to_save = True
                        except: pass

                # 1 Hour Reminder
                elif timedelta(minutes=55) < time_left < timedelta(minutes=65):
                    if not info.get("reminded_1h"):
                        try:
                            await context.bot.send_message(uid, "🚨 **KHATRA:**\nSirf 1 Ghanta bacha hai! Jaldi Admin se baat karo: @Merejigarketukde")
                            info["reminded_1h"] = True
                            users_to_save = True
                        except: pass
                        
            except: pass
            
    if users_to_save:
        save_data(data)

# --- AUTH & START ---
async def check_auth(update: Update):
    data = load_data()
    uid = str(update.effective_user.id)
    
    if uid in data.get("banned", []):
        await update.message.reply_text("🚫 **TERE KO BAN KAR DIYA HAI!**\nAdmin se baat kar.")
        return False
        
    if uid not in data["users"]: return False
    
    info = data["users"][uid]
    if isinstance(info, str): return False
    
    if datetime.now() > datetime.fromisoformat(info["expiry"]):
        await update.message.reply_text("⚠️ **KEY EXPIRE HO GAYI!**\nNaya maal kharido: @Merejigarketukde")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_id_to_db(user.id)
    
    if await check_auth(update):
        await update.message.reply_text(f"👑 **Aaja Boss {user.first_name}!**\nSystem set hai, lootna shuru karein?", reply_markup=main_menu(), parse_mode="Markdown")
    else:
        # PRICING POPUP (Roman Hindi)
        msg = (
            "🔥 **Aswad Godfather VIP** 🔥\n"
            "💎 **100% Confirm Hacking Tool**\n\n"
            "Ye free ka maal nahi hai, Paisa lagta hai quality ka!\n\n"
            "🕐 **1 Hour** – ₹19 (Trial)\n"
            "📅 **7 Days** – ₹139 (Best)\n"
            "📆 **1 Month** – ₹339 (Pro)\n\n"
            "💳 **Key Kharido:** @Merejigarketukde\n"
            "🔑 **Activate Kaise Karein:** `/activate KEY`"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")

# --- TEXT HANDLER ---
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_id_to_db(update.effective_user.id)
    
    if not await check_auth(update):
        await start(update, context)
        return

    text = update.message.text
    ud = context.user_data

    # Back Button
    if text == "🔙 Menu":
        ud.clear()
        await update.message.reply_text("🏠 **Main Menu**", reply_markup=main_menu(), parse_mode="Markdown")
        return

    # Game Select
    if text in ["🎯 Limbo", "💣 Mines", "🎲 Dice", "🔢 Keno", "🐉 Dragon Tower"]:
        ud.clear()
        ud["game"] = text
        caption_txt = "📌 **Active Client Seed Bhejo**\n(Game settings se copy karke yahan paste kar)"
        
        if CLIENT_IMG.exists():
            await update.message.reply_photo(CLIENT_IMG, caption=caption_txt, parse_mode="Markdown")
        else:
            await update.message.reply_text(caption_txt, parse_mode="Markdown")
        ud["step"] = "wait_client"
        return

    # Client Seed Input
    if ud.get("step") == "wait_client":
        await show_verified_animation(update, "Client Seed", text)
        caption_txt = "📌 **Ab Server Seed Bhejo**\n(Ye wala hidden hota hai, reveal karke bhejo)"
        
        if SERVER_IMG.exists():
            await update.message.reply_photo(SERVER_IMG, caption=caption_txt, parse_mode="Markdown")
        else:
            await update.message.reply_text(caption_txt, parse_mode="Markdown")
        ud["step"] = "wait_server"
        return

    # Server Seed Input
    if ud.get("step") == "wait_server":
        await show_verified_animation(update, "Server Seed", text)
        game = ud.get("game")
        
        if game == "💣 Mines":
            await update.message.reply_text("💣 **Kitne Mines Select Kiye Hain?**", reply_markup=mines_count_kb())
            ud["step"] = "wait_mines_cnt"
        elif game == "🔢 Keno":
            await update.message.reply_text("🔢 **Kitne Numbers Khelne Hain?**", reply_markup=keno_amt_kb())
            ud["step"] = "wait_keno_amt"
        elif game == "🐉 Dragon Tower":
            await update.message.reply_text("🐉 **Difficulty Kya Hai?**", reply_markup=dragon_diff_kb())
            ud["step"] = "wait_dragon_diff"
        elif game == "🎯 Limbo":
            await get_limbo_res(update, context)
            ud["step"] = "result"
        elif game == "🎲 Dice":
            await get_dice_res(update, context)
            ud["step"] = "result"
        return

    # --- GAME CONFIGS ---
    if ud.get("step") == "wait_mines_cnt":
        if not text.isdigit() or not (1 <= int(text) <= 24): return
        ud["mines"] = int(text)
        await update.message.reply_text("💎 **Kitne dabbe (Tiles) kholne hain?**", reply_markup=open_count_kb())
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
        await update.message.reply_text("⚠ **Risk Kitna Lena Hai?**", reply_markup=keno_risk_kb())
        ud["step"] = "wait_keno_risk"
        return

    if ud.get("step") == "wait_keno_risk":
        ud["keno_risk"] = text
        await get_keno_res(update, context)
        ud["step"] = "result"
        return

    if ud.get("step") == "wait_dragon_diff":
        ud["dragon_diff"] = text
        await update.message.reply_text("👣 **Kitne Steps upar jana hai?**", reply_markup=dragon_steps_kb())
        ud["step"] = "wait_dragon_steps"
        return

    if ud.get("step") == "wait_dragon_steps":
        ud["dragon_steps"] = text
        await get_dragon_res(update, context)
        ud["step"] = "result"
        return

    # --- RESULT LOOP ---
    if ud.get("step") == "result":
        if "Loss" in text:
            await update.message.reply_text("🔄 **Ruk! Dobara Analyze kar raha hu...**", parse_mode="Markdown")
            # Loop back to same function
            func = ud.get("last_func")
            if func == "limbo": await get_limbo_res(update, context)
            elif func == "dice": await get_dice_res(update, context)
            elif func == "keno": await get_keno_res(update, context)
            elif func == "mines": await get_mines_res(update, context)
            elif func == "dragon": await get_dragon_res(update, context)
            
        elif "Win" in text:
            ud.clear()
            await update.message.reply_text("🎉 **Paisa hi Paisa!** Chal ab menu pe wapas.", reply_markup=main_menu(), parse_mode="Markdown")
        return

# --- ADMIN COMMANDS ---
async def unauthorized_alert(update):
    await update.message.reply_text("⛔ **Teri Aukaat Nahi Hai Ye Command Chalane Ki!**")

async def gen_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: 
        await unauthorized_alert(update)
        return
    if not context.args:
        await update.message.reply_text("Aise likh: /gen 1h, /gen 1d, /gen 7d")
        return
    
    s = context.args[0].lower()
    m = 0
    if s.endswith('m'): m = int(s[:-1])
    elif s.endswith('h'): m = int(s[:-1])*60
    elif s.endswith('d'): m = int(s[:-1])*1440
    
    key = "KEY-" + str(uuid.uuid4())[:8].upper()
    data = load_data()
    data["keys"][key] = m
    save_data(data)
    await update.message.reply_text(f"💎 **Key Ban Gayi Boss!**\n🔑 `{key}`\n⏳ Duration: {s}", parse_mode="Markdown")

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    key = context.args[0].strip()
    data = load_data()
    uid = str(update.effective_user.id)
    
    if key in data["keys"]:
        m = data["keys"][key]
        exp = datetime.now() + timedelta(minutes=m)
        data["users"][uid] = {
            "expiry": exp.isoformat(),
            "name": update.effective_user.first_name,
            "reminded_24h": False,
            "reminded_1h": False
        }
        del data["keys"][key]
        save_data(data)
        await update.message.reply_text("✅ **Mubarak Ho! Key Activate Ho Gayi!**", reply_markup=main_menu())
    else:
        await update.message.reply_text("❌ **Galat Key Hai!** Sahi wali daal.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: return
    if not context.args: return
    msg = ' '.join(context.args)
    data = load_data()
    ids = data.get("all_ids", []) + list(data["users"].keys())
    ids = list(set(ids))
    
    sent = 0
    await update.message.reply_text(f"📣 {len(ids)} logo ko message bhej raha hu...")
    for uid in ids:
        try:
            await context.bot.send_message(uid, f"📢 **ANNOUNCEMENT**\n\n{msg}", parse_mode="Markdown")
            sent += 1
        except: pass
    await update.message.reply_text(f"✅ {sent} logo ko message chala gaya.")

async def admin_utils(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME:
        await unauthorized_alert(update)
        return
    
    cmd = update.message.text.split()[0]
    data = load_data()
    
    if cmd == "/users":
        msg = "👥 **Active Users:**\n"
        for uid, info in data["users"].items():
            if isinstance(info, dict) and datetime.now() < datetime.fromisoformat(info["expiry"]):
                msg += f"{info['name']} (`{uid}`)\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    elif cmd == "/keys":
        msg = "🔑 **Pending Keys:**\n" + "\n".join([f"`{k}` ({v}m)" for k,v in data["keys"].items()])
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    elif cmd == "/revoke":
        if context.args:
            k = context.args[0]
            if k in data["keys"]:
                del data["keys"][k]
                save_data(data)
                await update.message.reply_text("🗑️ Key Delete kar di.")
                
    elif cmd == "/info":
        if context.args and context.args[0] in data["users"]:
            u = data["users"][context.args[0]]
            await update.message.reply_text(str(u))

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME: return
    await update.message.reply_text("👑 /gen, /users, /keys, /revoke, /broadcast, /info")

def main():
    print("🚀 Bot Starting...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    job_queue = app.job_queue
    job_queue.run_repeating(check_expiry_reminders, interval=300, first=10)
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen_key))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CommandHandler("broadcast", broadcast))
    
    app.add_handler(CommandHandler("users", admin_utils))
    app.add_handler(CommandHandler("keys", admin_utils))
    app.add_handler(CommandHandler("revoke", admin_utils))
    app.add_handler(CommandHandler("info", admin_utils))
    app.add_handler(CommandHandler("admin", admin_help))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    app.run_polling()

if __name__ == "__main__":
    main()
