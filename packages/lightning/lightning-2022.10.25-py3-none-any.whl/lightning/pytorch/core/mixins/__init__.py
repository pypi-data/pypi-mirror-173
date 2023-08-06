try:

    from lightning_lite.utilities.device_dtype_mixin import _DeviceDtypeModuleMixin  # noqa: F401
    from pytorch_lightning.core.mixins.hparams_mixin import HyperparametersMixin  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
