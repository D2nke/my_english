#!/usr/bin/env python3
"""
Conta quantos itens do checklist estao marcados ([x]) e atualiza
o badge de progresso no arquivo de palavras e no README.md.
"""

import re
from pathlib import Path

CHECKLIST_FILE = Path("words/1000-palavras-mais-comuns-ingles.md")
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
    return f"![Progresso](https://img.shields.io/badge/palavras%20aprendidas-{checked}%2F{total}-{color})"


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
    if not CHECKLIST_FILE.exists():
        print(f"Arquivo nao encontrado: {CHECKLIST_FILE}")
        return

    text = CHECKLIST_FILE.read_text(encoding="utf-8")
    checked, total = count_progress(text)
    badge_md = build_badge(checked, total)

    changed_checklist = update_file(CHECKLIST_FILE, badge_md)
    changed_readme = update_file(README_FILE, badge_md)

    pct = round((checked / total * 100), 1) if total else 0
    print(f"Progresso: {checked}/{total} ({pct}%)")
    print(f"Checklist atualizado: {changed_checklist}")
    print(f"README atualizado: {changed_readme}")


if __name__ == "__main__":
    main()
