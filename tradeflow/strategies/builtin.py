# TradeFlow - ჩაშენებული სტრატეგიები | Built-in Strategies
"""
მზა სავაჭრო სტრატეგიები TradeFlow-სთვის.
Ready-made trading strategies for TradeFlow.
"""
from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    სტრატეგიის ბაზისური კლასი | Base Strategy Class

    ყველა სტრატეგიამ უნდა მემკვიდრეობით მიიღოს ეს კლასი.
    All strategies must inherit from this class.
    """

    def __init__(self, name="BaseStrategy"):
        self.name = name
        self._params = {}

    @abstractmethod
    def initialize(self, context):
        """ინიციალიზაცია | Initialize the strategy"""
        pass

    @abstractmethod
    def handle_data(self, context, data):
        """მონაცემთა დამუშავება | Handle incoming data"""
        pass

    def before_trading_start(self, context, data):
        """ვაჭრობის დაწყებამდე | Before trading starts each day"""
        pass

    def analyze(self, context, perf):
        """ანალიზი ბეკტესტის შემდეგ | Post-backtest analysis"""
        pass

    def set_params(self, **kwargs):
        """პარამეტრების დაყენება | Set strategy parameters"""
        self._params.update(kwargs)
        return self

    def get_param(self, key, default=None):
        """პარამეტრის მიღება | Get a parameter value"""
        return self._params.get(key, default)


class MACrossoverStrategy(BaseStrategy):
    """
    მოძრავი საშუალოების გადაკვეთის სტრატეგია | Moving Average Crossover

    ყიდულობს, როცა სწრაფი MA ზემოდან კვეთს ნელ MA-ს.
    ყიდის, როცა სწრაფი MA ქვემოდან კვეთს ნელ MA-ს.
    """

    def __init__(self, fast_period=10, slow_period=30):
        super().__init__(name="MA Crossover")
        self._params = {
            'fast_period': fast_period,
            'slow_period': slow_period,
        }

    def initialize(self, context):
        context.fast_period = self._params['fast_period']
        context.slow_period = self._params['slow_period']
        context.invested = False

    def handle_data(self, context, data):
        # ეს არის შაბლონი - რეალური იმპლემენტაციისთვის
        # საჭიროა tradeflow.api-ს გამოყენება
        pass


class RSIMeanReversionStrategy(BaseStrategy):
    """
    RSI საშუალოზე დაბრუნების სტრატეგია | RSI Mean Reversion

    ყიდულობს, როცა RSI < oversold დონე (ნაგულისხმევი: 30)
    ყიდის, როცა RSI > overbought დონე (ნაგულისხმევი: 70)
    """

    def __init__(self, period=14, oversold=30, overbought=70):
        super().__init__(name="RSI Mean Reversion")
        self._params = {
            'period': period,
            'oversold': oversold,
            'overbought': overbought,
        }

    def initialize(self, context):
        context.rsi_period = self._params['period']
        context.oversold = self._params['oversold']
        context.overbought = self._params['overbought']

    def handle_data(self, context, data):
        pass


class MomentumStrategy(BaseStrategy):
    """
    მომენტუმის სტრატეგია | Momentum Strategy

    ყიდულობს აქტივებს, რომლებსაც ყველაზე მაღალი მომენტუმი აქვთ.
    Buys assets with the highest momentum.
    """

    def __init__(self, lookback=20, num_positions=5):
        super().__init__(name="Momentum")
        self._params = {
            'lookback': lookback,
            'num_positions': num_positions,
        }

    def initialize(self, context):
        context.lookback = self._params['lookback']
        context.num_positions = self._params['num_positions']

    def handle_data(self, context, data):
        pass


class BollingerBreakoutStrategy(BaseStrategy):
    """
    ბოლინჯერის გარღვევის სტრატეგია | Bollinger Breakout

    ყიდულობს, როცა ფასი ზედა ზოლს გასცდება.
    ყიდის, როცა ფასი ქვედა ზოლს ჩამოსცდება.
    """

    def __init__(self, period=20, std_dev=2):
        super().__init__(name="Bollinger Breakout")
        self._params = {
            'period': period,
            'std_dev': std_dev,
        }

    def initialize(self, context):
        context.bb_period = self._params['period']
        context.bb_std = self._params['std_dev']

    def handle_data(self, context, data):
        pass
