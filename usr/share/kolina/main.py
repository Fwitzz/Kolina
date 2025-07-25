#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from window import KolinaWindow

# Set default icon for all windows
Gtk.Window.set_default_icon_name("kolina")

def main():
    win = KolinaWindow()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    main()
