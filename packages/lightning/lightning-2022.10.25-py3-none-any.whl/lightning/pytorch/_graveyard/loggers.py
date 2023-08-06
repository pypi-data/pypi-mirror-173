try:

    from pytorch_lightning._graveyard.loggers import LoggerCollection  # noqa: F401
    from pytorch_lightning._graveyard.loggers import _update_agg_funcs  # noqa: F401
    from pytorch_lightning._graveyard.loggers import _agg_and_log_metrics  # noqa: F401
    from pytorch_lightning._graveyard.loggers import Logger  # noqa: F401
    from pytorch_lightning._graveyard.loggers import pl  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
