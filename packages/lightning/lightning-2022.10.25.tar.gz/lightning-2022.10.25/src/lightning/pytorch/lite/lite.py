try:

    from pytorch_lightning.lite.lite import _PL_PLUGIN  # noqa: F401
    from pytorch_lightning.lite.lite import _PL_PLUGIN_INPUT  # noqa: F401
    from pytorch_lightning.lite.lite import LightningLite  # noqa: F401
    from pytorch_lightning.lite.lite import _convert_deprecated_device_flags  # noqa: F401
    from pytorch_lightning.lite.lite import _to_lite_strategy  # noqa: F401
    from pytorch_lightning.lite.lite import _to_lite_precision  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
