from pathlib import Path
import re

WORDS_DIR = Path("../words")
OUTPUT_FILE = Path("../words_export.txt")

WORD_PATTERN = re.compile(r"^-\s\[(?P<checked>[ xX])\]\s+\d+\.\s+(?P<word>.+)$")

all_words = []
known_words = []
unknown_words = []

files = sorted(
    WORDS_DIR.glob("*.md"),
    key=lambda f: int(re.search(r"\d+", f.stem).group())
)

for file in files:
    with file.open("r", encoding="utf-8") as f:
        for line in f:
            match = WORD_PATTERN.match(line.strip())

            if not match:
                continue

            checked = match.group("checked").lower()
            word = match.group("word").strip()

            all_words.append(word)

            if checked == "x":
                known_words.append(word)
            else:
                unknown_words.append(word)

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    f.write("=== ALL WORDS ===\n")
    f.write(", ".join(all_words) + "\n\n")

    f.write("=== UNKNOWN WORDS ===\n")
    f.write(", ".join(unknown_words) + "\n\n")

    f.write("=== KNOWN WORDS ===\n")
    f.write(", ".join(known_words) + "\n")

print(f"Total de palavras: {len(all_words)}")
print(f"Conhecidas: {len(known_words)}")
print(f"Desconhecidas: {len(unknown_words)}")
print(f"Arquivo gerado: {OUTPUT_FILE}")