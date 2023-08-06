try:

    from lightning_lite.plugins.environments.slurm import log  # noqa: F401
    from lightning_lite.plugins.environments.slurm import SLURMEnvironment  # noqa: F401
    from lightning_lite.plugins.environments.slurm import _is_srun_used  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
