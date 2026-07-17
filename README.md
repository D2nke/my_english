# 📚 3000+ Most Common English Words — Checklist

A personal project to track my English vocabulary progress by checking off which of the 5000 most frequent words I already know.

![Progress](https://img.shields.io/badge/words%20learned-1747%2F3729-yellow)

## How it works

- The complete checklist is divided into multiple files inside the [`words/`](words/) directory, with words ordered by usage frequency.
- Mark `- [x]` next to the words you already know (directly on GitHub by clicking the rendered checkbox, or by editing the file).
- On every `push` to any branch other than `main`/`master`, a GitHub Action automatically counts the checked items and updates the progress badge above and inside the checklist files themselves.

## Suggested workflow

1. Create a branch (e.g., `git checkout -b progress`).
2. Check off the words you already know in the checklist files.
3. Commit and push your branch.
4. The Action runs automatically, recalculates your progress, and commits the updated badges.
5. Whenever you're ready, open a Pull Request to `main` to consolidate your progress.

## Project structure

```
.
├── README.md
├── words/
│   ├── 0-1000.md                             # 0 to 1000 words checklist
│   ├── 1000-2000.md                          # 1000 to 2000 words checklist
│   ├── 2000-3000.md                          # 2000 to 3000 words checklist
│   ├── 3000-4000.md                          # 3000 to 4000 words checklist
│   └── 4000-5000.md                          # 4000 to 5000 words checklist
├── scripts/
│   └── update_progress.py                    # recalculates the progress badge
└── .github/
    └── workflows/
        └── update-progress.yml               # runs the script on every push outside main/master
```

## List source

Frequency list derived from [google-10000-english](https://github.com/first20hours/google-10000-english), based on n-gram analysis of the Google corpus.