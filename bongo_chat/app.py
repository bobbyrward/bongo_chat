import gtk
import gobject

from . import config


class Application(gobject.GObject):
    def __init__(self, main_window_class):
        self.main_window_class = main_window_class

    def main(self):
        self.main_window = self.main_window_class()
        gtk.main()

    def config(self):
        return config

    def main_window(self):
        return self.main_window


_APPLICATION = None


def get_app():
    return _APPLICATION
