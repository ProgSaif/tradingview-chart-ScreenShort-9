import time

from binance_pairs import get_all_pairs
from scanner import get_klines
from signals import generate_signal
from chart import capture_chart
from overlay import draw_levels
from telegram_sender import send_signal


pairs = get_all_pairs()

print("Total pairs:", len(pairs))


while True:

    for symbol in pairs:

        try:

            df = get_klines(symbol)

            signal = generate_signal(df)

            if signal:

                trade, entry, sl, tp1, tp2, tp3 = signal

                chart = capture_chart(symbol)

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

                send_signal(msg, chart)

        except:
            pass

    time.sleep(300)
