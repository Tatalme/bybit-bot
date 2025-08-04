import requests
import time
import schedule

BOT_TOKEN = '8034731678:AAERbF-tDGvX1doGqnOFOPjNGV8COPBIyx4'
CHAT_ID = '449453561'
SYMBOLS = ["TONUSDT", "INJUSDT", "XRPUSDT", "APTUSDT", "HBARUSDT", "TIAUSDT"]

def get_bybit_prices(symbols):
    url = "https://api.bybit.com/v5/market/tickers?category=linear"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        result = data.get("result", {}).get("list", [])
        prices = {}
        for item in result:
            symbol = item["symbol"]
            if symbol in symbols:
                prices[symbol] = item["lastPrice"]
        return prices
    except Exception as e:
        return {"error": str(e)}

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def job():
    prices = get_bybit_prices(SYMBOLS)
    if "error" in prices:
        send_message(f"❌ Ошибка получения цен: {prices['error']}")
    else:
        msg = "<b>📊 Котировки Bybit:</b>\n\n"
        for symbol, price in prices.items():
            msg += f"{symbol}: <code>{price}</code> USDT\n"
        send_message(msg)
        print("✅ Отправлено в Telegram")

schedule.every(30).minutes.do(job)
job()

while True:
    schedule.run_pending()
    time.sleep(5)