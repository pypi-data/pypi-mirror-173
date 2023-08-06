try:

    from pytorch_lightning.plugins.environments.bagua_environment import log  # noqa: F401
    from pytorch_lightning.plugins.environments.bagua_environment import BaguaEnvironment  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
