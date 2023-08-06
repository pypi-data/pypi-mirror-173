try:

    from pytorch_lightning.core.module import warning_cache  # noqa: F401
    from pytorch_lightning.core.module import log  # noqa: F401
    from pytorch_lightning.core.module import MODULE_OPTIMIZERS  # noqa: F401
    from pytorch_lightning.core.module import LightningModule  # noqa: F401
    from pytorch_lightning.core.module import _jit_is_scripting  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
