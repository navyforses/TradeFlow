# TradeFlow - ტექნიკური ინდიკატორების ბირთვი | Technical Indicators Core
"""
ტექნიკური ანალიზის ინდიკატორები pandas Series-ებისთვის.
Technical analysis indicators operating on pandas Series.
"""
import numpy as np
import pandas as pd


def sma(series, period=20):
    """
    მარტივი მოძრავი საშუალო | Simple Moving Average

    პარამეტრები:
        series: pandas Series - ფასების მწკრივი
        period: int - პერიოდი (ნაგულისხმევი: 20)

    აბრუნებს: pandas Series
    """
    return series.rolling(window=period).mean()


def ema(series, period=20):
    """
    ექსპონენციალური მოძრავი საშუალო | Exponential Moving Average

    პარამეტრები:
        series: pandas Series - ფასების მწკრივი
        period: int - პერიოდი (ნაგულისხმევი: 20)

    აბრუნებს: pandas Series
    """
    return series.ewm(span=period, adjust=False).mean()


def rsi(series, period=14):
    """
    ფარდობითი სიძლიერის ინდექსი | Relative Strength Index

    პარამეტრები:
        series: pandas Series - ფასების მწკრივი
        period: int - პერიოდი (ნაგულისხმევი: 14)

    აბრუნებს: pandas Series (0-100 დიაპაზონში)
    """
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(series, fast=12, slow=26, signal=9):
    """
    MACD ინდიკატორი | Moving Average Convergence Divergence

    პარამეტრები:
        series: pandas Series - ფასების მწკრივი
        fast: int - სწრაფი EMA პერიოდი (ნაგულისხმევი: 12)
        slow: int - ნელი EMA პერიოდი (ნაგულისხმევი: 26)
        signal: int - სიგნალის EMA პერიოდი (ნაგულისხმევი: 9)

    აბრუნებს: dict {'macd', 'signal', 'histogram'}
    """
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line

    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram,
    }


def bollinger_bands(series, period=20, std_dev=2):
    """
    ბოლინჯერის ზოლები | Bollinger Bands

    პარამეტრები:
        series: pandas Series - ფასების მწკრივი
        period: int - SMA პერიოდი (ნაგულისხმევი: 20)
        std_dev: float - სტანდარტული გადახრის მამრავლი

    აბრუნებს: dict {'upper', 'middle', 'lower'}
    """
    middle = sma(series, period)
    std = series.rolling(window=period).std()

    return {
        'upper': middle + (std * std_dev),
        'middle': middle,
        'lower': middle - (std * std_dev),
    }


def atr(high, low, close, period=14):
    """
    საშუალო ჭეშმარიტი დიაპაზონი | Average True Range

    პარამეტრები:
        high: pandas Series - მაქსიმალური ფასები
        low: pandas Series - მინიმალური ფასები
        close: pandas Series - დახურვის ფასები
        period: int - პერიოდი (ნაგულისხმევი: 14)

    აბრუნებს: pandas Series
    """
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return true_range.rolling(window=period).mean()


def vwap(high, low, close, volume):
    """
    მოცულობით შეწონილი საშუალო ფასი | Volume-Weighted Average Price

    პარამეტრები:
        high, low, close: pandas Series - ფასები
        volume: pandas Series - მოცულობა

    აბრუნებს: pandas Series
    """
    typical_price = (high + low + close) / 3
    cum_tp_vol = (typical_price * volume).cumsum()
    cum_vol = volume.cumsum()
    return cum_tp_vol / cum_vol


def momentum(series, period=10):
    """
    მომენტუმი | Momentum

    პარამეტრები:
        series: pandas Series - ფასების მწკრივი
        period: int - პერიოდი (ნაგულისხმევი: 10)

    აბრუნებს: pandas Series
    """
    return series - series.shift(period)


def stochastic(high, low, close, k_period=14, d_period=3):
    """
    სტოქასტიკური ოსცილატორი | Stochastic Oscillator

    პარამეტრები:
        high: pandas Series - მაქსიმალური ფასები
        low: pandas Series - მინიმალური ფასები
        close: pandas Series - დახურვის ფასები
        k_period: int - %K პერიოდი (ნაგულისხმევი: 14)
        d_period: int - %D პერიოდი (ნაგულისხმევი: 3)

    აბრუნებს: dict {'k', 'd'}
    """
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()

    return {'k': k, 'd': d}
