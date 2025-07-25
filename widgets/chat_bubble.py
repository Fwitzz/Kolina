import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from utils.md_utils import md_to_pango

class ChatBubble(Gtk.EventBox):
    """Rounded rectangle bubble with optional markup support."""

    def __init__(self, text: str, is_user: bool, use_markup: bool = False):
        super().__init__()
        self.use_markup = use_markup

        cls = "bubble-user" if is_user else "bubble-bot"
        self.get_style_context().add_class(cls)
        self.set_visible_window(True)

        self.label = Gtk.Label()
        self.label.set_xalign(0)
        self.label.set_line_wrap(True)
        self.label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.label.set_max_width_chars(44)
        self.label.set_selectable(True)
        self.label.get_style_context().add_class("bubble-label")

        # Padding
        for side in ("top", "bottom", "start", "end"):
            getattr(self.label, f"set_margin_{side}")(4 if side in ("top","bottom") else 12)

        if use_markup:
            self.label.set_markup(md_to_pango(text))
        else:
            self.label.set_text(text)

        self.add(self.label)

    def get_label_widget(self) -> Gtk.Label:
        return self.label
