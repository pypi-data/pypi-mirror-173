try:

    import numpy

    from lightning_lite.utilities import move_data_to_device  # noqa: F401
    from lightning_lite.utilities import AMPType, LightningEnum  # noqa: F401
    from lightning_lite.utilities.distributed import AllGatherGrad  # noqa: F401
    from pytorch_lightning.utilities.enums import GradClipAlgorithmType  # noqa: F401
    from pytorch_lightning.utilities.grads import grad_norm  # noqa: F401
    from pytorch_lightning.utilities.imports import (  # noqa: F401
        _APEX_AVAILABLE,
        _HIVEMIND_AVAILABLE,
        _HOROVOD_AVAILABLE,
        _HPU_AVAILABLE,
        _IPU_AVAILABLE,
        _IS_INTERACTIVE,
        _IS_WINDOWS,
        _OMEGACONF_AVAILABLE,
        _POPTORCH_AVAILABLE,
        _TORCH_GREATER_EQUAL_1_10,
        _TORCH_GREATER_EQUAL_1_11,
        _TORCH_GREATER_EQUAL_1_12,
        _TORCH_QUANTIZE_AVAILABLE,
        _TORCHVISION_AVAILABLE,
    )
    from pytorch_lightning.utilities.parameter_tying import find_shared_parameters, set_shared_parameters  # noqa: F401
    from pytorch_lightning.utilities.parsing import AttributeDict, flatten_dict, is_picklable  # noqa: F401
    from pytorch_lightning.utilities.rank_zero import (  # noqa: F401
        rank_zero_deprecation,
        rank_zero_info,
        rank_zero_only,
        rank_zero_warn,
    )

    from pytorch_lightning.utilities import FLOAT16_EPSILON  # noqa: F401
    from pytorch_lightning.utilities import FLOAT32_EPSILON  # noqa: F401
    from pytorch_lightning.utilities import FLOAT64_EPSILON  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
