try:
    from lightning_lite.plugins.collectives.collective import Collective
    from lightning_lite.plugins.collectives.single_device import SingleDeviceCollective
    from lightning_lite.plugins.collectives.torch_collective import TorchCollective

    from lightning_lite.plugins.collectives import __all__  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
