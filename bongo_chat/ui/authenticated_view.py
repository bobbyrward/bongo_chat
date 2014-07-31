import gtk


class AuthenticatedView(gtk.HBox):
    def __init__(self, parent):
        super(AuthenticatedView, self).__init__()
        self._create_ui()
        self._connect_signals(parent)
        self.access_token = None

    def _create_ui(self):
        self.label = gtk.Label('Token: ')
        self.pack_end(self.label, True, False, 30)
        self.label.show()

    def _connect_signals(self, parent):
        parent.connect('authenticated', self._on_authenticated)

    def _on_authenticated(self, source, access_token):
        self.access_token = access_token
