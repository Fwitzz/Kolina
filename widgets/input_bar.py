from gi.repository import Gtk

class InputBar(Gtk.Box):
    def __init__(self, on_send_callback):
        super().__init__(spacing=6)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Skriv noget...")
        self.pack_start(self.entry, True, True, 0)

        self.button = Gtk.Button(label="Send")
        self.button.connect("clicked", on_send_callback)
        self.pack_start(self.button, False, False, 0)

    def get_input(self):
        return self.entry.get_text()

    def clear(self):
        self.entry.set_text("")
