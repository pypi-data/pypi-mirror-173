try:

    from pytorch_lightning.utilities.meta import is_meta_init  # noqa: F401
    from pytorch_lightning.utilities.meta import init_meta  # noqa: F401
    from pytorch_lightning.utilities.meta import get_all_subclasses  # noqa: F401
    from pytorch_lightning.utilities.meta import recursively_setattr  # noqa: F401
    from pytorch_lightning.utilities.meta import materialize_module  # noqa: F401
    from pytorch_lightning.utilities.meta import init_meta_context  # noqa: F401
    from pytorch_lightning.utilities.meta import is_on_meta_device  # noqa: F401
    from pytorch_lightning.utilities.meta import _is_deferred  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
