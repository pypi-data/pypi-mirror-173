try:

    from pytorch_lightning.utilities.device_parser import parse_hpus  # noqa: F401
    from pytorch_lightning.utilities.device_parser import determine_root_gpu_device  # noqa: F401
    from pytorch_lightning.utilities.device_parser import is_cuda_available  # noqa: F401
    from pytorch_lightning.utilities.device_parser import num_cuda_devices  # noqa: F401
    from pytorch_lightning.utilities.device_parser import parse_cpu_cores  # noqa: F401
    from pytorch_lightning.utilities.device_parser import parse_gpu_ids  # noqa: F401
    from pytorch_lightning.utilities.device_parser import parse_tpu_cores  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
