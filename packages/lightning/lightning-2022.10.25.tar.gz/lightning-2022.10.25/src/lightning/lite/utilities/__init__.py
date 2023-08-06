try:

    from lightning_lite.utilities.apply_func import move_data_to_device  # noqa: F401
    from lightning_lite.utilities.enums import _AcceleratorType, _StrategyType, AMPType, LightningEnum  # noqa: F401
    from lightning_lite.utilities.rank_zero import (  # noqa: F401
        rank_zero_deprecation,
        rank_zero_info,
        rank_zero_only,
        rank_zero_warn,
    )

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
