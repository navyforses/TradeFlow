# 📈 TradeFlow

**ალგორითმული ტრეიდინგის პლატფორმა | Algorithmic Trading Platform**

შექმნილია შაკო ჯინჭარაძის მიერ | Created by Shako Jincharadze

---

## 🇬🇪 ქართულად

TradeFlow არის Python-ზე დაფუძნებული ალგორითმული ტრეიდინგის ბიბლიოთეკა, რომელიც საშუალებას გაძლევთ:

- სავაჭრო სტრატეგიების შექმნა და ბეკტესტინგი
- ისტორიულ მონაცემებზე ალგორითმების შემოწმება
- რეალურ დროში სიმულაციის გაშვება
- პორტფელის მართვა და რისკების ანალიზი

### ინსტალაცია

```bash
pip install tradeflow
```

### სწრაფი დაწყება

```python
from tradeflow.api import order_target, record, symbol

def initialize(context):
    """ინიციალიზაცია - ალგორითმის საწყისი პარამეტრები"""
    context.asset = symbol('AAPL')

def handle_data(context, data):
    """მონაცემთა დამუშავება - ყოველ ბარზე გაეშვება"""
    order_target(context.asset, 10)
    record(AAPL=data.current(context.asset, 'price'))
```

### CLI ბრძანებები

```bash
# მონაცემების ჩატვირთვა
tradeflow ingest -b quandl

# ბეკტესტის გაშვება
tradeflow run -f my_strategy.py -s 2020-01-01 -e 2023-12-31

# მონაცემთა ბაზის გაწმენდა
tradeflow clean -b quandl --keep-last 3
```

---

## 🇬🇧 English

TradeFlow is a Python-based algorithmic trading library that enables:

- Creating and backtesting trading strategies
- Testing algorithms on historical data
- Running real-time simulations
- Portfolio management and risk analysis

### Installation

```bash
pip install tradeflow
```

### Quick Start

```python
from tradeflow.api import order_target, record, symbol

def initialize(context):
    """Initialization - set algorithm parameters"""
    context.asset = symbol('AAPL')

def handle_data(context, data):
    """Data handler - runs on every bar"""
    order_target(context.asset, 10)
    record(AAPL=data.current(context.asset, 'price'))
```

---

## 🏗️ პროექტის სტრუქტურა | Project Structure

```
tradeflow/
├── algorithm.py       # ძირითადი ალგორითმის კლასი | Core algorithm class
├── api.py             # სავაჭრო API | Trading API
├── assets/            # ფინანსური ინსტრუმენტები | Financial instruments
├── data/              # მონაცემთა დამუშავება | Data processing
│   └── bundles/       # მონაცემთა წყაროები | Data sources
├── finance/           # ფინანსური ლოგიკა | Financial logic
├── pipeline/          # მონაცემთა პაიპლაინი | Data pipeline
├── lib/               # ბიბლიოთეკის ბირთვი | Library core
├── utils/             # დამხმარე ფუნქციები | Utility functions
└── examples/          # მაგალითები | Examples
```

## 📋 მოთხოვნები | Requirements

- Python >= 3.8
- NumPy
- Pandas
- Cython

## 📄 ლიცენზია | License

Apache License 2.0

## 👤 ავტორი | Author

**შაკო ჯინჭარაძე | Shako Jincharadze**
- GitHub: [@navyforses](https://github.com/navyforses)
- Email: jincharadzeshako@gmail.com
