try:

    from pytorch_lightning._graveyard.trainer import _patch_sys_modules  # noqa: F401
    from pytorch_lightning._graveyard.trainer import TrainerDataLoadingMixin  # noqa: F401
    from pytorch_lightning._graveyard.trainer import TrainerOptimizersMixin  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _gpus  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _root_gpu  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _tpu_cores  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _ipus  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _num_gpus  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _devices  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _use_amp  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _weights_save_path  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _lightning_optimizers  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _should_rank_save_checkpoint  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _validated_ckpt_path  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _validated_ckpt_path_setter  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _tested_ckpt_path  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _tested_ckpt_path_setter  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _predicted_ckpt_path  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _predicted_ckpt_path_setter  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _verbose_evaluate  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _verbose_evaluate_setter  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _run_stage  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _call_hook  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _prepare_dataloader  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _request_dataloader  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _init_optimizers  # noqa: F401
    from pytorch_lightning._graveyard.trainer import _convert_to_lightning_optimizers  # noqa: F401
    from pytorch_lightning._graveyard.trainer import Trainer  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
