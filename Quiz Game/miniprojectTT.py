import tkinter as tk
import random

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game Pro")
        self.root.geometry("950x650")

        self.current_q = 0
        self.score = 0
        self.current_questions = []
        self.current_level = "easy"

        # TIMER
        self.time_left = 10
        self.timer_label = None

        self.theme = {"bg": "#0f172a", "card": "#1e293b"}

        self.btn_style = {
            "font": ("Arial", 13, "bold"),
            "width": 22,
            "height": 2,
            "bd": 0,
            "fg": "white",
            "activebackground": "#475569"
        }

        self.questions_data = {

    "easy": [
        {"q": "What is the sum of 2 + 2?", "opt": ["3", "4", "5", "6"], "ans": "4", "hint": "Basic addition"},
        {"q": "What is the capital of India?", "opt": ["Delhi", "Mumbai", "Chennai", "Kolkata"], "ans": "Delhi", "hint": "Starts with D"},
        {"q": "What is 5 - 3?", "opt": ["1", "2", "3", "4"], "ans": "2", "hint": "Subtraction"},
        {"q": "What color is the sky?", "opt": ["Blue", "Green", "Red", "Yellow"], "ans": "Blue", "hint": "Look up"},
        {"q": "3 × 3 = ?", "opt": ["6", "9", "12", "3"], "ans": "9", "hint": "Multiplication"}
    ],

    "medium": [
        {"q": "What is 5 × 6?", "opt": ["30", "25", "20", "35"], "ans": "30", "hint": "Multiply"},
        {"q": "What is Python?", "opt": ["Snake", "Programming Language", "Game", "OS"], "ans": "Programming Language", "hint": "Coding"},
        {"q": "10 ÷ 2 = ?", "opt": ["2", "3", "5", "10"], "ans": "5", "hint": "Division"},
        {"q": "HTML stands for?", "opt": ["Hyper Text Markup Language", "Other"], "ans": "Hyper Text Markup Language", "hint": "Web"},
        {"q": "Square of 4?", "opt": ["8", "16", "12", "10"], "ans": "16", "hint": "4 × 4"}
    ],

    "hard": [
        {"q": "Binary of 10?", "opt": ["1010", "1001", "1111", "1100"], "ans": "1010", "hint": "Base 2"},
        {"q": "OOP stands for?", "opt": ["Object Oriented Programming", "Other"], "ans": "Object Oriented Programming", "hint": "Concept"},
        {"q": "2⁵ = ?", "opt": ["32", "16", "25", "10"], "ans": "32", "hint": "Power"},
        {"q": "RAM stands for?", "opt": ["Random Access Memory", "Other"], "ans": "Random Access Memory", "hint": "Memory"},
        {"q": "CPU stands for?", "opt": ["Central Processing Unit", "Other"], "ans": "Central Processing Unit", "hint": "Brain"}
    ]
}
        self.root.configure(bg=self.theme["bg"])

        self.main_frame = tk.Frame(root, bg=self.theme["bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.card = tk.Frame(self.main_frame, bg=self.theme["card"])
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=750, height=550)

        self.menu()

    def clear(self):
        for w in self.card.winfo_children():
            w.destroy()

    def exit_app(self):
        self.root.destroy()

    def menu(self):
        self.clear()

        tk.Label(self.card, text="QUIZ GAME",
                 font=("Arial", 28, "bold"),
                 fg="white", bg=self.theme["card"]).pack(pady=25)

        self.difficulty = tk.StringVar(value="easy")

        frame = tk.Frame(self.card, bg=self.theme["card"])
        frame.pack(pady=15)

        for lvl in ["easy", "medium", "hard"]:
            tk.Radiobutton(frame, text=lvl.capitalize(),
                           variable=self.difficulty, value=lvl,
                           font=("Arial", 12, "bold"),
                           bg=self.theme["card"], fg="white",
                           selectcolor=self.theme["card"]).pack(side="left", padx=15)

        tk.Button(self.card, text="Start Game",
                  command=lambda: self.start(self.difficulty.get()),
                  bg="#3b82f6", **self.btn_style).pack(pady=12)

        tk.Button(self.card, text="Exit",
                  command=self.exit_app,
                  bg="#ef4444", **self.btn_style).pack(pady=8)

    def start(self, level):
        self.current_level = level
        self.current_q = 0
        self.score = 0
        self.current_questions = random.sample(
            self.questions_data[level],
            len(self.questions_data[level])
        )
        self.load()

    # TIMER FUNCTION
    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            self.current_q += 1
            self.load()

    def load(self):
        self.clear()

        if self.current_q < len(self.current_questions):
            self.time_left = 10  # reset timer

            q = self.current_questions[self.current_q]

            tk.Label(self.card, text=q["q"],
                     font=("Arial", 20, "bold"),
                     fg="white", bg=self.theme["card"],
                     wraplength=650, justify="center").pack(pady=25)

            # TIMER LABEL (ONLY ADDITION)
            self.timer_label = tk.Label(self.card,
                                       text="Time Left: 10s",
                                       font=("Arial", 14, "bold"),
                                       fg="red",
                                       bg=self.theme["card"])
            self.timer_label.pack(pady=5)

            for opt in q["opt"]:
                tk.Button(self.card, text=opt,
                          command=lambda o=opt: self.answer(o),
                          bg="#334155", **self.btn_style).pack(pady=6)

            # ORIGINAL CONTROL FRAME (UNCHANGED)
            control = tk.Frame(self.card, bg=self.theme["card"])
            control.pack(pady=15)

            tk.Button(control, text="Hint",
                      command=lambda: self.show_hint(q),
                      bg="#f59e0b", **self.btn_style).pack(side="left", padx=10)

            tk.Button(control, text="Restart",
                      command=lambda: self.start(self.current_level),
                      bg="#3b82f6", **self.btn_style).pack(side="left", padx=10)

            tk.Button(control, text="⬅ Back",
                      command=self.menu,
                      bg="#64748b", **self.btn_style).pack(side="left", padx=10)

            tk.Button(control, text="Exit",
                      command=self.exit_app,
                      bg="#ef4444", **self.btn_style).pack(side="left", padx=10)

            self.start_timer()  # start timer

        else:
            self.result()

    def answer(self, selected):
        self.time_left = 0  # stop timer

        if selected == self.current_questions[self.current_q]["ans"]:
            self.score += 1

        self.current_q += 1
        self.load()

    def show_hint(self, q):
        tk.Label(self.card, text=" " + q["hint"],
                 font=("Arial", 12),
                 fg="yellow", bg=self.theme["card"]).pack(pady=5)

    def result(self):
        self.clear()

        tk.Label(self.card,
                 text=f"Score: {self.score}/{len(self.current_questions)}",
                 font=("Arial", 22, "bold"),
                 fg="#22c55e", bg=self.theme["card"]).pack(pady=30)

        btn_frame = tk.Frame(self.card, bg=self.theme["card"])
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Restart",
                  command=lambda: self.start(self.current_level),
                  bg="#22c55e", **self.btn_style).pack(pady=6)

        tk.Button(btn_frame, text="Menu",
                  command=self.menu,
                  bg="#3b82f6", **self.btn_style).pack(pady=6)

        tk.Button(btn_frame, text="⬅ Back",
                  command=self.menu,
                  bg="#64748b", **self.btn_style).pack(pady=6)

        tk.Button(btn_frame, text="Exit",
                  command=self.exit_app,
                  bg="#ef4444", **self.btn_style).pack(pady=6)


root = tk.Tk()
app = QuizGame(root)
root.mainloop()
