import time

from binance_pairs import get_all_pairs
from scanner import get_klines
from signals import generate_signal
from chart import capture_chart
from overlay import draw_levels
from telegram_sender import send_signal


print("🚀 Bot starting...")

pairs = get_all_pairs()

print("✅ Binance pairs loaded")
print("Total pairs:", len(pairs))


while True:

    print("\n🔄 Starting new scan cycle...\n")

    for symbol in pairs[:20]:   # limit for testing

        try:

            print(f"📊 Checking {symbol}")

            df = get_klines(symbol)

            print(f"✔ Data loaded for {symbol}")

            signal = generate_signal(df)

            print(f"🔍 Signal result for {symbol}: {signal}")

            if signal:

                print(f"🚨 SIGNAL FOUND on {symbol}")

                trade, entry, sl, tp1, tp2, tp3 = signal

                print("📸 Capturing TradingView chart...")

                chart = capture_chart(symbol)

                print("🖊 Adding Entry / SL / TP overlay...")

                chart = draw_levels(chart, entry, sl, tp1, tp2, tp3)

                msg = f"""
💹 ${symbol.replace('USDT','')} — {trade}

Entry: {entry:.4f}
SL: {sl:.4f}
TP1: {tp1:.4f}
TP2: {tp2:.4f}
TP3: {tp3:.4f}

DYOR
"""

                print("📤 Sending signal to Telegram...")

                send_signal(msg, chart)

                print("✅ Signal sent successfully")

        except Exception as e:

            print(f"❌ ERROR on {symbol}")
            print(e)

    print("\n⏳ Waiting 5 minutes before next scan...\n")

    time.sleep(300)
