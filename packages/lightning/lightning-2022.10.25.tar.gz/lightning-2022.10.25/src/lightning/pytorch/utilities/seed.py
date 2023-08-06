try:

    from pytorch_lightning.utilities.seed import isolate_rng  # noqa: F401
    from pytorch_lightning.utilities.seed import seed_everything  # noqa: F401
    from pytorch_lightning.utilities.seed import reset_seed  # noqa: F401
    from pytorch_lightning.utilities.seed import pl_worker_init_function  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
