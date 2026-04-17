import tkinter as tk
import random
import json
import os

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game Pro")
        self.root.geometry("950x650")

        self.theme = {"bg": "#0f172a", "card": "#1e293b"}

        self.btn_style = {
            "font": ("Segoe UI", 13, "bold"),
            "width": 25,
            "height": 2,
            "bd": 0,
            "fg": "white",
            "cursor": "hand2"
        }

        
        self.questions_data = self.load_questions()

        self.root.configure(bg=self.theme["bg"])
        self.main_frame = tk.Frame(root, bg=self.theme["bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.card = tk.Frame(self.main_frame, bg=self.theme["card"])
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=750, height=550)

        self.menu()

    
    def load_questions(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "questions.json")

        with open(file_path, "r") as f:
            return json.load(f)

   
    def save_score(self, name, score):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "scores.json")

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append({"name": name, "score": score})
        data = sorted(data, key=lambda x: x["score"], reverse=True)[:5]

        with open(file_path, "w") as f:
            json.dump(data, f)

    def clear(self):
        for w in self.card.winfo_children():
            w.destroy()

    def hover(self, btn):
        btn.bind("<Enter>", lambda e: btn.config(bg="#475569"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#334155"))

    def menu(self):
        self.clear()

        tk.Label(self.card, text="QUIZ GAME PRO",
                 font=("Segoe UI", 28, "bold"),
                 fg="#38bdf8", bg=self.theme["card"]).pack(pady=20)

        self.name_entry = tk.Entry(self.card, font=("Segoe UI", 14))
        self.name_entry.insert(0, "Enter your name")
        self.name_entry.pack(pady=10)

        self.category = tk.StringVar(value="Programming")
        self.difficulty = tk.StringVar(value="easy")

        frame = tk.Frame(self.card, bg=self.theme["card"])
        frame.pack(pady=10)

        for cat in ["Programming", "Aptitude", "GK", "DSA"]:
            tk.Radiobutton(frame, text=cat, variable=self.category,
                           value=cat, bg=self.theme["card"],
                           fg="white", selectcolor=self.theme["card"]).pack(side="left", padx=10)

        frame2 = tk.Frame(self.card, bg=self.theme["card"])
        frame2.pack(pady=10)

        for lvl in ["easy", "medium", "hard"]:
            tk.Radiobutton(frame2, text=lvl, variable=self.difficulty,
                           value=lvl, bg=self.theme["card"],
                           fg="white", selectcolor=self.theme["card"]).pack(side="left", padx=10)

        btn = tk.Button(self.card, text="Start Game",
                        command=self.start, bg="#334155", **self.btn_style)
        btn.pack(pady=10)
        self.hover(btn)

    def start(self):
        self.player = self.name_entry.get()
        self.current_q = 0
        self.score = 0
        self.time_left = 10

        pool = self.questions_data[self.category.get()][self.difficulty.get()]
        self.questions = random.sample(pool, min(10, len(pool)))

        self.load_question()

    def start_timer(self):
        if self.time_left > 0:
            color = "#22c55e" if self.time_left > 5 else "#ef4444"
            self.timer.config(text=f"⏱ {self.time_left}s", fg=color)
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            self.next_question()

    def load_question(self):
        self.clear()

        if self.current_q >= len(self.questions):
            return self.result()

        self.time_left = 10
        q = self.questions[self.current_q]
        random.shuffle(q["opt"])

        tk.Label(self.card,
                 text=f"{self.player} | Q {self.current_q+1}/{len(self.questions)}",
                 font=("Segoe UI", 12),
                 fg="#94a3b8", bg=self.theme["card"]).pack()

        tk.Label(self.card, text=q["q"],
                 font=("Segoe UI", 20, "bold"),
                 fg="white", bg=self.theme["card"],
                 wraplength=650).pack(pady=20)

        self.timer = tk.Label(self.card, text="", font=("Segoe UI", 14),
                              bg=self.theme["card"])
        self.timer.pack()

        for opt in q["opt"]:
            btn = tk.Button(self.card, text=opt,
                            command=lambda o=opt: self.check_answer(o),
                            bg="#334155", **self.btn_style)
            btn.pack(pady=5)
            self.hover(btn)

        self.start_timer()

    def check_answer(self, selected):
        correct = self.questions[self.current_q]["ans"]

        self.clear()

        if selected == correct:
            self.score += 1
            msg = " Correct!"
            color = "#22c55e"
        else:
            msg = f" Wrong!\nCorrect: {correct}"
            color = "#ef4444"

        tk.Label(self.card, text=msg,
                 font=("Segoe UI", 18, "bold"),
                 fg=color, bg=self.theme["card"]).pack(pady=40)

        self.root.after(1500, self.next_question)

    def next_question(self):
        self.current_q += 1
        self.load_question()

    def result(self):
        self.clear()

        self.save_score(self.player, self.score)

        tk.Label(self.card,
                 text=f"🎉 {self.player}, Score: {self.score}/{len(self.questions)}",
                 font=("Segoe UI", 22, "bold"),
                 fg="#38bdf8", bg=self.theme["card"]).pack(pady=20)

        tk.Label(self.card, text="🏆 Leaderboard",
                 font=("Segoe UI", 16, "bold"),
                 fg="white", bg=self.theme["card"]).pack()

        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "scores.json")

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                for s in data:
                    tk.Label(self.card,
                             text=f"{s['name']} - {s['score']}",
                             fg="white", bg=self.theme["card"]).pack()
        except:
            pass

        btn = tk.Button(self.card, text="Play Again",
                        command=self.menu, bg="#334155", **self.btn_style)
        btn.pack(pady=20)
        self.hover(btn)


root = tk.Tk()
app = QuizGame(root)
root.mainloop()
