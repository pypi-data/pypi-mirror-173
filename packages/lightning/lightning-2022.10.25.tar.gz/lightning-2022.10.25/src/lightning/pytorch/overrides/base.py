try:

    from pytorch_lightning.overrides.base import _LightningPrecisionModuleWrapperBase  # noqa: F401
    from pytorch_lightning.overrides.base import _LightningModuleWrapperBase  # noqa: F401
    from pytorch_lightning.overrides.base import unwrap_lightning_module  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
