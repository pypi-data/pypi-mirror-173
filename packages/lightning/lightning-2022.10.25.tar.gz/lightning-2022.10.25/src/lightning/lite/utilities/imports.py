try:

    from lightning_lite.utilities.imports import _IS_WINDOWS  # noqa: F401
    from lightning_lite.utilities.imports import _IS_INTERACTIVE  # noqa: F401
    from lightning_lite.utilities.imports import _PYTHON_GREATER_EQUAL_3_8_0  # noqa: F401
    from lightning_lite.utilities.imports import _PYTHON_GREATER_EQUAL_3_10_0  # noqa: F401
    from lightning_lite.utilities.imports import _TORCH_GREATER_EQUAL_1_9_1  # noqa: F401
    from lightning_lite.utilities.imports import _TORCH_GREATER_EQUAL_1_10  # noqa: F401
    from lightning_lite.utilities.imports import _TORCH_LESSER_EQUAL_1_10_2  # noqa: F401
    from lightning_lite.utilities.imports import _TORCH_GREATER_EQUAL_1_11  # noqa: F401
    from lightning_lite.utilities.imports import _TORCH_GREATER_EQUAL_1_12  # noqa: F401
    from lightning_lite.utilities.imports import _TORCH_GREATER_EQUAL_1_13  # noqa: F401
    from lightning_lite.utilities.imports import _TORCH_GREATER_EQUAL_1_14  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
