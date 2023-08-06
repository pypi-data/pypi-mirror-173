try:

    from pytorch_lightning.trainer.setup import _init_debugging_flags  # noqa: F401
    from pytorch_lightning.trainer.setup import _determine_batch_limits  # noqa: F401
    from pytorch_lightning.trainer.setup import _init_profiler  # noqa: F401
    from pytorch_lightning.trainer.setup import _log_device_info  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
