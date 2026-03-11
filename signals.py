import pandas as pd
import numpy as np
from config import EMA_FAST, EMA_SLOW, RSI_PERIOD


def rsi(series, period):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100/(1+rs))


def generate_signal(df):

    df["ema_fast"] = df["close"].ewm(span=EMA_FAST).mean()
    df["ema_slow"] = df["close"].ewm(span=EMA_SLOW).mean()
    df["rsi"] = rsi(df["close"], RSI_PERIOD)

    last = df.iloc[-1]

    price = last["close"]

    if last["ema_fast"] > last["ema_slow"] and last["rsi"] < 60:

        entry = price
        sl = price * 0.98

        tp1 = price * 1.02
        tp2 = price * 1.04
        tp3 = price * 1.07

        return "LONG", entry, sl, tp1, tp2, tp3

    if last["ema_fast"] < last["ema_slow"] and last["rsi"] > 40:

        entry = price
        sl = price * 1.02

        tp1 = price * 0.98
        tp2 = price * 0.96
        tp3 = price * 0.93

        return "SHORT", entry, sl, tp1, tp2, tp3

    return None
