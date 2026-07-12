from pathlib import Path
import re

# Pasta onde estão os arquivos
WORDS_DIR = Path("words")

# Expressão para encontrar linhas do tipo:
# - [ ] 123. idea
# - [x] 456. information
WORD_PATTERN = re.compile(r"^(\s*-\s\[[ xX]\]\s+\d+\.\s+)(.+)$")

seen_words = set()

# Ordena pelos números do nome do arquivo
files = sorted(
    WORDS_DIR.glob("*.md"),
    key=lambda f: int(re.search(r"\d+", f.stem).group())
)

for file in files:
    print(f"Processando {file.name}...")

    output = []

    with file.open("r", encoding="utf-8") as f:
        for line in f:
            match = WORD_PATTERN.match(line)

            if not match:
                output.append(line)
                continue

            prefix, word = match.groups()

            # comparação sem diferenciar maiúsculas/minúsculas
            normalized = word.strip().lower()

            if normalized in seen_words:
                # Palavra repetida -> ignora
                print(f"  Removida: {word}")
                continue

            seen_words.add(normalized)
            output.append(line)

    with file.open("w", encoding="utf-8") as f:
        f.writelines(output)

print("\nConcluído!")