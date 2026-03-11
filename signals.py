import pandas as pd
import numpy as np

from config import EMA_FAST, EMA_SLOW, RSI_PERIOD, RSI_LONG_MAX, RSI_SHORT_MIN

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal(df):
    df["ema_fast"] = df["close"].ewm(span=EMA_FAST, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=EMA_SLOW, adjust=False).mean()
    df["rsi"] = calculate_rsi(df, RSI_PERIOD)
    
    last = df.iloc[-1]
    if last["ema_fast"] > last["ema_slow"] and last["rsi"] < RSI_LONG_MAX:
        entry = float(last["close"])
        sl = float(entry * 0.98)
        tp1 = float(entry * 1.02)
        tp2 = float(entry * 1.04)
        tp3 = float(entry * 1.06)
        return ("LONG", entry, sl, tp1, tp2, tp3)
    
    elif last["ema_fast"] < last["ema_slow"] and last["rsi"] > RSI_SHORT_MIN:
        entry = float(last["close"])
        sl = float(entry * 1.02)
        tp1 = float(entry * 0.98)
        tp2 = float(entry * 0.96)
        tp3 = float(entry * 0.94)
        return ("SHORT", entry, sl, tp1, tp2, tp3)
    
    return None
