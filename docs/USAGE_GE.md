# TradeFlow — გამოყენების სრული სახელმძღვანელო

## სარჩევი

1. [ინსტალაცია](#ინსტალაცია)
2. [პირველი ნაბიჯები](#პირველი-ნაბიჯები)
3. [ალგორითმის სტრუქტურა](#ალგორითმის-სტრუქტურა)
4. [ინდიკატორები](#ინდიკატორები)
5. [მზა სტრატეგიები](#მზა-სტრატეგიები)
6. [მონაცემების ჩატვირთვა](#მონაცემების-ჩატვირთვა)
7. [Backtesting — ისტორიული ტესტირება](#backtesting)
8. [შედეგების ანალიზი](#შედეგების-ანალიზი)
9. [CLI ბრძანებები](#cli-ბრძანებები)
10. [პრაქტიკული მაგალითები](#პრაქტიკული-მაგალითები)

---

## ინსტალაცია

### pip-ით (რეკომენდებული)

```bash
pip install tradeflow
```

### GitHub-დან პირდაპირ

```bash
pip install git+https://github.com/navyforses/TradeFlow.git
```

### წყარო კოდიდან

```bash
git clone https://github.com/navyforses/TradeFlow.git
cd TradeFlow
pip install -e .
```

### დამოკიდებულებები

TradeFlow ავტომატურად დააყენებს საჭირო ბიბლიოთეკებს:

- `numpy` — მათემატიკური გამოთვლები
- `pandas` — მონაცემთა მანიპულაცია
- `matplotlib` — გრაფიკები და ვიზუალიზაცია
- `scipy` — სტატისტიკური ანალიზი

---

## პირველი ნაბიჯები

### მინიმალური მაგალითი

```python
from tradeflow import run_algorithm
from tradeflow.api import order, symbol, record

# ინიციალიზაცია — გაეშვება ერთხელ, დასაწყისში
def initialize(context):
    context.asset = symbol('AAPL')  # Apple-ის აქცია

# მონაცემთა დამუშავება — გაეშვება ყოველ სავაჭრო დღეს
def handle_data(context, data):
    # ვიყიდოთ 10 აქცია
    order(context.asset, 10)
    # ჩავწეროთ ფასი ანალიზისთვის
    record(AAPL=data.current(context.asset, 'price'))

# ალგორითმის გაშვება
results = run_algorithm(
    start='2020-01-01',
    end='2023-12-31',
    initialize=initialize,
    handle_data=handle_data,
    capital_base=100000  # საწყისი კაპიტალი $100,000
)

print(results.portfolio_value)
```

### რა მოხდა ამ კოდში?

1. `initialize()` — ერთხელ გაეშვა და AAPL სიმბოლო დაამახსოვრა
2. `handle_data()` — ყოველ სავაჭრო დღეს იყიდა 10 აქცია
3. `run_algorithm()` — 2020-2023 წლებში პროსიმულირდა ვაჭრობა $100K საწყისი თანხით
4. `results` — შედეგები შეინახა DataFrame-ში

---

## ალგორითმის სტრუქტურა

ყველა TradeFlow ალგორითმს აქვს ორი მთავარი ფუნქცია:

### initialize(context)

გაეშვება **ერთხელ**, ალგორითმის დასაწყისში. აქ ხდება:

- აქტივების განსაზღვრა
- პარამეტრების დაყენება
- ცვლადების ინიციალიზაცია

```python
def initialize(context):
    # რომელ აქციებს ვაჭრობთ
    context.asset = symbol('AAPL')

    # პარამეტრები
    context.lookback = 20        # რამდენ დღეს ვუყურებთ უკან
    context.max_position = 100   # მაქსიმუმ რამდენი აქცია
    context.stop_loss = 0.05     # 5% stop-loss

    # დაგეგმილი ფუნქცია — ყოველ დღე ბაზრის გახსნისას
    schedule_function(
        rebalance,
        date_rules.every_day(),
        time_rules.market_open(minutes=30)
    )
```

### handle_data(context, data)

გაეშვება **ყოველ სავაჭრო დღეს**. აქ ხდება:

- მონაცემების წაკითხვა
- სიგნალების გენერაცია
- ორდერების განთავსება

```python
def handle_data(context, data):
    # მიმდინარე ფასი
    price = data.current(context.asset, 'price')

    # ბოლო 20 დღის ფასების ისტორია
    price_history = data.history(context.asset, 'price', 20, '1d')

    # საშუალო ფასი
    average = price_history.mean()

    # სავაჭრო ლოგიკა
    if price < average * 0.95:
        # ფასი 5%-ით ქვემოთაა საშუალოზე — ვყიდულობთ
        order(context.asset, 10)
    elif price > average * 1.05:
        # ფასი 5%-ით ზემოთაა — ვყიდით
        order(context.asset, -10)
```

### context ობიექტი

`context` არის საერთო მეხსიერება, რომელიც ინახავს მონაცემებს ფუნქციებს შორის:

```python
context.asset          # აქტივი
context.portfolio      # პორტფოლიო
context.portfolio.cash # ნაღდი ფული
context.portfolio.positions  # ღია პოზიციები
context.account.leverage     # ბერკეტი
```

### data ობიექტი

`data` გაძლევს ბაზრის მონაცემებზე წვდომას:

```python
# მიმდინარე ფასი
data.current(asset, 'price')
data.current(asset, 'volume')

# ისტორიული მონაცემები
data.history(asset, 'price', 30, '1d')    # ბოლო 30 დღე
data.history(asset, 'volume', 10, '1d')   # ბოლო 10 დღის მოცულობა

# შესაძლებელია თუ არა ვაჭრობა
data.can_trade(asset)
```

---

## ინდიკატორები

TradeFlow-ს აქვს 10+ ჩაშენებული ტექნიკური ინდიკატორი:

### RSI (Relative Strength Index)

ზომავს აქტივის გადაჭარბებულ ყიდვას ან გაყიდვას. 0-100 სკალა.

- RSI > 70 — გადაჭარბებული ყიდვა (overbought), შესაძლოა დაეცეს
- RSI < 30 — გადაჭარბებული გაყიდვა (oversold), შესაძლოა აიწიოს

```python
from tradeflow.indicators import RSI

prices = data.history(context.asset, 'price', 50, '1d')
rsi = RSI(prices, period=14)

if rsi[-1] < 30:
    order(context.asset, 10)   # oversold — ვყიდულობთ
elif rsi[-1] > 70:
    order(context.asset, -10)  # overbought — ვყიდით
```

### MACD (Moving Average Convergence Divergence)

ტრენდის მიმართულებისა და ძალის ინდიკატორი.

```python
from tradeflow.indicators import MACD

prices = data.history(context.asset, 'price', 50, '1d')
macd_line, signal_line = MACD(prices, fast=12, slow=26, signal=9)

# MACD ხაზი signal-ს ზემოდან კვეთს — ყიდვის სიგნალი
if macd_line[-1] > signal_line[-1] and macd_line[-2] < signal_line[-2]:
    order(context.asset, 20)
# MACD ხაზი signal-ს ქვემოდან კვეთს — გაყიდვის სიგნალი
elif macd_line[-1] < signal_line[-1] and macd_line[-2] > signal_line[-2]:
    order(context.asset, -20)
```

### Bollinger Bands

ფასის ზედა და ქვედა საზღვრები სტანდარტული გადახრის მიხედვით.

```python
from tradeflow.indicators import BollingerBands

prices = data.history(context.asset, 'price', 30, '1d')
upper, middle, lower = BollingerBands(prices, period=20, std_dev=2)

current_price = prices[-1]

if current_price < lower[-1]:
    order(context.asset, 10)   # ფასი ქვედა ზღვარს ქვემოთ — ყიდვა
elif current_price > upper[-1]:
    order(context.asset, -10)  # ფასი ზედა ზღვარს ზემოთ — გაყიდვა
```

### SMA (Simple Moving Average)

მარტივი მოძრავი საშუალო.

```python
from tradeflow.indicators import SMA

prices = data.history(context.asset, 'price', 200, '1d')
sma_50 = SMA(prices, period=50)
sma_200 = SMA(prices, period=200)

# Golden Cross — 50-დღიანი საშუალო 200-დღიანს ზემოდან კვეთს
if sma_50[-1] > sma_200[-1] and sma_50[-2] < sma_200[-2]:
    order_target_percent(context.asset, 1.0)  # მთელი კაპიტალი
```

### EMA (Exponential Moving Average)

ექსპონენციალური მოძრავი საშუალო — უფრო მეტ წონას აძლევს ბოლო ფასებს.

```python
from tradeflow.indicators import EMA

prices = data.history(context.asset, 'price', 50, '1d')
ema_12 = EMA(prices, period=12)
ema_26 = EMA(prices, period=26)
```

### VWAP (Volume Weighted Average Price)

მოცულობით შეწონილი საშუალო ფასი.

```python
from tradeflow.indicators import VWAP

prices = data.history(context.asset, 'price', 30, '1d')
volumes = data.history(context.asset, 'volume', 30, '1d')
vwap = VWAP(prices, volumes)
```

### ATR (Average True Range)

ცვალებადობის (volatility) ინდიკატორი.

```python
from tradeflow.indicators import ATR

high = data.history(context.asset, 'high', 20, '1d')
low = data.history(context.asset, 'low', 20, '1d')
close = data.history(context.asset, 'close', 20, '1d')
atr = ATR(high, low, close, period=14)
```

### Stochastic Oscillator

```python
from tradeflow.indicators import StochasticOscillator

high = data.history(context.asset, 'high', 20, '1d')
low = data.history(context.asset, 'low', 20, '1d')
close = data.history(context.asset, 'close', 20, '1d')
k_line, d_line = StochasticOscillator(high, low, close, k_period=14, d_period=3)
```

---

## მზა სტრატეგიები

### Mean Reversion (საშუალოსკენ დაბრუნება)

იდეა: ფასი საშუალოდან რომ გადაიხრება, საბოლოოდ უკან ბრუნდება.

```python
from tradeflow.strategies import MeanReversion

def initialize(context):
    context.asset = symbol('AAPL')
    context.strategy = MeanReversion(
        lookback=20,      # 20 დღე უკან ვუყურებთ
        threshold=1.5,    # 1.5 სტანდარტული გადახრა
        position_size=100 # 100 აქცია
    )

def handle_data(context, data):
    prices = data.history(context.asset, 'price', 30, '1d')
    signal = context.strategy.generate_signal(prices)

    if signal == 'BUY':
        order(context.asset, context.strategy.position_size)
    elif signal == 'SELL':
        order(context.asset, -context.strategy.position_size)
```

### Momentum (იმპულსი)

იდეა: რომელი აქტივიც ბოლო პერიოდში მატულობდა, გააგრძელებს ზრდას.

```python
from tradeflow.strategies import MomentumStrategy

def initialize(context):
    context.asset = symbol('AAPL')
    context.strategy = MomentumStrategy(
        fast=10,   # სწრაფი პერიოდი
        slow=30    # ნელი პერიოდი
    )

def handle_data(context, data):
    prices = data.history(context.asset, 'price', 50, '1d')
    signal = context.strategy.generate_signal(prices)

    if signal == 'BUY':
        order_target_percent(context.asset, 0.9)  # კაპიტალის 90%
    elif signal == 'SELL':
        order_target_percent(context.asset, 0.0)  # გავყიდოთ ყველა
```

### Pairs Trading (წყვილური ვაჭრობა)

იდეა: ორი კორელირებული აქტივის ფასთა სხვაობით ვაჭრობა.

```python
from tradeflow.strategies import PairsTrading

def initialize(context):
    context.stock_a = symbol('KO')    # Coca-Cola
    context.stock_b = symbol('PEP')   # PepsiCo
    context.strategy = PairsTrading(
        lookback=30,
        entry_threshold=2.0,
        exit_threshold=0.5
    )

def handle_data(context, data):
    prices_a = data.history(context.stock_a, 'price', 30, '1d')
    prices_b = data.history(context.stock_b, 'price', 30, '1d')

    signal = context.strategy.generate_signal(prices_a, prices_b)

    if signal == 'LONG_A_SHORT_B':
        order_target_percent(context.stock_a, 0.5)
        order_target_percent(context.stock_b, -0.5)
    elif signal == 'LONG_B_SHORT_A':
        order_target_percent(context.stock_a, -0.5)
        order_target_percent(context.stock_b, 0.5)
```

### Breakout (გარღვევა)

იდეა: ფასი რომ გარკვეულ დონეს გაარღვევს, ძლიერი მოძრაობა მოჰყვება.

```python
from tradeflow.strategies import BreakoutStrategy

def initialize(context):
    context.asset = symbol('AAPL')
    context.strategy = BreakoutStrategy(
        lookback=20,         # 20 დღის მაქსიმუმ/მინიმუმ
        volume_factor=1.5    # მოცულობა 1.5x საშუალოზე მეტი
    )
```

---

## მონაცემების ჩატვირთვა

### Quandl-დან (უფასო)

```bash
# API გასაღების დაყენება
export QUANDL_API_KEY=your_api_key_here

# მონაცემების ჩამოტვირთვა
tradeflow ingest quandl
```

### CSV ფაილიდან

```python
import pandas as pd

# CSV ფაილის წაკითხვა
data = pd.read_csv('my_data.csv', parse_dates=['date'], index_col='date')

# საჭირო სვეტები: open, high, low, close, volume
```

### Yahoo Finance-დან

```bash
pip install yfinance
```

```python
import yfinance as yf

# მონაცემების ჩამოტვირთვა
aapl = yf.download('AAPL', start='2020-01-01', end='2023-12-31')
```

---

## Backtesting

### სრული Backtest მაგალითი

```python
from tradeflow import run_algorithm
from tradeflow.api import order, symbol, record, order_target_percent
from tradeflow.indicators import RSI, SMA

def initialize(context):
    context.asset = symbol('AAPL')
    context.lookback = 14

def handle_data(context, data):
    prices = data.history(context.asset, 'price', 50, '1d')

    rsi = RSI(prices, period=context.lookback)
    sma = SMA(prices, period=20)
    current_price = prices[-1]

    # კომბინირებული სიგნალი: RSI + SMA
    if rsi[-1] < 30 and current_price > sma[-1]:
        order_target_percent(context.asset, 0.9)
        record(signal='BUY')
    elif rsi[-1] > 70 and current_price < sma[-1]:
        order_target_percent(context.asset, 0.0)
        record(signal='SELL')

    record(
        price=current_price,
        rsi=rsi[-1],
        sma=sma[-1],
        portfolio=context.portfolio.portfolio_value
    )

results = run_algorithm(
    start='2020-01-01',
    end='2023-12-31',
    initialize=initialize,
    handle_data=handle_data,
    capital_base=100000
)
```

### შედეგების მიღება

```python
# პორტფოლიოს ღირებულება დროში
print(results.portfolio_value)

# საბოლოო ღირებულება
print(f"საწყისი: $100,000")
print(f"საბოლოო: ${results.portfolio_value[-1]:,.2f}")
print(f"მოგება: {((results.portfolio_value[-1] / 100000) - 1) * 100:.2f}%")
```

---

## შედეგების ანალიზი

### გრაფიკის აგება

```python
import matplotlib.pyplot as plt

# პორტფოლიოს ღირებულების გრაფიკი
fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# 1. პორტფოლიოს ღირებულება
axes[0].plot(results.portfolio_value, color='#00d4aa', linewidth=1.5)
axes[0].set_title('პორტფოლიოს ღირებულება')
axes[0].set_ylabel('USD')
axes[0].grid(True, alpha=0.3)

# 2. ფასი და SMA
axes[1].plot(results.price, label='ფასი', color='white', linewidth=1)
axes[1].plot(results.sma, label='SMA 20', color='#3b82f6', linewidth=1)
axes[1].set_title('AAPL ფასი')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# 3. RSI
axes[2].plot(results.rsi, color='#f59e0b', linewidth=1)
axes[2].axhline(y=70, color='red', linestyle='--', alpha=0.5)
axes[2].axhline(y=30, color='green', linestyle='--', alpha=0.5)
axes[2].set_title('RSI')
axes[2].set_ylabel('RSI')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('backtest_results.png', dpi=150)
plt.show()
```

### მეტრიკები

```python
import numpy as np

portfolio = results.portfolio_value
returns = portfolio.pct_change().dropna()

# ძირითადი მეტრიკები
total_return = (portfolio[-1] / portfolio[0]) - 1
annual_return = (1 + total_return) ** (252 / len(returns)) - 1
sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
max_drawdown = ((portfolio / portfolio.cummax()) - 1).min()

print(f"სრული მოგება: {total_return * 100:.2f}%")
print(f"წლიური მოგება: {annual_return * 100:.2f}%")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"მაქსიმალური ვარდნა: {max_drawdown * 100:.2f}%")
```

---

## CLI ბრძანებები

```bash
# ალგორითმის გაშვება
tradeflow run my_strategy.py --start 2020-01-01 --end 2023-12-31

# მონაცემების ჩატვირთვა
tradeflow ingest quandl

# მონაცემების სია
tradeflow bundles

# დახმარება
tradeflow --help

# ქართულ ენაზე
tradeflow --lang ka
```

---

## პრაქტიკული მაგალითები

### მაგალითი 1: Golden Cross სტრატეგია

50-დღიანი SMA რომ 200-დღიანს ზემოდან გადაკვეთს — ყიდვა. ქვემოდან — გაყიდვა.

```python
from tradeflow import run_algorithm
from tradeflow.api import order_target_percent, symbol, record
from tradeflow.indicators import SMA

def initialize(context):
    context.asset = symbol('AAPL')

def handle_data(context, data):
    prices = data.history(context.asset, 'price', 210, '1d')

    if len(prices) < 200:
        return

    sma_50 = SMA(prices, 50)
    sma_200 = SMA(prices, 200)

    # Golden Cross
    if sma_50[-1] > sma_200[-1] and sma_50[-2] <= sma_200[-2]:
        order_target_percent(context.asset, 1.0)
        record(signal=1)
    # Death Cross
    elif sma_50[-1] < sma_200[-1] and sma_50[-2] >= sma_200[-2]:
        order_target_percent(context.asset, 0.0)
        record(signal=-1)
    else:
        record(signal=0)

results = run_algorithm(
    start='2018-01-01',
    end='2023-12-31',
    initialize=initialize,
    handle_data=handle_data,
    capital_base=50000
)
```

### მაგალითი 2: მრავალი აქტივის პორტფოლიო

```python
from tradeflow import run_algorithm
from tradeflow.api import order_target_percent, symbol, record
from tradeflow.indicators import RSI

def initialize(context):
    context.assets = [
        symbol('AAPL'),
        symbol('GOOGL'),
        symbol('MSFT'),
        symbol('AMZN'),
        symbol('TSLA')
    ]
    context.weight = 1.0 / len(context.assets)  # თანაბარი წონა

def handle_data(context, data):
    for asset in context.assets:
        if not data.can_trade(asset):
            continue

        prices = data.history(asset, 'price', 20, '1d')
        rsi = RSI(prices, period=14)

        if rsi[-1] < 30:
            # oversold — ვყიდულობთ წონის მიხედვით
            order_target_percent(asset, context.weight)
        elif rsi[-1] > 70:
            # overbought — ვყიდით
            order_target_percent(asset, 0.0)

results = run_algorithm(
    start='2020-01-01',
    end='2023-12-31',
    initialize=initialize,
    handle_data=handle_data,
    capital_base=100000
)
```

### მაგალითი 3: Stop-Loss და Take-Profit

```python
from tradeflow import run_algorithm
from tradeflow.api import order, order_target_percent, symbol, get_open_orders

def initialize(context):
    context.asset = symbol('AAPL')
    context.bought_price = None
    context.stop_loss = 0.05      # 5% stop-loss
    context.take_profit = 0.10    # 10% take-profit

def handle_data(context, data):
    current_price = data.current(context.asset, 'price')
    position = context.portfolio.positions.get(context.asset)

    if position and position.amount > 0:
        # გვაქვს პოზიცია — ვამოწმებთ stop-loss/take-profit
        entry_price = position.cost_basis
        pnl_pct = (current_price - entry_price) / entry_price

        if pnl_pct <= -context.stop_loss:
            # Stop-Loss: ზარალი 5%-ს მიაღწია
            order_target_percent(context.asset, 0.0)
            context.bought_price = None
        elif pnl_pct >= context.take_profit:
            # Take-Profit: მოგება 10%-ს მიაღწია
            order_target_percent(context.asset, 0.0)
            context.bought_price = None
    else:
        # არ გვაქვს პოზიცია — ვეძებთ შესვლის წერტილს
        prices = data.history(context.asset, 'price', 20, '1d')
        if current_price < prices.mean() * 0.97:
            order_target_percent(context.asset, 0.9)
            context.bought_price = current_price
```

---

## ხშირი კითხვები

**Q: რეალურ ფულს ხომ არ კარგავ?**
A: არა. TradeFlow არის backtesting პლატფორმა — ისტორიულ მონაცემებზე ტესტავს სტრატეგიებს. რეალური ვაჭრობა არ ხდება.

**Q: რა მონაცემები მჭირდება?**
A: OHLCV (Open, High, Low, Close, Volume) ფორმატის მონაცემები. შეგიძლია Yahoo Finance, Quandl ან CSV-დან ჩატვირთო.

**Q: რამდენი აქტივი შემიძლია ერთდროულად?**
A: შეზღუდვა არ არის. 1-დან 1000-მდე აქტივს ერთდროულად გატესტავ.

**Q: როგორ ვაკეთებ ოპტიმიზაციას?**
A: პარამეტრები შეცვალე (lookback, threshold, period) და შეადარე Sharpe Ratio და მაქსიმალური ვარდნა.

---

## ავტორი

**Shako Jincharadze** (@navyforses)

- GitHub: [github.com/navyforses/TradeFlow](https://github.com/navyforses/TradeFlow)
- ვებსაიტი: [navyforses.github.io/TradeFlow](https://navyforses.github.io/TradeFlow)

---

*TradeFlow — ალგორითმული ვაჭრობის ქართული პლატფორმა*
