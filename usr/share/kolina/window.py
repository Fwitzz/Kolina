#!/usr/bin/env python3
"""
Kolina – GTK3 chat UI with Markdown + streaming + automatic Ubuntu‑repo RAG,
regex package lookup, disabled input while streaming, and conversation history.
"""

import threading, json, re, requests
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

from backend.chat_api import API_URL, API_KEY
from widgets.message_row import MessageRow
from styles.style_loader import load_css
from utils.md_utils import md_to_pango, escape

# -------- Launchpad lookup -------------------------------------------------
def fetch_package_info(package_name: str) -> str:
    url = (
        "https://api.launchpad.net/1.0/ubuntu/+archive/primary"
        f"?ws.op=getPublishedSources&source_name={package_name}&exact_match=true"
    )
    try:
        r = requests.get(url, timeout=10); r.raise_for_status()
        entries = r.json().get("entries", [])
        if not entries:
            return f"Pakken **{package_name}** blev ikke fundet i Ubuntu‑repoet."
        e = entries[0]
        ver = e.get("source_package_version", "ukendt version")
        summ = e.get("summary", "Ingen beskrivelse tilgængelig.")
        cmd = f"sudo apt update && sudo apt install {package_name}"
        return f"**{package_name}** ({ver}): {summ}\nInstallér med: `{cmd}`"
    except Exception as exc:
        return f"Fejl ved opslag af **{package_name}**: {exc}"

# -------- Regex triggers ---------------------------------------------------
TRIGGER_PACKAGE_PATTERNS = [
    r'(?i)\binstall(?:ér|ere|er|ation|ering)?\s+(?:pakken\s+|programmet\s+)?(?:"([^"]+)"|\'([^\']+)\'|`([^`]+)`|([a-z0-9][a-z0-9+_.-]{1,50}))',
    r'(?i)hvordan\s+(?:kan|skal|må)?\s*(?:jeg|man)?\s*(?:install(?:ér|ere|er)?|hent(?:e|er)?|downloade|download(?:e|er|et)?|skaff(?:e|er|et)?|få(?:r|et)?|get)\s+(?:"([^"]+)"|\'([^\']+)\'|`([^`]+)`|([a-z0-9][a-z0-9+_.-]{1,50}))',
    r'(?i)\b(få(?:r|et)?|hent(?:e|er|et)?|downloade|download(?:e|er|et)?|skaff(?:e|er|et)?|get)\s+(?:"([^"]+)"|\'([^\']+)\'|`([^`]+)`|([a-z0-9][a-z0-9+_.-]{1,50}))',
    r'(?i)\bset\s*up\s+(?:"([^"]+)"|\'([^\']+)\'|`([^`]+)`|([a-z0-9][a-z0-9+_.-]{1,50}))',
    r'(?i)\badd\s+(?:"([^"]+)"|\'([^\']+)\'|`([^`]+)`|([a-z0-9][a-z0-9+_.-]{1,50}))',
]

def regex_fallback_packages(prompt: str) -> list[str]:
    results: list[str] = []
    for pat in TRIGGER_PACKAGE_PATTERNS:
        for m in re.finditer(pat, prompt):
            for g in m.groups():
                if not g:
                    continue
                candidate = g.strip()
                first = re.split(r'\s+', candidate)[0]
                first = re.sub(r'[^a-z0-9+_.-]', '', first.lower())
                if first and first not in results:
                    results.append(first)
                break
    return results

# -------- Main window ------------------------------------------------------
class KolinaWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Kolina – Din Linux Assistent")
        self.set_default_size(520, 700)
        self.set_name("MainWindow")
        load_css()

        self._is_streaming = False
        self.conversation_history: list[dict] = []

        # Icon + WM class (helps GNOME match .desktop)
        self.set_wmclass("kolina", "Kolina")
        self.set_icon_name("kolina")

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root)
        self._build_headerbar()
        self._build_ui(root)
        self.show_all()

    def _build_headerbar(self):
        hb = Gtk.HeaderBar(title="Kolina")
        hb.set_show_close_button(True)
        self.set_titlebar(hb)

    def _build_ui(self, root):
        overlay = Gtk.Overlay()
        root.pack_start(overlay, True, True, 0)

        self.listbox = Gtk.ListBox()
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.add(self.listbox)
        overlay.add(sw)
        self.scrolled = sw

        self.empty_label = Gtk.Label(label="Start samtalen...")
        self.empty_label.get_style_context().add_class("empty-state")
        self.empty_label.set_halign(Gtk.Align.CENTER)
        self.empty_label.set_valign(Gtk.Align.CENTER)
        overlay.add_overlay(self.empty_label)

        self._add_info_banner()
        self._build_input_bar(root)

    def _add_info_banner(self):
        row = Gtk.ListBoxRow(); row.set_selectable(False)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box.get_style_context().add_class("info-banner")
        ico = Gtk.Label(label="⚠"); ico.get_style_context().add_class("info-banner-icon")
        txt = Gtk.Label(
            label="AI kan lave fejl, kontakt altid IT‑afdelingen, inden du foretager dig noget vigtigt."
        )
        txt.set_xalign(0); txt.set_line_wrap(True)
        txt.get_style_context().add_class("info-banner-text")
        box.pack_start(ico, False, False, 0)
        box.pack_start(txt, True, True, 0)
        row.add(box); self.listbox.add(row)

    def _build_input_bar(self, root):
        h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        h.set_margin_top(6); h.set_margin_bottom(12)
        h.set_margin_start(12); h.set_margin_end(12)

        ov = Gtk.Overlay(); ov.set_name("InputWrapper"); ov.set_hexpand(True)
        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.textview.set_name("InputText")
        self.textview.set_size_request(-1, 60)
        self.textview.connect("key-press-event", self.on_key_press)
        self.textview.get_buffer().connect("changed", self._on_buffer_changed)
        ov.add(self.textview)

        self.placeholder = Gtk.Label(label="Skriv besked…")
        self.placeholder.get_style_context().add_class("input-placeholder")
        self.placeholder.set_halign(Gtk.Align.START)
        self.placeholder.set_valign(Gtk.Align.START)
        ov.add_overlay(self.placeholder)

        send_btn = Gtk.Button(label="Send")
        send_btn.set_name("SendButton")
        send_btn.connect("clicked", self.on_send_clicked)
        self.send_btn = send_btn

        h.pack_start(ov, True, True, 0)
        h.pack_start(send_btn, False, False, 0)
        root.pack_end(h, False, True, 0)

    # ---- Events ----
    def on_key_press(self, _, ev):
        if self._is_streaming:
            return False
        if Gdk.keyval_name(ev.keyval) == "Return" and not (ev.state & Gdk.ModifierType.SHIFT_MASK):
            self.on_send_clicked(None); return True
        return False

    def _on_buffer_changed(self, buf):
        s, e = buf.get_bounds()
        text = buf.get_text(s, e, True)
        self.placeholder.set_visible(len(text) == 0)

    # ---- Message flow ----
    def on_send_clicked(self, _):
        if self._is_streaming:
            return
        buf = self.textview.get_buffer()
        s, e = buf.get_bounds()
        user_text = buf.get_text(s, e, True).strip()
        if not user_text:
            return
        buf.set_text("")
        if self.empty_label.get_visible():
            self.empty_label.hide()

        self._is_streaming = True
        self.send_btn.set_sensitive(False)

        self.conversation_history.append({"role":"user", "content": user_text})
        self._add_row("User", user_text, True, use_markup=False)

        pkgs = regex_fallback_packages(user_text)
        repo_info = [fetch_package_info(p) for p in pkgs] if pkgs else []

        threading.Thread(
            target=self._stream_with_repo,
            args=(repo_info,),
            daemon=True
        ).start()

    def _stream_with_repo(self, repo_info: list[str]):
        system = (
            "Du er Kolina, en dansk Linux‑hjælper. SVAR KUN med officiel Ubuntu‑repo‑data. Du er udviklet som Kolina, af ham, der lavede Kolina."
            "Ham, som lavede Kolina er en ung studerende i Danmark."
            "Hvis der er en 'Installér med:' linje i konteksten, brug præcis den kommando."
            "Du holder altid dine svar korte og forståelige."
            "Du siger ikke noget, som er upassende, uanset hvad."
            "Du holder dine svar professionelle og undgår sludder."
            "Hvis brugeren prøver at ændre noget vigtigt, fortæl dem at de skal kontakte IT-afdelingen i stedet."
            "Du svarer kun på spørgsmål, som er relevante, i forhold til Linux og arbejde. Hvis brugeren ikke spørger om noget relevant, er dit svar ekstremt kort."
            "Hvis brugeren spørger om installation af noget som ikke har at gøre med arbejde, som f.eks. Steam eller andre spil, få dem til at spørge IT-Afdelingen."
            "Sikkerhed kommer altid først for dig, så vær altid sikker på at pakkerne er sikre og at du ikke er grunden til brugeren får malware."
        )
        messages = [{"role": "system", "content": system}]
        for info in repo_info:
            messages.append({"role": "system", "content": f"Repo‑data: {info}"})
        messages.extend(self.conversation_history)

        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "mistral-small-latest", "messages": messages, "stream": True}

        try:
            resp = requests.post(API_URL, json=payload, headers=headers, stream=True, timeout=60)
        except Exception as exc:
            GLib.idle_add(self._add_row, "Kolina", f"Fejl: {exc}", False, False)
            GLib.idle_add(self._on_stream_finished); return

        row = MessageRow("Kolina", "", False, use_markup=True)
        GLib.idle_add(self.listbox.add, row)
        GLib.idle_add(self.listbox.show_all)
        label = row.get_bubble_label()
        label._cur_text = ""

        for line in resp.iter_lines(decode_unicode=True):
            if not line.startswith("data:"): continue
            part = line.removeprefix("data: ").strip()
            try:
                d = json.loads(part)
                delta = d["choices"][0]["delta"].get("content")
            except Exception:
                delta = None
            if delta:
                label._cur_text += delta
                GLib.idle_add(label.set_markup, md_to_pango(label._cur_text))

        final = label._cur_text
        GLib.idle_add(self.conversation_history.append, {"role":"assistant", "content": final})
        GLib.idle_add(self._scroll_bottom)
        GLib.idle_add(self._on_stream_finished)

    def _on_stream_finished(self):
        self._is_streaming = False
        self.send_btn.set_sensitive(True)
        return False

    def _add_row(self, sender: str, text: str, is_user: bool, use_markup: bool):
        content = md_to_pango(text) if use_markup else escape(text)
        row = MessageRow(sender, content, is_user, use_markup=use_markup)
        self.listbox.add(row)
        self.listbox.show_all()
        GLib.idle_add(self._scroll_bottom)

    def _scroll_bottom(self):
        adj = self.scrolled.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        return False
