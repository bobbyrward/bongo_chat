import gtk
import webkit
import gobject
import urllib
import urlparse

from .. import config


class OAuthDialog(gtk.Dialog):
    __gsignals__ = {
        'oauth-authtoken-granted': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [gobject.TYPE_STRING])
    }

    def __init__(self, parent):
        super(OAuthDialog, self).__init__('Log in to Twitch.TV', parent, gtk.DIALOG_MODAL)
        self.scrolled_window = gtk.ScrolledWindow()
        self.web_view = webkit.WebView()
        self.scrolled_window.add(self.web_view)
        self.vbox.pack_end(self.scrolled_window)

        self.web_view.connect(
            'resource-request-starting',
            self._resource_request_starting
        )

        url = 'https://api.twitch.tv/kraken/oauth2/authorize?{}'.format(
            urllib.urlencode({
                'response_type': 'code',
                'client_id': config.CLIENT_ID,
                'redirect_uri': config.CALLBACK_URL,
                'scope': ' '.join(['chat_login', 'user_read']),
            })
        )

        self.set_default_size(800, 400)
        self.web_view.load_uri(url)
        self.web_view.show()
        self.scrolled_window.show()

    def _resource_request_starting(self, view, frame, resource, request, response, data=None):
        uri = resource.get_uri()
        parsed_url = urlparse.urlparse(uri)

        if parsed_url.scheme == config.CALLBACK_SCHEME:
            query_params = urlparse.parse_qs(parsed_url.query)
            self.emit('oauth-authtoken-granted', query_params['code'][0])
            self.response(gtk.RESPONSE_OK)
            return webkit.NAVIGATION_RESPONSE_IGNORE
