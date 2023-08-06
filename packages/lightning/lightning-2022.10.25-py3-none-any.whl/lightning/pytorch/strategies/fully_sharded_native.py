try:

    from pytorch_lightning.strategies.fully_sharded_native import _distributed_available  # noqa: F401
    from pytorch_lightning.strategies.fully_sharded_native import _fsdp_available  # noqa: F401
    from pytorch_lightning.strategies.fully_sharded_native import log  # noqa: F401
    from pytorch_lightning.strategies.fully_sharded_native import DDPFullyShardedNativeStrategy  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
