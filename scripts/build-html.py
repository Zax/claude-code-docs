#!/usr/bin/env python3
"""
Genera un singolo file HTML dalla documentazione Markdown.
Uso: python3 scripts/build-html.py
Richiede: pandoc (brew install pandoc)
"""

import re
import subprocess
import sys
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "claude-code-docs.html"
TEMPLATE = Path(__file__).parent / "template.html"
CSS = Path(__file__).parent / "style.css"

NAV_PATTERN = re.compile(r'^←\s|^\[←\s')


def check_pandoc():
    if subprocess.run(['which', 'pandoc'], capture_output=True).returncode != 0:
        print("Errore: pandoc non trovato. Installa con: brew install pandoc")
        sys.exit(1)


def strip_nav_lines(content: str) -> str:
    """Rimuove righe di navigazione e separatori adiacenti."""
    lines = content.splitlines()

    if lines and NAV_PATTERN.match(lines[0]):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)

    if lines and NAV_PATTERN.match(lines[-1]):
        lines.pop()
    while lines and not lines[-1].strip():
        lines.pop()
    if lines and lines[-1].strip() == '---':
        lines.pop()
    while lines and not lines[-1].strip():
        lines.pop()

    return '\n'.join(lines)


def get_file_order() -> list:
    """Estrae l'ordine dei file dall'indice del README."""
    content = (ROOT / "README.md").read_text(encoding='utf-8')
    # Solo le voci numerate dell'indice (es. "1. [Titolo](docs/file.md)")
    files = re.findall(r'^\d+\.\s+\[.*?\]\(docs/([^)]+\.md)\)', content, re.MULTILINE)
    result = []
    for f in files:
        result.append(ROOT / "docs" / f)
        # Dopo plugin.md aggiungi le pagine dei singoli plugin in ordine
        if f == 'plugin.md':
            plugin_dir = ROOT / "docs" / "plugin"
            for sub in sorted(plugin_dir.glob('*.md')):
                result.append(sub)
    return result


def main():
    check_pandoc()

    sections = []
    for f in get_file_order():
        if f.exists():
            cleaned = strip_nav_lines(f.read_text(encoding='utf-8'))
            if cleaned:
                sections.append(cleaned)
        else:
            print(f"Avviso: file non trovato: {f}")

    combined = '\n\n---\n\n'.join(sections)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md',
                                     delete=False, encoding='utf-8') as tmp:
        tmp.write(combined)
        tmp_path = tmp.name

    try:
        subprocess.run([
            'pandoc', tmp_path,
            '--standalone',
            '--toc', '--toc-depth=3',
            '--from=gfm',
            '--to=html5',
            f'--template={TEMPLATE}',
            f'--css={CSS}',
            '--embed-resources',
            '--metadata=title:Claude Code - Knowledge Base',
            '-o', str(OUTPUT),
        ], check=True, cwd=ROOT)
        size_kb = OUTPUT.stat().st_size // 1024
        print(f"✓ Generato: {OUTPUT.name} ({size_kb} KB)")
    finally:
        os.unlink(tmp_path)


if __name__ == '__main__':
    main()
