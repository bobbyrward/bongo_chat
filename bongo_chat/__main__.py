import logging

from .ui.main_window import MainWindow
from . import app


def main():
    logging.basicConfig(level=logging.DEBUG)
    app._APPLICATION = app.Application(MainWindow)
    app.get_app().main()


if __name__ == '__main__':
    main()
