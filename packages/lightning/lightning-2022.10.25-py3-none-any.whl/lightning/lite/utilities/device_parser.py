try:

    from lightning_lite.utilities.device_parser import determine_root_gpu_device  # noqa: F401
    from lightning_lite.utilities.device_parser import parse_gpu_ids  # noqa: F401
    from lightning_lite.utilities.device_parser import _normalize_parse_gpu_string_input  # noqa: F401
    from lightning_lite.utilities.device_parser import _sanitize_gpu_ids  # noqa: F401
    from lightning_lite.utilities.device_parser import _normalize_parse_gpu_input_to_list  # noqa: F401
    from lightning_lite.utilities.device_parser import _get_all_available_gpus  # noqa: F401
    from lightning_lite.utilities.device_parser import _check_unique  # noqa: F401
    from lightning_lite.utilities.device_parser import _check_data_type  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
