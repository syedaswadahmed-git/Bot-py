import random, asyncio
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

TOKEN = "8595752857:AAE-snKxRbSau0OP9rw22p_Jkzus5qu0NC8"

BASE = Path(__file__).parent
CLIENT_IMG = BASE / "images/client_seed.jpg"
SERVER_IMG = BASE / "images/server_seed.jpg"

# ================= KEYBOARDS =================

def main_menu():
    return ReplyKeyboardMarkup(
        [["🎯 Limbo", "💣 Mines"],
         ["🎲 Dice", "🔢 Keno"]],
        resize_keyboard=True
    )

def win_loss_kb():
    return ReplyKeyboardMarkup(
        [["✅ Win", "❌ Loss"]],
        resize_keyboard=True
    )

def mines_count_kb():
    rows, row = [], []
    for i in range(1, 25):
        row.append(str(i))
        if len(row) == 6:
            rows.append(row); row = []
    if row: rows.append(row)
    rows.append(["🏠 Main Menu"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def open_count_kb():
    rows, row = [], []
    for i in range(1, 11):
        row.append(str(i))
        if len(row) == 5:
            rows.append(row); row = []
    rows.append(["🏠 Main Menu"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def dice_kb():
    return ReplyKeyboardMarkup(
        [["⬅ Left", "➡ Right"], ["🏠 Main Menu"]],
        resize_keyboard=True
    )

def keno_risk_kb():
    return ReplyKeyboardMarkup(
        [["🟢 Low", "🟡 Medium", "🔴 High"], ["🏠 Main Menu"]],
        resize_keyboard=True
    )

# ================= HELPERS =================

async def ask_client_seed(update):
    with open(CLIENT_IMG, "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption="📌 Send Active Client Seed"
        )

async def ask_server_seed(update):
    with open(SERVER_IMG, "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption="📌 Send Active Server Seed"
        )

async def analysis(update):
    await update.message.reply_text("🔍 Analyzing...")
    await asyncio.sleep(random.randint(3, 5))

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👑 *Aswad Godfather Bot*\n\nChoose a game 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ================= HANDLER =================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    step = context.user_data.get("step")
    game = context.user_data.get("game")

    if text == "🏠 Main Menu":
        await start(update, context)
        return

    # -------- GAME SELECT --------
    if text in ["🎯 Limbo", "💣 Mines", "🎲 Dice", "🔢 Keno"]:
        context.user_data.clear()
        context.user_data["game"] = text
        context.user_data["step"] = "client_seed"
        await ask_client_seed(update)
        return

    # -------- CLIENT SEED --------
    if step == "client_seed":
        context.user_data["step"] = "server_seed"
        await ask_server_seed(update)
        return

    # -------- SERVER SEED --------
    if step == "server_seed":
        await analysis(update)

        if game == "🎯 Limbo":
            mult = random.choices(
                [1.3, 1.5, 1.8, 2, 3, 5, 10],
                weights=[40, 30, 15, 7, 5, 2, 1]
            )[0]
            context.user_data["step"] = "result"
            await update.message.reply_text(
                f"🎯 *Limbo Prediction*\n\nMultiplier: *{mult}x*",
                reply_markup=win_loss_kb(),
                parse_mode="Markdown"
            )
            return

        if game == "🎲 Dice":
            side = random.choice(["⬅ Left", "➡ Right"])
            context.user_data["step"] = "result"
            await update.message.reply_text(
                f"🎲 *Dice Prediction*\n\nPlay: *{side}*",
                reply_markup=win_loss_kb(),
                parse_mode="Markdown"
            )
            return

        if game == "🔢 Keno":
            context.user_data["step"] = "keno_count"
            await update.message.reply_text(
                "🔢 How many numbers do you want to select? (1–40)"
            )
            return

        if game == "💣 Mines":
            context.user_data["step"] = "mines_count"
            await update.message.reply_text(
                "💣 Select number of mines",
                reply_markup=mines_count_kb()
            )
            return

    # -------- MINES --------
    if step == "mines_count" and text.isdigit():
        context.user_data["mines"] = int(text)
        context.user_data["step"] = "open_count"
        await update.message.reply_text(
            "🧩 How many tiles to open?",
            reply_markup=open_count_kb()
        )
        return

    if step == "open_count" and text.isdigit():
        await analysis(update)
        opens = int(text)
        cells = random.sample(range(25), opens)
        board = ""
        for i in range(25):
            board += "✅ " if i in cells else "⬜ "
            if (i+1) % 5 == 0:
                board += "\n"

        context.user_data["step"] = "result"
        await update.message.reply_text(
            f"💣 *Mines Prediction*\n\n{board}",
            reply_markup=win_loss_kb(),
            parse_mode="Markdown"
        )
        return

    # -------- KENO --------
    if step == "keno_count" and text.isdigit():
        count = int(text)
        if not 1 <= count <= 40:
            return
        context.user_data["keno_count"] = count
        context.user_data["step"] = "keno_risk"
        await update.message.reply_text(
            "⚠️ Select Risk Level",
            reply_markup=keno_risk_kb()
        )
        return

    if step == "keno_risk" and text in ["🟢 Low", "🟡 Medium", "🔴 High"]:
        await analysis(update)

        count = context.user_data["keno_count"]
        risk = text

        picks = 3 if risk == "🟢 Low" else 5 if risk == "🟡 Medium" else 8
        picks = min(picks, count)

        nums = random.sample(range(1, 41), picks)
        context.user_data["step"] = "result"

        await update.message.reply_text(
            f"🔢 *Keno Prediction*\n\n"
            f"Risk: {risk}\n"
            f"Numbers: {', '.join(map(str, nums))}",
            reply_markup=win_loss_kb(),
            parse_mode="Markdown"
        )
        return

    # -------- RESULT --------
    if step == "result":
        if text == "✅ Win":
            await start(update, context)
            return

        if text == "❌ Loss":
            context.user_data["step"] = "server_seed"
            await analysis(update)
            await ask_server_seed(update)
            return

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("🤖 Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()

