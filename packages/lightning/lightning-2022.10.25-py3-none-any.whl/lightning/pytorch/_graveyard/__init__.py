try:

    import pytorch_lightning._graveyard.callbacks
    import pytorch_lightning._graveyard.core
    import pytorch_lightning._graveyard.loggers
    import pytorch_lightning._graveyard.trainer
    import pytorch_lightning._graveyard.training_type  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
