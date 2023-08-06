try:

    from lightning_lite.accelerators.cuda import CUDAAccelerator  # noqa: F401
    from lightning_lite.accelerators.cuda import _get_all_available_cuda_gpus  # noqa: F401
    from lightning_lite.accelerators.cuda import _patch_cuda_is_available  # noqa: F401
    from lightning_lite.accelerators.cuda import num_cuda_devices  # noqa: F401
    from lightning_lite.accelerators.cuda import is_cuda_available  # noqa: F401
    from lightning_lite.accelerators.cuda import _parse_visible_devices  # noqa: F401
    from lightning_lite.accelerators.cuda import _raw_device_count_nvml  # noqa: F401
    from lightning_lite.accelerators.cuda import _device_count_nvml  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
