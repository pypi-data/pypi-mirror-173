try:

    from lightning_lite.strategies.launchers.multiprocessing import _MultiProcessingLauncher  # noqa: F401
    from lightning_lite.strategies.launchers.multiprocessing import _GlobalStateSnapshot  # noqa: F401
    from lightning_lite.strategies.launchers.multiprocessing import _check_bad_cuda_fork  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
