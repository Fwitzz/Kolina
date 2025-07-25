#!/usr/bin/env python3
import os

# -------- Manual .env loading --------
# Check for .env in user config and project root
env_paths = [
    os.path.expanduser("~/.config/kolina/.env"),
    os.path.join(os.path.dirname(__file__), ".env"),
]
for env_path in env_paths:
    if os.path.isfile(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue
                key, sep, val = line.partition("=")
                if sep != "=":
                    continue
                key = key.strip()
                # Remove quotes if present
                val = val.strip().strip("'\"")
                # Do not override existing environment vars
                if key not in os.environ:
                    os.environ[key] = val

# -------- Standard GTK startup --------
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from window import KolinaWindow

# Verify API key after loading .env
from backend.chat_api import API_KEY
if not API_KEY:
    raise RuntimeError("MISTRAL_API_KEY ikke sat – husk at oprette .env eller eksportere variablen")

# Set default icon for all windows
Gtk.Window.set_default_icon_name("kolina")

def main():
    win = KolinaWindow()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    main()
