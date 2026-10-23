# ULTIMATE QUIZ — PC Edition

Jednoduchá desktopová kvízová aplikácia pre Windows. Má vlastné okno, výber slovenčiny alebo češtiny, otázky s možnosťami a výsledné skóre.

## Spustenie zo zdrojového kódu

1. Nainštaluj Python 3.10 alebo novší z https://www.python.org/downloads/
2. Pri inštalácii zaškrtni **Add Python to PATH**.
3. Stiahni alebo naklonuj tento repozitár.
4. Otvor priečinok projektu v termináli a spusti:

```bash
python main.py
```

Aplikácia používa Tkinter, ktorý je súčasťou bežnej Windows inštalácie Pythonu.

## Vytvorenie `.exe`

V termináli v priečinku projektu spusti:

```bash
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --name ULTIMATE-QUIZ --add-data "quizzes.json;." main.py
```

Výsledok nájdeš v priečinku `dist` ako `ULTIMATE-QUIZ.exe`.

**Poznámka:** `quizzes.json` je zdrojový súbor s otázkami. Ak chceš upraviť otázky v budúcej verzii, zmeň ho a vytvor `.exe` znova. Pri zostavení cez PyInstaller sa otázky zabalia do programu.

## Pridávanie otázok

Otvor `quizzes.json`. Každá otázka obsahuje:
- `question` — text otázky
- `answers` — zoznam štyroch odpovedí
- `correct` — index správnej odpovede, od `0` po `3`

Udržuj rovnaký počet a poradie otázok pre oba jazyky, ak chceš porovnateľné kvízy.

## Súbory projektu

- `main.py` — aplikácia a grafické rozhranie
- `quizzes.json` — otázky v slovenčine a češtine
- `requirements.txt` — nástroj na zostavenie `.exe`
- `build.bat` — jednoduché zostavenie pre Windows
- `.gitignore` — ignorované dočasné súbory

## GitHub

Vytvor nový **Public** repozitár s názvom `ultimate-quiz-pc` a nahraj doň súbory z tohto priečinka. Nikdy do repozitára nevkladaj heslá ani súkromné údaje.
