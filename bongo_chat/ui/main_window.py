import gtk
import gobject
import requests

from . authenticated_view import AuthenticatedView
from . unauthenticated_view import UnauthenticatedView
from . oauth_dialog import OAuthDialog
from .. import config


class MainWindow(gtk.Window):
    __gsignals__ = {
        'authenticated': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [gobject.TYPE_STRING])
    }

    def __init__(self):
        super(MainWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self._create_ui()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def close(self, widget):
        self.emit('delete-event', gtk.gdk.Event(gtk.gdk.DELETE))

    def _create_ui(self):
        self.set_title('BongoChat')
        self.connect('delete_event', self.delete_event)
        self.set_border_width(10)
        self.set_default_size(1024, 800)

        self.need_login = UnauthenticatedView(self)
        self.need_login.show()
        self.need_login.connect('do-login', self._do_login)
        self.add(self.need_login)

        self.authenticated_view = AuthenticatedView(self)
        self.authenticated_view.hide()

        self.show()

    def _show_logged_in_ui(self):
        self.need_login.hide()
        self.remove(self.need_login)

        self.authenticated_view.show()
        self.add(self.authenticated_view)

    def _show_fatal_error(self, error_message):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, error_message)
        dialog.run()
        dialog.destroy()
        self.destroy()

    def _get_access_token(self, auth_token):
        request_data = {
            'client_id': config.CLIENT_ID,
            'client_secret': config.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': config.CALLBACK_URL,
            'code': auth_token,
        }
        print request_data

        response = requests.post('https://api.twitch.tv/kraken/oauth2/token', request_data)

        try:
            response.raise_for_status()
        except Exception as exc:
            print response.content
            self._show_fatal_error(str(exc))
            raise

        self.access_token = response.json()['access_token']
        self.emit('authenticated', self.access_token)

    def _on_authtoken_granted(self, source, auth_token):
        print '_on_authtoken_granted({})'.format(auth_token)
        self.authtoken = auth_token
        self._get_access_token(auth_token)
        self._show_logged_in_ui()

    def _do_login(self, source):
        self.login = OAuthDialog(self)
        self.login.connect('oauth-authtoken-granted', self._on_authtoken_granted)
        self.login.run()
        self.login.destroy()
