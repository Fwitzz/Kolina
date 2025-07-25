from gi.repository import Gtk

class Avatar(Gtk.EventBox):
    def __init__(self, initial: str, is_user: bool):
        super().__init__()
        style = self.get_style_context()
        style.add_class("avatar")
        if is_user:
            style.add_class("avatar-user")
        self.set_size_request(32, 32)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)

        lbl = Gtk.Label(label=initial.upper())
        lbl.get_style_context().add_class("avatar-label")
        box.pack_start(lbl, True, True, 0)
        self.add(box)
