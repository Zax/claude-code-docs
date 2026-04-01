#!/usr/bin/env python3
"""
Genera un singolo file HTML dalla documentazione Markdown.
Uso: python3 scripts/build-html.py
"""

import re
import sys
from pathlib import Path

try:
    import markdown
    from markdown.extensions.toc import TocExtension
except ImportError:
    print("Errore: modulo 'markdown' non trovato.")
    print("Installa con: pip3 install markdown")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "claude-code-docs.html"
CSS_FILE = Path(__file__).parent / "style.css"

NAV_PATTERN = re.compile(r'^←\s|^\[←\s')


def strip_nav_lines(content: str) -> str:
    """Rimuove le righe di navigazione e i separatori finali."""
    lines = content.splitlines()

    # Rimuovi nav line iniziale e blank lines seguenti
    if lines and NAV_PATTERN.match(lines[0]):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)

    # Rimuovi nav line finale
    if lines and NAV_PATTERN.match(lines[-1]):
        lines.pop()
    # Rimuovi blank lines finali
    while lines and not lines[-1].strip():
        lines.pop()
    # Rimuovi eventuale hr finale
    if lines and lines[-1].strip() == '---':
        lines.pop()
    while lines and not lines[-1].strip():
        lines.pop()

    return '\n'.join(lines)


def get_file_order() -> list:
    """Estrae l'ordine dei file dall'indice del README."""
    readme = ROOT / "README.md"
    content = readme.read_text(encoding='utf-8')
    files = re.findall(r'\(docs/([^)]+\.md)\)', content)
    return [ROOT / "docs" / f for f in files]


def main():
    files = get_file_order()
    sections = []

    for f in files:
        if f.exists():
            content = f.read_text(encoding='utf-8')
            cleaned = strip_nav_lines(content)
            if cleaned:
                sections.append(cleaned)
        else:
            print(f"Avviso: file non trovato: {f}")

    combined = '\n\n---\n\n'.join(sections)

    css = CSS_FILE.read_text(encoding='utf-8') if CSS_FILE.exists() else ""

    md = markdown.Markdown(extensions=[
        TocExtension(toc_depth=3),
        'tables',
        'fenced_code',
        'attr_list',
    ])
    body = md.convert(combined)
    toc = md.toc

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claude Code - Knowledge Base</title>
  <style>
{css}
  </style>
</head>
<body>
  <header>
    <h1>Claude Code - Knowledge Base</h1>
    <p class="subtitle">Documentazione personale sull'uso di Claude Code</p>
  </header>
  <nav id="toc">
    <strong>Indice</strong>
    {toc}
  </nav>
  <main>
{body}
  </main>
</body>
</html>"""

    OUTPUT.write_text(html, encoding='utf-8')
    size_kb = OUTPUT.stat().st_size // 1024
    print(f"✓ Generato: {OUTPUT.name} ({size_kb} KB)")


if __name__ == '__main__':
    main()
