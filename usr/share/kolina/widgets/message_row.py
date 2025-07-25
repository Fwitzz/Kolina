import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from widgets.avatar import Avatar
from widgets.chat_bubble import ChatBubble

class MessageRow(Gtk.ListBoxRow):
    """
    Avatar + name above bubble start; extra spacing between rows.
    Supports an optional `use_markup` flag for Pango markup bubbles.
    """

    def __init__(self, sender: str, text: str, is_user: bool, use_markup: bool = False):
        super().__init__()
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        outer.set_margin_start(12)
        outer.set_margin_end(12)
        outer.set_margin_bottom(18)
        outer.set_margin_top(2)

        grid = Gtk.Grid()
        grid.set_column_spacing(6)
        outer.pack_start(grid, False, False, 0)

        # Avatar + name
        avatar = Avatar(sender[:1], is_user)
        name_label = Gtk.Label(label=sender)
        name_label.get_style_context().add_class("name-label")
        name_label.get_style_context().add_class("name-label-user" if is_user else "name-label-bot")
        name_label.set_xalign(0.0)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        header.pack_start(avatar, False, False, 0)
        header.pack_start(name_label, False, False, 0)
        header.set_margin_bottom(4)

        # Chat bubble (now with markup support)
        bubble = ChatBubble(text, is_user, use_markup=use_markup)

        filler = Gtk.Box()
        filler.set_hexpand(True)

        if is_user:
            header.set_margin_end(6)
            grid.attach(filler, 0, 0, 1, 2)
            grid.attach(header, 1, 0, 1, 1)
            grid.attach(bubble, 1, 1, 1, 1)
        else:
            header.set_margin_start(6)
            grid.attach(header, 0, 0, 1, 1)
            grid.attach(bubble, 0, 1, 1, 1)
            grid.attach(filler, 1, 0, 1, 2)

        self.add(outer)

    def get_bubble_label(self) -> Gtk.Label:
        """
        Return the internal Gtk.Label of the chat bubble,
        for animating text or updating markup.
        """
        # The bubble is the second child of the grid row
        # but easier to find it:
        for child in self.get_children():
            # outer box
            for grand in child.get_children():
                if isinstance(grand, Gtk.Grid):
                    grid = grand
                    # locate the ChatBubble widget
                    for widget in grid.get_children():
                        if isinstance(widget, ChatBubble):
                            return widget.get_label_widget()
        raise RuntimeError("Could not locate bubble label")
