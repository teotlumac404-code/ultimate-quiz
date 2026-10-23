import json
import random
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path


APP_NAME = "ULTIMATE QUIZ"


def app_dir():
    """Folder containing the app files, including when bundled by PyInstaller."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def load_quizzes():
    data_file = app_dir() / "quizzes.json"
    if not data_file.exists():
        # PyInstaller may bundle the data file inside the executable folder.
        bundled = Path(getattr(sys, "_MEIPASS", app_dir())) / "quizzes.json"
        data_file = bundled
    with data_file.open("r", encoding="utf-8") as f:
        return json.load(f)


class UltimateQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("760x560")
        self.root.minsize(620, 480)
        self.root.configure(bg="#101827")

        self.data = load_quizzes()
        self.language = "sk"
        self.questions = []
        self.index = 0
        self.score = 0
        self.selected = tk.StringVar(value="")

        self.build_start_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def label(self, parent, text, size=12, color="#f8fafc", bold=False, **kwargs):
        return tk.Label(
            parent, text=text, font=("Segoe UI", size, "bold" if bold else "normal"),
            fg=color, bg=kwargs.pop("bg", "#101827"), wraplength=680,
            justify=kwargs.pop("justify", "center"), **kwargs
        )

    def button(self, parent, text, command, bg="#6d5dfc", **kwargs):
        return tk.Button(
            parent, text=text, command=command, font=("Segoe UI", 12, "bold"),
            fg="#ffffff", bg=bg, activebackground="#5144d8",
            activeforeground="#ffffff", relief="flat", bd=0, padx=18, pady=11,
            cursor="hand2", **kwargs
        )

    def build_start_screen(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#101827", padx=30, pady=28)
        frame.pack(fill="both", expand=True)

        self.label(frame, "🎯 ULTIMATE QUIZ", 28, "#a5b4fc", True).pack(pady=(14, 8))
        self.label(frame, "Otestuj svoje vedomosti!", 15, "#cbd5e1").pack(pady=(0, 26))
        self.label(frame, "Vyber si jazyk kvízu:", 13, "#f8fafc", True).pack(pady=(0, 12))

        row = tk.Frame(frame, bg="#101827")
        row.pack()
        self.button(row, "🇸🇰 Slovenčina", lambda: self.start_quiz("sk"), bg="#0f9f78").pack(side="left", padx=8)
        self.button(row, "🇨🇿 Čeština", lambda: self.start_quiz("cs"), bg="#2563eb").pack(side="left", padx=8)

        self.label(
            frame,
            "Vyber jazyk a odpovedaj na otázky. Na konci uvidíš svoj výsledok.",
            11, "#94a3b8"
        ).pack(pady=28)
        self.label(frame, "ULTIMATE QUIZ • PC Edition", 9, "#64748b").pack(side="bottom", pady=(20, 0))

    def start_quiz(self, language):
        self.language = language
        self.questions = list(self.data[language]["questions"])
        random.shuffle(self.questions)
        self.index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear()
        lang_data = self.data[self.language]
        if self.index >= len(self.questions):
            self.show_result()
            return

        q = self.questions[self.index]
        frame = tk.Frame(self.root, bg="#101827", padx=32, pady=24)
        frame.pack(fill="both", expand=True)

        self.label(frame, "ULTIMATE QUIZ", 20, "#a5b4fc", True).pack(pady=(0, 8))
        self.label(
            frame,
            f"{lang_data['question_label']} {self.index + 1}/{len(self.questions)}    •    {lang_data['score_label']}: {self.score}",
            11, "#94a3b8"
        ).pack(pady=(0, 22))

        self.label(frame, q["question"], 18, "#f8fafc", True).pack(pady=(0, 22))

        self.selected = tk.StringVar(value="")
        for i, answer in enumerate(q["answers"]):
            rb = tk.Radiobutton(
                frame, text=answer, variable=self.selected, value=str(i),
                font=("Segoe UI", 12), fg="#f8fafc", bg="#1e293b",
                selectcolor="#4338ca", activebackground="#1e293b",
                activeforeground="#ffffff", anchor="w", padx=14, pady=10,
                wraplength=620, indicatoron=False, relief="flat", bd=0,
                cursor="hand2"
            )
            rb.pack(fill="x", pady=5)

        bottom = tk.Frame(frame, bg="#101827")
        bottom.pack(fill="x", pady=(22, 0))
        self.button(bottom, lang_data["back"], self.build_start_screen, bg="#475569").pack(side="left")
        self.button(bottom, lang_data["next"], self.check_answer).pack(side="right")

    def check_answer(self):
        chosen = self.selected.get()
        lang_data = self.data[self.language]
        if chosen == "":
            messagebox.showinfo(lang_data["notice_title"], lang_data["choose_answer"])
            return

        q = self.questions[self.index]
        if int(chosen) == q["correct"]:
            self.score += 1
        self.index += 1
        self.show_question()

    def show_result(self):
        self.clear()
        lang_data = self.data[self.language]
        total = len(self.questions)
        percent = round((self.score / total) * 100) if total else 0

        frame = tk.Frame(self.root, bg="#101827", padx=30, pady=35)
        frame.pack(fill="both", expand=True)
        self.label(frame, "🏆 " + lang_data["result_title"], 25, "#a5b4fc", True).pack(pady=(25, 18))
        self.label(frame, f"{self.score} / {total}", 34, "#f8fafc", True).pack(pady=5)
        self.label(frame, f"{percent}%", 20, "#34d399", True).pack(pady=5)
        self.label(frame, lang_data["result_message"], 13, "#cbd5e1").pack(pady=(10, 26))
        self.button(frame, lang_data["play_again"], self.build_start_screen).pack()
        self.label(frame, "ULTIMATE QUIZ • PC Edition", 9, "#64748b").pack(side="bottom", pady=(20, 0))


if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateQuizApp(root)
    root.mainloop()
