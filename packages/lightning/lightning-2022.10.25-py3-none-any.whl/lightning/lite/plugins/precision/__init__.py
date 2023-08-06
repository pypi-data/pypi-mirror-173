try:

    from lightning_lite.plugins.precision.deepspeed import DeepSpeedPrecision
    from lightning_lite.plugins.precision.double import DoublePrecision
    from lightning_lite.plugins.precision.native_amp import NativeMixedPrecision
    from lightning_lite.plugins.precision.precision import Precision
    from lightning_lite.plugins.precision.tpu import TPUPrecision
    from lightning_lite.plugins.precision.tpu_bf16 import TPUBf16Precision

    from lightning_lite.plugins.precision import __all__  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
