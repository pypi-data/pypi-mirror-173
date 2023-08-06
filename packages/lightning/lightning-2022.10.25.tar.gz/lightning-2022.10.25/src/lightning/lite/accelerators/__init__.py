try:

    from lightning_lite.accelerators.accelerator import Accelerator  # noqa: F401
    from lightning_lite.accelerators.cpu import CPUAccelerator  # noqa: F401
    from lightning_lite.accelerators.cuda import CUDAAccelerator  # noqa: F401
    from lightning_lite.accelerators.mps import MPSAccelerator  # noqa: F401
    from lightning_lite.accelerators.registry import _AcceleratorRegistry, call_register_accelerators
    from lightning_lite.accelerators.tpu import TPUAccelerator  # noqa: F401

    from lightning_lite.accelerators import _ACCELERATORS_BASE_MODULE  # noqa: F401
    from lightning_lite.accelerators import ACCELERATOR_REGISTRY  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
