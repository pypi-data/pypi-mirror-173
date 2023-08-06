try:

    from lightning_lite.strategies.fairscale import _FAIRSCALE_AVAILABLE  # noqa: F401
    from lightning_lite.strategies.fairscale import DDPShardedStrategy  # noqa: F401
    from lightning_lite.strategies.fairscale import DDPSpawnShardedStrategy  # noqa: F401
    from lightning_lite.strategies.fairscale import _reinit_optimizers_with_oss  # noqa: F401
    from lightning_lite.strategies.fairscale import _FairscaleBackwardSyncControl  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
