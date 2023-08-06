try:

    from pytorch_lightning.utilities.upgrade_checkpoint import KEYS_MAPPING  # noqa: F401
    from pytorch_lightning.utilities.upgrade_checkpoint import log  # noqa: F401
    from pytorch_lightning.utilities.upgrade_checkpoint import upgrade_checkpoint  # noqa: F401
    if __name__ == "__main__":

        from pytorch_lightning.utilities.upgrade_checkpoint import parser  # noqa: F401
        from pytorch_lightning.utilities.upgrade_checkpoint import args  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
