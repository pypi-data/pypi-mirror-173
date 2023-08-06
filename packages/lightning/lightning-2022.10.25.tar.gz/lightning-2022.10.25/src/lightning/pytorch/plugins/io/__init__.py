try:

    from lightning_lite.plugins import CheckpointIO, TorchCheckpointIO, XLACheckpointIO
    from pytorch_lightning.plugins.io.async_plugin import AsyncCheckpointIO
    from pytorch_lightning.plugins.io.hpu_plugin import HPUCheckpointIO

    from pytorch_lightning.plugins.io import __all__  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
