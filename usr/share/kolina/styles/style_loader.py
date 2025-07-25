from gi.repository import Gtk, Gdk

def load_css():
    provider = Gtk.CssProvider()
    with open("styles/style.css", "rb") as f:
        provider.load_from_data(f.read())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER
    )
