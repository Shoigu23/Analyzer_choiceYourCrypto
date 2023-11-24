from binance.client import Client
import numpy as np

api_key = "sgkRXTuJHcZuBBudB5TaVjAn6K7ccrpO9FER1Hz8jsOoB0eAUolVWU0j6k4fknXt"
api_secret = "bwj1RC0RZ7KdI4QPZFJrVZRHcgomPuzDQaF13rqr4LPT35gYXJqQvLeBnBszYbR3"

client = Client(api_key, api_secret)

while True:
    symbol = input().upper()+'USDT'
    if symbol == 'EXIT':
        break
    interval = Client.KLINE_INTERVAL_1HOUR

    klines = client.get_historical_klines(symbol, interval, "1 day ago UTC")

    closing_prices = [float(kline[4]) for kline in klines]

    sma5 = np.convolve(closing_prices, np.ones(5) / 5, mode='valid')
    sma20 = np.convolve(closing_prices, np.ones(20) / 20, mode='valid')
    sma20_adjusted = np.pad(sma20, (len(sma5) - len(sma20), 0), 'constant')

    signal = np.where(sma5 > sma20_adjusted, 1, -1)

    # print("Closing prices: ", closing_prices[-10:])
    # print("SMA5: ", sma5[-10:])
    # print("SMA5: ", sma5[-10:])
    # print("SIGNAL: ", signal[-10:])

    if signal[-1] > signal[-2]:
        print("BUY")
    elif signal[-1] < signal[-2]:
        print("SELL")
    else:
        print("HOLD")