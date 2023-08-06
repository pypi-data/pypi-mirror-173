try:

    from lightning_lite.plugins import ClusterEnvironment  # noqa: F401
    from lightning_lite.plugins.environments import (  # noqa: F401
        KubeflowEnvironment,
        LightningEnvironment,
        LSFEnvironment,
        SLURMEnvironment,
        TorchElasticEnvironment,
        XLAEnvironment,
    )
    from pytorch_lightning.plugins.environments.bagua_environment import BaguaEnvironment  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
