import tkinter as tk
from tkinter import messagebox
from collections import deque

graph = {
    "Fever": ["Flu", "COVID"],
    "Cough": ["Flu", "COVID"],
    "Headache": ["Migraine", "Flu"],
    "Fatigue": ["COVID"],
    "Body Pain": ["Flu"],
    "Cold": ["Flu"],
    "Flu": [],
    "COVID": [],
    "Migraine": []
}

disease_info = {
    "Flu": {
        "desc": "A common viral infection causing fever, cold, and body pain.",
        "precautions": "Rest, drink fluids, take paracetamol, avoid cold exposure."
    },
    "COVID": {
        "desc": "A contagious respiratory disease caused by coronavirus.",
        "precautions": "Wear mask, isolate, sanitize hands, consult doctor."
    },
    "Migraine": {
        "desc": "A neurological condition causing intense headaches.",
        "precautions": "Avoid stress, proper sleep, reduce screen time."
    }
}

diseases_list = list(disease_info.keys())

def bfs(start):
    visited = set()
    queue = deque([start])
    found = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            if node in diseases_list:
                found.append(node)
            for neighbor in graph.get(node, []):
                queue.append(neighbor)
    return found

def detect_disease():
    user_input = entry.get().strip()
    if user_input == "":
        messagebox.showerror("Error", "Enter symptoms")
        return
    symptoms = [s.strip().title() for s in user_input.split(",")]
    score = {}
    for symptom in symptoms:
        if symptom not in graph:
            continue
        results = bfs(symptom)
        for disease in results:
            score[disease] = score.get(disease, 0) + 1
    if not score:
        output_text.set("No disease found. Check symptoms.")
        return
    sorted_diseases = sorted(score.items(), key=lambda x: x[1], reverse=True)
    result = ""
    for disease, sc in sorted_diseases:
        info = disease_info[disease]
        result += f"{disease}  | Score: {sc}\n"
        result += f"{info['desc']}\n"
        result += f"Precautions: {info['precautions']}\n\n"
    output_text.set(result)

root = tk.Tk()
root.title("AI Disease Detection")
root.geometry("540x520")
root.config(bg="#0f172a")

card = tk.Frame(root, bg="#1e293b", bd=0)
card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=440)

tk.Label(card, text="AI Disease Detection",
         font=("Segoe UI", 20, "bold"),
         bg="#1e293b", fg="#38bdf8").pack(pady=20)

tk.Label(card, text="Enter Symptoms",
         font=("Segoe UI", 11),
         bg="#1e293b", fg="#cbd5f5").pack()

entry = tk.Entry(card, width=32, font=("Segoe UI", 12), bd=0, justify="center")
entry.pack(pady=10, ipady=6)

btn = tk.Button(card, text="Detect Disease",
                command=detect_disease,
                bg="#38bdf8", fg="black",
                font=("Segoe UI", 12, "bold"),
                activebackground="#0ea5e9",
                bd=0, padx=10, pady=6)
btn.pack(pady=15)

output_text = tk.StringVar()

output_box = tk.Label(card,
                      textvariable=output_text,
                      bg="#0f172a",
                      fg="#22d3ee",
                      wraplength=400,
                      justify="left",
                      font=("Segoe UI", 10),
                      padx=10, pady=10)
output_box.pack(pady=10, fill="both", expand=True)

tk.Label(card, text="Example: Fever, Cough",
         bg="#1e293b", fg="#64748b",
         font=("Segoe UI", 9)).pack(pady=5)

root.mainloop()