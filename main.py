import json
import random
from pathlib import Path
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

BG = (0.06, 0.09, 0.15, 1)
PANEL = (0.11, 0.15, 0.22, 1)
PURPLE = (0.43, 0.36, 0.99, 1)
WHITE = (0.96, 0.97, 1, 1)
MUTED = (0.70, 0.75, 0.83, 1)
GREEN = (0.05, 0.62, 0.47, 1)
BLUE = (0.14, 0.39, 0.92, 1)

class UltimateQuizApp(App):
    title = 'ULTIMATE QUIZ'

    def build(self):
        Window.clearcolor = BG
        self.data = json.loads((Path(__file__).parent / 'quizzes.json').read_text(encoding='utf-8'))
        self.language = 'sk'
        self.questions = []
        self.index = 0
        self.score = 0
        self.selected = None
        self.root_box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        self.show_start()
        return self.root_box

    def reset_layout(self):
        self.root_box.clear_widgets()

    def add_label(self, text, size=18, color=WHITE, height=None, bold=False):
        lbl = Label(text=text, font_size=dp(size), color=color, size_hint_y=None if height else 1,
                    height=dp(height) if height else 0, bold=bold, halign='center', valign='middle')
        lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0] - dp(8), None)))
        self.root_box.add_widget(lbl)
        return lbl

    def make_button(self, text, callback, color=PURPLE, height=54):
        btn = Button(text=text, size_hint_y=None, height=dp(height), background_normal='',
                     background_color=color, color=WHITE, font_size=dp(17), bold=True)
        btn.bind(on_release=lambda *_: callback())
        self.root_box.add_widget(btn)
        return btn

    def show_start(self):
        self.reset_layout()
        self.add_label('🎯 ULTIMATE QUIZ', 29, (0.65, 0.69, 1, 1), 68, True)
        self.add_label('Otestuj svoje vedomosti!', 17, MUTED, 48)
        self.add_label('Vyber si jazyk kvízu:', 18, WHITE, 46, True)
        self.make_button('🇸🇰  Slovenčina', lambda: self.start_quiz('sk'), GREEN)
        self.make_button('🇨🇿  Čeština', lambda: self.start_quiz('cs'), BLUE)
        self.add_label('8 otázok • Výsledok na konci', 13, MUTED, 42)

    def start_quiz(self, language):
        self.language = language
        self.questions = list(self.data[language]['questions'])
        random.shuffle(self.questions)
        self.index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.reset_layout()
        lang = self.data[self.language]
        if self.index >= len(self.questions):
            self.show_result()
            return
        q = self.questions[self.index]
        self.selected = None
        self.add_label('ULTIMATE QUIZ', 22, (0.65, 0.69, 1, 1), 42, True)
        self.add_label(f"{lang['question_label']} {self.index + 1}/{len(self.questions)}  •  {lang['score_label']}: {self.score}", 14, MUTED, 40)
        self.add_label(q['question'], 21, WHITE, 110, True)
        self.answer_buttons = []
        for i, answer in enumerate(q['answers']):
            btn = ToggleButton(text=answer, group='answers', size_hint_y=None, height=dp(52),
                               background_normal='', background_color=PANEL, color=WHITE,
                               font_size=dp(16), halign='center')
            btn.bind(on_release=lambda inst, ix=i: self.select_answer(ix))
            self.root_box.add_widget(btn)
            self.answer_buttons.append(btn)
        self.make_button('Ďalej →' if self.language == 'sk' else 'Další →', self.check_answer, PURPLE, 56)
        self.make_button('← Späť na výber' if self.language == 'sk' else '← Zpět na výběr', self.show_start, PANEL, 46)

    def select_answer(self, index):
        self.selected = index
        for i, btn in enumerate(self.answer_buttons):
            btn.state = 'down' if i == index else 'normal'
            btn.background_color = PURPLE if i == index else PANEL

    def check_answer(self):
        if self.selected is None:
            self.add_label('Najprv vyber jednu odpoveď.' if self.language == 'sk' else 'Nejdřív vyber jednu odpověď.', 14, (1, 0.7, 0.35, 1), 34)
            return
        if self.selected == self.questions[self.index]['correct']:
            self.score += 1
        self.index += 1
        self.show_question()

    def show_result(self):
        self.reset_layout()
        lang = self.data[self.language]
        total = len(self.questions)
        percent = round(self.score / total * 100) if total else 0
        self.add_label('🏆 ' + lang['result_title'], 27, (0.65, 0.69, 1, 1), 80, True)
        self.add_label(f'{self.score} / {total}', 40, WHITE, 80, True)
        self.add_label(f'{percent}%', 27, (0.20, 0.85, 0.60, 1), 60, True)
        self.add_label(lang['result_message'], 16, MUTED, 90)
        self.make_button(lang['play_again'], self.show_start, PURPLE)

if __name__ == '__main__':
    UltimateQuizApp().run()
