try:

    from lightning_lite.strategies.ddp import DDPStrategy  # noqa: F401
    from lightning_lite.strategies.ddp_spawn import DDPSpawnStrategy  # noqa: F401
    from lightning_lite.strategies.deepspeed import DeepSpeedStrategy  # noqa: F401
    from lightning_lite.strategies.dp import DataParallelStrategy  # noqa: F401
    from lightning_lite.strategies.fairscale import DDPShardedStrategy  # noqa: F401
    from lightning_lite.strategies.fairscale import DDPSpawnShardedStrategy  # noqa: F401
    from lightning_lite.strategies.parallel import ParallelStrategy  # noqa: F401
    from lightning_lite.strategies.registry import _call_register_strategies, _StrategyRegistry
    from lightning_lite.strategies.single_device import SingleDeviceStrategy  # noqa: F401
    from lightning_lite.strategies.single_tpu import SingleTPUStrategy  # noqa: F401
    from lightning_lite.strategies.strategy import Strategy  # noqa: F401
    from lightning_lite.strategies.xla import XLAStrategy  # noqa: F401

    from lightning_lite.strategies import STRATEGY_REGISTRY  # noqa: F401
    from lightning_lite.strategies import _STRATEGIES_BASE_MODULE  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
