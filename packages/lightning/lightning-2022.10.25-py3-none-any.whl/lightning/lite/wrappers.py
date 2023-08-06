try:

    from lightning_lite.wrappers import T_destination  # noqa: F401
    from lightning_lite.wrappers import _LiteOptimizer  # noqa: F401
    from lightning_lite.wrappers import _LiteModule  # noqa: F401
    from lightning_lite.wrappers import _LiteDataLoader  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
