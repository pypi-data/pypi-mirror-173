try:

    from pytorch_lightning._graveyard.training_type import _patch_sys_modules  # noqa: F401
    from pytorch_lightning._graveyard.training_type import _ttp_constructor  # noqa: F401
    from pytorch_lightning._graveyard.training_type import _patch_plugin_classes  # noqa: F401
    from pytorch_lightning._graveyard.training_type import on_colab_kaggle  # noqa: F401
    from pytorch_lightning._graveyard.training_type import _training_type_plugin  # noqa: F401
    from pytorch_lightning._graveyard.training_type import pl  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
