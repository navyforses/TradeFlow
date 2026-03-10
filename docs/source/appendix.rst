API Reference
-------------

Running a Backtest
~~~~~~~~~~~~~~~~~~

.. autofunction:: tradeflow.run_algorithm(...)

Algorithm API
~~~~~~~~~~~~~

The following methods are available for use in the ``initialize``,
``handle_data``, and ``before_trading_start`` API functions.

In all listed functions, the ``self`` argument is implicitly the
currently-executing :class:`~tradeflow.algorithm.TradingAlgorithm` instance.

Data Object
```````````

.. autoclass:: tradeflow.protocol.BarData
   :members:

Scheduling Functions
````````````````````

.. autofunction:: tradeflow.api.schedule_function

.. autoclass:: tradeflow.api.date_rules
   :members:
   :undoc-members:

.. autoclass:: tradeflow.api.time_rules
   :members:

Orders
``````

.. autofunction:: tradeflow.api.order

.. autofunction:: tradeflow.api.order_value

.. autofunction:: tradeflow.api.order_percent

.. autofunction:: tradeflow.api.order_target

.. autofunction:: tradeflow.api.order_target_value

.. autofunction:: tradeflow.api.order_target_percent

.. autoclass:: tradeflow.finance.execution.ExecutionStyle
   :members:

.. autoclass:: tradeflow.finance.execution.MarketOrder

.. autoclass:: tradeflow.finance.execution.LimitOrder

.. autoclass:: tradeflow.finance.execution.StopOrder

.. autoclass:: tradeflow.finance.execution.StopLimitOrder

.. autofunction:: tradeflow.api.get_order

.. autofunction:: tradeflow.api.get_open_orders

.. autofunction:: tradeflow.api.cancel_order

Order Cancellation Policies
'''''''''''''''''''''''''''

.. autofunction:: tradeflow.api.set_cancel_policy

.. autoclass:: tradeflow.finance.cancel_policy.CancelPolicy
   :members:

.. autofunction:: tradeflow.api.EODCancel

.. autofunction:: tradeflow.api.NeverCancel


Assets
``````

.. autofunction:: tradeflow.api.symbol

.. autofunction:: tradeflow.api.symbols

.. autofunction:: tradeflow.api.future_symbol

.. autofunction:: tradeflow.api.set_symbol_lookup_date

.. autofunction:: tradeflow.api.sid


Trading Controls
````````````````

Zipline provides trading controls to help ensure that the algorithm is
performing as expected. The functions help protect the algorithm from certian
bugs that could cause undesirable behavior when trading with real money.

.. autofunction:: tradeflow.api.set_do_not_order_list

.. autofunction:: tradeflow.api.set_long_only

.. autofunction:: tradeflow.api.set_max_leverage

.. autofunction:: tradeflow.api.set_max_order_count

.. autofunction:: tradeflow.api.set_max_order_size

.. autofunction:: tradeflow.api.set_max_position_size


Simulation Parameters
`````````````````````

.. autofunction:: tradeflow.api.set_benchmark

Commission Models
'''''''''''''''''

.. autofunction:: tradeflow.api.set_commission

.. autoclass:: tradeflow.finance.commission.CommissionModel
   :members:

.. autoclass:: tradeflow.finance.commission.PerShare

.. autoclass:: tradeflow.finance.commission.PerTrade

.. autoclass:: tradeflow.finance.commission.PerDollar

Slippage Models
'''''''''''''''

.. autofunction:: tradeflow.api.set_slippage

.. autoclass:: tradeflow.finance.slippage.SlippageModel
   :members:

.. autoclass:: tradeflow.finance.slippage.FixedSlippage

.. autoclass:: tradeflow.finance.slippage.VolumeShareSlippage

Pipeline
````````

For more information, see :ref:`pipeline-api`

.. autofunction:: tradeflow.api.attach_pipeline

.. autofunction:: tradeflow.api.pipeline_output


Miscellaneous
`````````````

.. autofunction:: tradeflow.api.record

.. autofunction:: tradeflow.api.get_environment

.. autofunction:: tradeflow.api.fetch_csv

Blotters
~~~~~~~~

.. autoclass:: tradeflow.finance.blotter.blotter.Blotter
   :members:

.. autoclass:: tradeflow.finance.blotter.SimulationBlotter
   :members:

.. _pipeline-api:

Pipeline API
~~~~~~~~~~~~

.. autoclass:: tradeflow.pipeline.Pipeline
   :members:
   :member-order: groupwise

.. autoclass:: tradeflow.pipeline.CustomFactor
   :members:
   :member-order: groupwise

.. autoclass:: tradeflow.pipeline.Filter
   :members: __and__, __or__, if_else
   :exclude-members: dtype

.. autoclass:: tradeflow.pipeline.Factor
   :members: bottom, deciles, demean, linear_regression, pearsonr,
             percentile_between, quantiles, quartiles, quintiles, rank,
             spearmanr, top, winsorize, zscore, isnan, notnan, isfinite, eq,
             __add__, __sub__, __mul__, __div__, __mod__, __pow__, __lt__,
             __le__, __ne__, __ge__, __gt__, clip, fillna, mean, stddev, max,
             min, median, sum, clip
   :exclude-members: dtype
   :member-order: bysource

.. autoclass:: tradeflow.pipeline.Term
   :members:
   :exclude-members: compute_extra_rows, dependencies, inputs, mask, windowed

.. autoclass:: tradeflow.pipeline.data.DataSet
   :members:

.. autoclass:: tradeflow.pipeline.data.Column
   :members:

.. autoclass:: tradeflow.pipeline.data.BoundColumn
   :members:

.. autoclass:: tradeflow.pipeline.data.DataSetFamily
   :members:

.. autoclass:: tradeflow.pipeline.data.EquityPricing
   :members: open, high, low, close, volume
   :undoc-members:

Built-in Factors
````````````````

.. autoclass:: tradeflow.pipeline.factors.AverageDollarVolume
   :members:

.. autoclass:: tradeflow.pipeline.factors.BollingerBands
   :members:

.. autoclass:: tradeflow.pipeline.factors.BusinessDaysSincePreviousEvent
   :members:

.. autoclass:: tradeflow.pipeline.factors.BusinessDaysUntilNextEvent
   :members:

.. autoclass:: tradeflow.pipeline.factors.DailyReturns
   :members:

.. autoclass:: tradeflow.pipeline.factors.ExponentialWeightedMovingAverage
   :members:

.. autoclass:: tradeflow.pipeline.factors.ExponentialWeightedMovingStdDev
   :members:

.. autoclass:: tradeflow.pipeline.factors.Latest
   :members:

.. autoclass:: tradeflow.pipeline.factors.MACDSignal
   :members:

.. autoclass:: tradeflow.pipeline.factors.MaxDrawdown
   :members:

.. autoclass:: tradeflow.pipeline.factors.Returns
   :members:

.. autoclass:: tradeflow.pipeline.factors.RollingPearson
   :members:

.. autoclass:: tradeflow.pipeline.factors.RollingSpearman
   :members:

.. autoclass:: tradeflow.pipeline.factors.RollingLinearRegressionOfReturns
   :members:

.. autoclass:: tradeflow.pipeline.factors.RollingPearsonOfReturns
   :members:

.. autoclass:: tradeflow.pipeline.factors.RollingSpearmanOfReturns
   :members:

.. autoclass:: tradeflow.pipeline.factors.SimpleBeta
   :members:

.. autoclass:: tradeflow.pipeline.factors.RSI
   :members:

.. autoclass:: tradeflow.pipeline.factors.SimpleMovingAverage
   :members:

.. autoclass:: tradeflow.pipeline.factors.VWAP
   :members:

.. autoclass:: tradeflow.pipeline.factors.WeightedAverageValue
   :members:

.. autoclass:: tradeflow.pipeline.factors.PercentChange
   :members:

.. autoclass:: tradeflow.pipeline.factors.PeerCount
   :members:


Built-in Filters
````````````````

.. autoclass:: tradeflow.pipeline.filters.All
   :members:

.. autoclass:: tradeflow.pipeline.filters.AllPresent
   :members:

.. autoclass:: tradeflow.pipeline.filters.Any
   :members:

.. autoclass:: tradeflow.pipeline.filters.AtLeastN
   :members:

.. autoclass:: tradeflow.pipeline.filters.SingleAsset
   :members:

.. autoclass:: tradeflow.pipeline.filters.StaticAssets
   :members:

.. autoclass:: tradeflow.pipeline.filters.StaticSids
   :members:

Pipeline Engine
```````````````

.. autoclass:: tradeflow.pipeline.engine.PipelineEngine
   :members: run_pipeline, run_chunked_pipeline
   :member-order: bysource

.. autoclass:: tradeflow.pipeline.engine.SimplePipelineEngine
   :members: __init__, run_pipeline, run_chunked_pipeline
   :member-order: bysource

.. autofunction:: tradeflow.pipeline.engine.default_populate_initial_workspace

Data Loaders
````````````

.. autoclass:: tradeflow.pipeline.loaders.equity_pricing_loader.USEquityPricingLoader
   :members: __init__, from_files, load_adjusted_array
   :member-order: bysource

Asset Metadata
~~~~~~~~~~~~~~

.. autoclass:: tradeflow.assets.Asset
   :members:

.. autoclass:: tradeflow.assets.Equity
   :members:

.. autoclass:: tradeflow.assets.Future
   :members:

.. autoclass:: tradeflow.assets.AssetConvertible
   :members:


Trading Calendar API
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: tradeflow.utils.calendars.get_calendar

.. autoclass:: tradeflow.utils.calendars.TradingCalendar
   :members:

.. autofunction:: tradeflow.utils.calendars.register_calendar

.. autofunction:: tradeflow.utils.calendars.register_calendar_type

.. autofunction:: tradeflow.utils.calendars.deregister_calendar

.. autofunction:: tradeflow.utils.calendars.clear_calendars


Data API
~~~~~~~~

Writers
```````
.. autoclass:: tradeflow.data.minute_bars.BcolzMinuteBarWriter
   :members:

.. autoclass:: tradeflow.data.bcolz_daily_bars.BcolzDailyBarWriter
   :members:

.. autoclass:: tradeflow.data.adjustments.SQLiteAdjustmentWriter
   :members:

.. autoclass:: tradeflow.assets.AssetDBWriter
   :members:

Readers
```````
.. autoclass:: tradeflow.data.minute_bars.BcolzMinuteBarReader
   :members:

.. autoclass:: tradeflow.data.bcolz_daily_bars.BcolzDailyBarReader
   :members:

.. autoclass:: tradeflow.data.adjustments.SQLiteAdjustmentReader
   :members:

.. autoclass:: tradeflow.assets.AssetFinder
   :members:

.. autoclass:: tradeflow.data.data_portal.DataPortal
   :members:

.. autoclass:: tradeflow.sources.benchmark_source.BenchmarkSource
   :members:

Bundles
```````
.. autofunction:: tradeflow.data.bundles.register

.. autofunction:: tradeflow.data.bundles.ingest(name, environ=os.environ, date=None, show_progress=True)

.. autofunction:: tradeflow.data.bundles.load(name, environ=os.environ, date=None)

.. autofunction:: tradeflow.data.bundles.unregister

.. data:: tradeflow.data.bundles.bundles

   The bundles that have been registered as a mapping from bundle name to bundle
   data. This mapping is immutable and may only be updated through
   :func:`~tradeflow.data.bundles.register` or
   :func:`~tradeflow.data.bundles.unregister`.


Risk Metrics
~~~~~~~~~~~~

Algorithm State
```````````````

.. autoclass:: tradeflow.finance.ledger.Ledger
   :members:

.. autoclass:: tradeflow.protocol.Portfolio
   :members:

.. autoclass:: tradeflow.protocol.Account
   :members:

.. autoclass:: tradeflow.finance.ledger.PositionTracker
   :members:

.. autoclass:: tradeflow.finance._finance_ext.PositionStats

Built-in Metrics
````````````````

.. autoclass:: tradeflow.finance.metrics.metric.SimpleLedgerField

.. autoclass:: tradeflow.finance.metrics.metric.DailyLedgerField

.. autoclass:: tradeflow.finance.metrics.metric.StartOfPeriodLedgerField

.. autoclass:: tradeflow.finance.metrics.metric.StartOfPeriodLedgerField

.. autoclass:: tradeflow.finance.metrics.metric.Returns

.. autoclass:: tradeflow.finance.metrics.metric.BenchmarkReturnsAndVolatility

.. autoclass:: tradeflow.finance.metrics.metric.CashFlow

.. autoclass:: tradeflow.finance.metrics.metric.Orders

.. autoclass:: tradeflow.finance.metrics.metric.Transactions

.. autoclass:: tradeflow.finance.metrics.metric.Positions

.. autoclass:: tradeflow.finance.metrics.metric.ReturnsStatistic

.. autoclass:: tradeflow.finance.metrics.metric.AlphaBeta

.. autoclass:: tradeflow.finance.metrics.metric.MaxLeverage

Metrics Sets
````````````

.. autofunction:: tradeflow.finance.metrics.register

.. autofunction:: tradeflow.finance.metrics.load

.. autofunction:: tradeflow.finance.metrics.unregister

.. data:: tradeflow.data.finance.metrics.metrics_sets

   The metrics sets that have been registered as a mapping from metrics set name
   to load function. This mapping is immutable and may only be updated through
   :func:`~tradeflow.finance.metrics.register` or
   :func:`~tradeflow.finance.metrics.unregister`.


Utilities
~~~~~~~~~

Caching
```````

.. autoclass:: tradeflow.utils.cache.CachedObject

.. autoclass:: tradeflow.utils.cache.ExpiringCache

.. autoclass:: tradeflow.utils.cache.dataframe_cache

.. autoclass:: tradeflow.utils.cache.working_file

.. autoclass:: tradeflow.utils.cache.working_dir

Command Line
````````````
.. autofunction:: tradeflow.utils.cli.maybe_show_progress
