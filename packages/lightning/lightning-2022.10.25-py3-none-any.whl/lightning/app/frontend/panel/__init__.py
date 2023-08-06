try:
    from lightning_app.frontend.panel.app_state_watcher import AppStateWatcher
    from lightning_app.frontend.panel.panel_frontend import PanelFrontend

    from lightning_app.frontend.panel import __all__  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_app import __version__
    msg = f'Your `lightning` package was built for `lightning_app==1.8.0rc0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
