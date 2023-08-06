try:

    from lightning_lite.plugins.environments.lightning import LightningEnvironment  # noqa: F401
    from lightning_lite.plugins.environments.lightning import find_free_network_port  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
