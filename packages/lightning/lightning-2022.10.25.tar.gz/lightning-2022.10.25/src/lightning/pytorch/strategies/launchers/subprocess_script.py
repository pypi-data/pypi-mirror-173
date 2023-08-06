try:

    from pytorch_lightning.strategies.launchers.subprocess_script import _HYDRA_AVAILABLE  # noqa: F401
    from pytorch_lightning.strategies.launchers.subprocess_script import _SubprocessScriptLauncher  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
