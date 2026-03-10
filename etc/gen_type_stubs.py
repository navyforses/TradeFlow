import inspect
from operator import attrgetter
from textwrap import dedent

from tradeflow import api, TradingAlgorithm


def main():
    with open(api.__file__.rstrip('c') + 'i', 'w') as stub:
        # Imports so that Asset et al can be resolved.
        # "from MOD import *" will re-export the imports from the stub, so
        # explicitly importing.
        stub.write(dedent("""\
        import collections
        from tradeflow.assets import Asset, Equity, Future
        from tradeflow.assets.futures import FutureChain
        from tradeflow.finance.asset_restrictions import Restrictions
        from tradeflow.finance.cancel_policy import CancelPolicy
        from tradeflow.pipeline import Pipeline
        from tradeflow.protocol import Order
        from tradeflow.utils.events import EventRule
        from tradeflow.utils.security_list import SecurityList

        """))

        # Sort to generate consistent stub file:
        for api_func in sorted(TradingAlgorithm.all_api_methods(),
                               key=attrgetter('__name__')):
            stub.write('\n')
            sig = inspect._signature_bound_method(inspect.signature(api_func))

            indent = ' ' * 4
            stub.write(dedent('''\
                def {func_name}{func_sig}:
                    """'''.format(func_name=api_func.__name__,
                                  func_sig=sig)))
            stub.write(dedent('{indent}{func_doc}'.format(
                # `or '\n'` is to handle a None docstring:
                func_doc=dedent(api_func.__doc__.lstrip()) or '\n',
                indent=indent,
            )))
            stub.write('{indent}"""\n'.format(indent=indent))


if __name__ == '__main__':
    main()
