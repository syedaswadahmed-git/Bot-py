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
