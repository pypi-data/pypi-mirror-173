try:

    from pytorch_lightning.tuner.tuning import _TunerResult  # noqa: F401
    from pytorch_lightning.tuner.tuning import Tuner  # noqa: F401
    from pytorch_lightning.tuner.tuning import _check_tuner_configuration  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
