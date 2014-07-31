import gtk
import gobject


class UnauthenticatedView(gtk.HBox):
    __gsignals__ = {
        'do-login': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [])
    }

    def __init__(self, parent):
        super(UnauthenticatedView, self).__init__()
        self._create_ui()

    def _on_button_click(self, source, data=None):
        self.emit('do-login')

    def _create_ui(self):
        self.button = gtk.Button('Log in to Twitch.TV')
        self.button.connect('clicked', self._on_button_click)
        self.button.show()

        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.button, True, False, 30)
        self.vbox.show()

        self.pack_start(self.vbox, True, False, 30)
