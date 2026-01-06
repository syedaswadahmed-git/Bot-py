import random, asyncio
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

TOKEN = "8595752857:AAE-snKxRbSau0OP9rw22p_Jkzus5qu0NC8"

BASE = Path(__file__).parent
CLIENT_IMG = BASE / "images/client_seed.jpg"
SERVER_IMG = BASE / "images/server_seed.jpg"

# ---------------- KEYBOARDS ----------------

def main_menu():
    return ReplyKeyboardMarkup(
        [["🎯 Limbo", "💣 Mines"], ["🎲 Dice", "🔢 Keno"]],
        resize_keyboard=True
    )

def win_loss_kb():
    return ReplyKeyboardMarkup([["✅ Win", "❌ Loss"]], resize_keyboard=True)

def mines_count_kb():
    rows, row = [], []
    for i in range(1, 25):
        row.append(str(i))
        if len(row) == 6:
            rows.append(row); row = []
    if row: rows.append(row)
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def open_count_kb():
    rows, row = [], []
    for i in range(1, 11):
        row.append(str(i))
        if len(row) == 5:
            rows.append(row); row = []
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def dice_kb():
    return ReplyKeyboardMarkup([["⬅ Left", "➡ Right"]], resize_keyboard=True)

def keno_count_kb():
    rows, row = [], []
    for i in range(1, 41):
        row.append(str(i))
        if len(row) == 8:
            rows.append(row); row = []
    if row: rows.append(row)
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def keno_risk_kb():
    return ReplyKeyboardMarkup(
        [["🟢 Low", "🟡 Medium", "🔴 High"]],
        resize_keyboard=True
    )

# ---------------- HELPERS ----------------

async def ask_client_seed(update):
    with open(CLIENT_IMG, "rb") as img:
        await update.message.reply_photo(img, caption="📌 Send Active Client Seed")

async def ask_server_seed(update):
    with open(SERVER_IMG, "rb") as img:
        await update.message.reply_photo(img, caption="📌 Send Active Server Seed")

async def analyzing(update, re=False):
    await update.message.reply_text("🔄 Re-Analyzing..." if re else "🔍 Analyzing...")
    await asyncio.sleep(random.randint(3, 5))

# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👑 Aswad Godfather Bot\n\nChoose Game 👇",
        reply_markup=main_menu()
    )

# ---------------- GAME LOGIC ----------------

async def limbo_predict(update, context):
    mult = random.choices(
        [1.3, 1.5, 1.8, 2, 3, 5, 10],
        [35, 30, 15, 10, 5, 3, 2]
    )[0]
    context.user_data["last_game"] = "🎯 Limbo"
    context.user_data["last_data"] = mult
    context.user_data["step"] = "result"
    await update.message.reply_text(
        f"🎯 Limbo Prediction\n\nMultiplier: {mult}x",
        reply_markup=win_loss_kb()
    )

async def dice_predict(update, context):
    side = random.choice(["⬅ Left", "➡ Right"])
    context.user_data["last_game"] = "🎲 Dice"
    context.user_data["last_data"] = side
    context.user_data["step"] = "result"
    await update.message.reply_text(
        f"🎲 Dice Prediction\n\nPlay: {side}",
        reply_markup=win_loss_kb()
    )

async def mines_predict(update, context):
    opens = context.user_data["opens"]
    cells = random.sample(range(25), opens)
    board = ""
    for i in range(25):
        board += "✅ " if i in cells else "⬜ "
        if (i + 1) % 5 == 0:
            board += "\n"
    context.user_data["last_game"] = "💣 Mines"
    context.user_data["last_data"] = opens
    context.user_data["step"] = "result"
    await update.message.reply_text(board, reply_markup=win_loss_kb())

async def keno_predict(update, context):
    count = context.user_data["keno_count"]
    nums = random.sample(range(1, 41), count)
    context.user_data["last_game"] = "🔢 Keno"
    context.user_data["last_data"] = count
    context.user_data["step"] = "result"
    await update.message.reply_text(
        f"🔢 Keno Numbers:\n{', '.join(map(str, nums))}",
        reply_markup=win_loss_kb()
    )

# ---------------- TEXT HANDLER ----------------

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    step = context.user_data.get("step")
    game = context.user_data.get("game")

    # GAME SELECT
    if text in ["🎯 Limbo", "💣 Mines", "🎲 Dice", "🔢 Keno"]:
        context.user_data.clear()
        context.user_data["game"] = text
        context.user_data["step"] = "client_seed"
        await ask_client_seed(update)
        return

    # CLIENT SEED
    if step == "client_seed":
        context.user_data["step"] = "server_seed"
        await ask_server_seed(update)
        return

    # SERVER SEED
    if step == "server_seed":
        await analyzing(update)
        if game == "🎯 Limbo":
            await limbo_predict(update, context)
        elif game == "🎲 Dice":
            await dice_predict(update, context)
        elif game == "💣 Mines":
            context.user_data["step"] = "mines_count"
            await update.message.reply_text(
                "💣 Select Mines Count",
                reply_markup=mines_count_kb()
            )
        elif game == "🔢 Keno":
            context.user_data["step"] = "keno_count"
            await update.message.reply_text(
                "🔢 How many numbers?",
                reply_markup=keno_count_kb()
            )
        return

    # MINES FLOW
    if step == "mines_count":
        if not text.isdigit():
            return
        context.user_data["mines"] = int(text)
        context.user_data["step"] = "open_count"
        await update.message.reply_text(
            "🧩 How many tiles to open?",
            reply_markup=open_count_kb()
        )
        return

    if step == "open_count":
        if not text.isdigit():
            return
        context.user_data["opens"] = int(text)
        await analyzing(update)
        await mines_predict(update, context)
        return

    # KENO FLOW
    if step == "keno_count":
        if not text.isdigit():
            return
        context.user_data["keno_count"] = int(text)
        context.user_data["step"] = "keno_risk"
        await update.message.reply_text(
            "⚠ Select Risk",
            reply_markup=keno_risk_kb()
        )
        return

    if step == "keno_risk":
        if text not in ["🟢 Low", "🟡 Medium", "🔴 High"]:
            return
        context.user_data["keno_risk"] = text
        await analyzing(update)
        await keno_predict(update, context)
        return

    # RESULT
    if step == "result":
        if text == "✅ Win":
            await update.message.reply_text(
                "🎉 WIN CONFIRMED",
                reply_markup=main_menu()
            )
            context.user_data.clear()
            return

        if text == "❌ Loss":
            await analyzing(update, re=True)
            last_game = context.user_data["last_game"]
            if last_game == "🎯 Limbo":
                await limbo_predict(update, context)
            elif last_game == "🎲 Dice":
                await dice_predict(update, context)
            elif last_game == "💣 Mines":
                await mines_predict(update, context)
            elif last_game == "🔢 Keno":
                await keno_predict(update, context)
            return

# ---------------- MAIN ----------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("🤖 Bot Running…")
    app.run_polling()

if __name__ == "__main__":
    main()
