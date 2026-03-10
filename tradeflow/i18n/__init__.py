# TradeFlow - ლოკალიზაციის სისტემა | Localization System

_CURRENT_LANG = 'ka'

TRANSLATIONS = {
    'ka': {
        'starting_simulation': 'სიმულაციის დაწყება...',
        'simulation_complete': 'სიმულაცია დასრულდა',
        'loading_data': 'მონაცემების ჩატვირთვა...',
        'data_loaded': 'მონაცემები ჩაიტვირთა',
        'backtest_start': 'ბეკტესტის დაწყება',
        'backtest_end': 'ბეკტესტი დასრულდა',
        'order_placed': 'შეკვეთა განთავსდა',
        'order_filled': 'შეკვეთა შესრულდა',
        'order_cancelled': 'შეკვეთა გაუქმდა',
        'portfolio_value': 'პორტფელის ღირებულება',
        'total_return': 'მთლიანი მოგება/ზარალი',
        'sharpe_ratio': 'შარპის კოეფიციენტი',
        'max_drawdown': 'მაქსიმალური ვარდნა',
        'win_rate': 'მომგებიანი ტრეიდების პროცენტი',
        'total_trades': 'მთლიანი ტრეიდები',
        'error_no_data': 'მონაცემები ვერ მოიძებნა',
        'error_invalid_dates': 'თარიღები არასწორია',
        'error_no_strategy': 'სტრატეგია არ არის მითითებული',
        'ingest_start': 'მონაცემების იმპორტის დაწყება',
        'ingest_complete': 'მონაცემების იმპორტი დასრულდა',
        'bundle_not_found': 'მონაცემთა წყარო ვერ მოიძებნა',
        'strategy_registered': 'სტრატეგია დარეგისტრირდა',
    },
    'en': {
        'starting_simulation': 'Starting simulation...',
        'simulation_complete': 'Simulation complete',
        'loading_data': 'Loading data...',
        'data_loaded': 'Data loaded',
        'backtest_start': 'Starting backtest',
        'backtest_end': 'Backtest complete',
        'order_placed': 'Order placed',
        'order_filled': 'Order filled',
        'order_cancelled': 'Order cancelled',
        'portfolio_value': 'Portfolio value',
        'total_return': 'Total return',
        'sharpe_ratio': 'Sharpe ratio',
        'max_drawdown': 'Max drawdown',
        'win_rate': 'Win rate',
        'total_trades': 'Total trades',
        'error_no_data': 'No data found',
        'error_invalid_dates': 'Invalid dates',
        'error_no_strategy': 'No strategy specified',
        'ingest_start': 'Starting data ingest',
        'ingest_complete': 'Data ingest complete',
        'bundle_not_found': 'Data bundle not found',
        'strategy_registered': 'Strategy registered',
    }
}


def set_language(lang):
    """ენის დაყენება | Set language (ka/en)"""
    global _CURRENT_LANG
    if lang not in TRANSLATIONS:
        raise ValueError(f"Unsupported language: {lang}. Use 'ka' or 'en'")
    _CURRENT_LANG = lang


def get_language():
    """მიმდინარე ენის მიღება | Get current language"""
    return _CURRENT_LANG


def t(key):
    """თარგმნა | Translate a key to current language"""
    lang_dict = TRANSLATIONS.get(_CURRENT_LANG, TRANSLATIONS['en'])
    return lang_dict.get(key, key)


def tr(key, **kwargs):
    """თარგმნა ფორმატირებით | Translate with formatting"""
    text = t(key)
    if kwargs:
        return text.format(**kwargs)
    return text
