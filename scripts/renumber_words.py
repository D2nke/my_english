from pathlib import Path
import re
import shutil

WORDS_DIR = Path("../words")
BACKUP_DIR = Path("words_backup_global")

BACKUP_DIR.mkdir(exist_ok=True)

WORD_PATTERN = re.compile(r"^(\s*-\s\[([ xX])\]\s+)\d+\.\s+(.+)$")

files = sorted(
    WORDS_DIR.glob("*.md"),
    key=lambda f: int(re.search(r"\d+", f.stem).group())
)

# ==========================================================
# Backup
# ==========================================================

for file in files:
    shutil.copy2(file, BACKUP_DIR / file.name)

# ==========================================================
# Leitura
# ==========================================================

all_words = []
headers = []

for file in files:

    header = []
    reading_words = False

    with file.open("r", encoding="utf-8") as f:

        for line in f:

            match = WORD_PATTERN.match(line)

            if match:
                reading_words = True
                _, checked, word = match.groups()
                all_words.append((checked, word))
            else:
                if not reading_words:
                    header.append(line)

    headers.append(header)

all_words.sort(key=lambda x: x[0].lower() != "x")

# ==========================================================
# Escrita
# ==========================================================

TOTAL = len(all_words)

print("=" * 60)
print("REORGANIZANDO ARQUIVOS")
print("=" * 60)

index = 0

for file_index, file in enumerate(files):

    start = index
    end = min(index + 1000, TOTAL)

    if start >= TOTAL:
        # Remove arquivos que ficaram vazios
        file.unlink()
        print(f"{file.name:<20} removido (vazio)")
        continue

    with file.open("w", encoding="utf-8") as f:

        # Cabeçalho original
        f.writelines(headers[file_index])

        # Palavras
        for number, (checked, word) in enumerate(
            all_words[start:end],
            start=start + 1
        ):
            f.write(f"- [{checked}] {number}. {word}\n")

    print(
        f"{file.name:<20} "
        f"{end-start:>4} palavras "
        f"({start+1} → {end})"
    )

    index += 1000

print("=" * 60)
print(f"TOTAL DE PALAVRAS: {TOTAL}")
print("=" * 60)
print(f"Backup criado em: {BACKUP_DIR}")