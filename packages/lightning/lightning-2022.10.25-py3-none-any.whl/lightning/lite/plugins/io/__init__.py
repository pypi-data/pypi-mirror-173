try:

    from lightning_lite.plugins.io.checkpoint_io import CheckpointIO
    from lightning_lite.plugins.io.torch_io import TorchCheckpointIO
    from lightning_lite.plugins.io.xla import XLACheckpointIO

    from lightning_lite.plugins.io import __all__  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
