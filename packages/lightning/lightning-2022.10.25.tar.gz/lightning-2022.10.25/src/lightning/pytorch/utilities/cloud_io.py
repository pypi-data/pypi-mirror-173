try:

    from pytorch_lightning.utilities.cloud_io import atomic_save  # noqa: F401
    from pytorch_lightning.utilities.cloud_io import get_filesystem  # noqa: F401
    from pytorch_lightning.utilities.cloud_io import load  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
