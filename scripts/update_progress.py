#!/usr/bin/env python3
"""
Conta quantos itens do checklist estão marcados ([x]) em todos os arquivos .md
da pasta 'words/' e atualiza o badge de progresso neles e no README.md.
"""

import re
from pathlib import Path

WORDS_DIR = Path("words")
README_FILE = Path("README.md")

BADGE_PATTERN = re.compile(
    r"!\[Progress\]\(https://img\.shields\.io/badge/words%20learned-\d+%2F\d+-\w+\)"
)

def count_progress(text: str) -> tuple[int, int]:
    checked = len(re.findall(r"- \[[xX]\]", text))
    total = len(re.findall(r"- \[[ xX]\]", text))
    return checked, total


def badge_color(pct: float) -> str:
    if pct >= 100:
        return "brightgreen"
    if pct >= 66:
        return "green"
    if pct >= 33:
        return "yellow"
    return "red"


def build_badge(checked: int, total: int) -> str:
    pct = (checked / total * 100) if total else 0
    color = badge_color(pct)
    return f"![Progress](https://img.shields.io/badge/words%20learned-{checked}%2F{total}-{color})"


def update_file(path: Path, badge_md: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    new_text = BADGE_PATTERN.sub(badge_md, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    if not WORDS_DIR.is_dir():
        print(f"Directory not found: {WORDS_DIR}")
        return

    # Busca todos os arquivos .md dentro da pasta words/
    md_files = list(WORDS_DIR.glob("*.md"))
    
    if not md_files:
        print(f"No .md files found in {WORDS_DIR}")
        return

    total_checked = 0
    total_items = 0

    # Primeiro passo: acumular o progresso de todos os arquivos
    for file_path in md_files:
        text = file_path.read_text(encoding="utf-8")
        checked, total = count_progress(text)
        total_checked += checked
        total_items += total

    # Gera o badge baseado no total acumulado
    badge_md = build_badge(total_checked, total_items)

    # Segundo passo: atualizar o badge em todos os arquivos .md de words/
    print("Updating checklist files:")
    for file_path in md_files:
        changed = update_file(file_path, badge_md)
        print(f"  - {file_path.name}: {'Updated' if changed else 'No changes'}")

    # Atualiza o README.md
    changed_readme = update_file(README_FILE, badge_md)
    print(f"README update: {'Updated' if changed_readme else 'No changes'}")

    pct = round((total_checked / total_items * 100), 1) if total_items else 0
    print(f"\nGlobal Progress: {total_checked}/{total_items} ({pct}%)")


if __name__ == "__main__":
    main()