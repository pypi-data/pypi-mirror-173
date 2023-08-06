try:

    from lightning_lite.accelerators.tpu import TPUAccelerator  # noqa: F401
    from lightning_lite.accelerators.tpu import TPU_CHECK_TIMEOUT  # noqa: F401
    from lightning_lite.accelerators.tpu import _inner_f  # noqa: F401
    from lightning_lite.accelerators.tpu import _multi_process  # noqa: F401
    from lightning_lite.accelerators.tpu import _is_device_tpu  # noqa: F401
    from lightning_lite.accelerators.tpu import _XLA_AVAILABLE  # noqa: F401
    from lightning_lite.accelerators.tpu import tpu_distributed  # noqa: F401
    from lightning_lite.accelerators.tpu import parse_tpu_cores  # noqa: F401
    from lightning_lite.accelerators.tpu import _tpu_cores_valid  # noqa: F401
    from lightning_lite.accelerators.tpu import _parse_tpu_cores_str  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
