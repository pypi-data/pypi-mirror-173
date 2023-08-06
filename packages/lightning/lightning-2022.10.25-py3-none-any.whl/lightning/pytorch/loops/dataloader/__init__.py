try:

    from pytorch_lightning.loops.dataloader.dataloader_loop import DataLoaderLoop  # noqa: F401
    from pytorch_lightning.loops.dataloader.evaluation_loop import EvaluationLoop  # noqa: F401
    from pytorch_lightning.loops.dataloader.prediction_loop import PredictionLoop  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
