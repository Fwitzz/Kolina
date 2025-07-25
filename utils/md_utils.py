import re

def escape(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

# ```lang\ncode...```  (language is optional)
_BLOCK_RE = re.compile(r'```(?:([^\n`]+)\n)?(.*?)```', re.DOTALL)
_INLINE_CODE_RE = re.compile(r'`([^`\n]+)`')
_HEADING_RE = re.compile(r'^(#{1,3})\s*(.+)$', re.MULTILINE)
_BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
_LINK_RE = re.compile(r'\[([^\]]+)\]\([^\)]+\)')
_LIST_RE = re.compile(r'(?m)^[ \t]*[-*]\s+')

def _process_inline(text: str) -> str:
    s = escape(text)

    # Headings
    def heading_sub(m):
        level = len(m.group(1))
        content = escape(m.group(2))
        size = {1: "18000", 2: "16000", 3: "14000"}.get(level, "12000")
        return f'<span weight="bold" size="{size}">{content}</span>'
    s = _HEADING_RE.sub(heading_sub, s)

    # Bold
    s = _BOLD_RE.sub(r'<b>\1</b>', s)

    # Inline code
    def inline_code_sub(m):
        code = escape(m.group(1))
        return (f'<span font_family="monospace" background="#eeeeee" '
                f'foreground="#333333">{code}</span>')
    s = _INLINE_CODE_RE.sub(inline_code_sub, s)

    # Links -> display text only
    s = _LINK_RE.sub(r'\1', s)

    # Bulleted lists
    s = _LIST_RE.sub('• ', s)

    return s

def md_to_pango(text: str) -> str:
    """
    Minimal Markdown -> Pango conversion supporting:
    - headings (#, ##, ###)
    - **bold**
    - inline code `code`
    - fenced blocks ```lang ... ```
    - bullet lists (- or *)
    - links [text](url) -> text
    """
    out = []
    last = 0
    for m in _BLOCK_RE.finditer(text):
        # Text before block: inline processing
        out.append(_process_inline(text[last:m.start()]))
        code_body = m.group(2)  # actual code
        code_markup = (f'<span font_family="monospace" background="#eeeeee" '
                       f'foreground="#333333">{escape(code_body.rstrip())}</span>')
        out.append(code_markup)
        last = m.end()

    out.append(_process_inline(text[last:]))  # tail
    return ''.join(out)
