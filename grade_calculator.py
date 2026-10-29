import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Settings ----------
SUBJECTS = ["Maths", "OS", "DSA", "COA", "APP"]
MAX_MARKS = 100  

# ---------- Dark theme colors ----------
BG = "#1e1e2e"          # window background
HEADER = "#11111b"      # header bar
CARD = "#2a2a3c"        # card background
TEXT = "#f5f5f5"        # main text
MUTED = "#a6adc8"       # labels / secondary text
ENTRY_BG = "#3a3a4f"    # input boxes
BORDER = "#45475a"
GREEN = "#2ecc71"
GREEN_DARK = "#27ae60"
RED = "#ff6b6b"
ORANGE = "#e67e22"
ORANGE_DARK = "#ca6f1e"
GREY = "#6c7086"
GREY_DARK = "#585b70"


# ---------- Functions ----------
def get_grade(percentage):
    """Return grade letter based on percentage."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def make_entry(parent):
    """Create a dark input box."""
    return tk.Entry(parent, font=("Segoe UI", 11), width=20, relief="flat",
                    bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                    highlightthickness=1, highlightbackground=BORDER,
                    highlightcolor="#3498db")


def reset_result():
    """Show the empty/default result card."""
    name_result.config(text="Enter details and press Calculate")
    roll_result.config(text="")
    grade_label.config(text="--", fg=MUTED)
    percent_label.config(text="")
    total_label.config(text="")
    status_label.config(text="")
    progress["value"] = 0
    progress.config(style="Pass.Horizontal.TProgressbar")


def calculate(event=None):
    """Read details and marks, validate them, and show the result."""
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()

    if name == "":
        messagebox.showwarning("Missing Name", "Please enter the student's name.")
        name_entry.focus()
        return
    if roll == "":
        messagebox.showwarning("Missing Roll No", "Please enter the roll number.")
        roll_entry.focus()
        return

    total = 0
    for subject in SUBJECTS:
        value = entries[subject].get().strip()

        # check the input is a number
        try:
            marks = float(value)
        except ValueError:
            messagebox.showerror("Invalid Input", f"Enter a valid number for {subject}.")
            entries[subject].focus()
            return

        # check the marks are in range
        if marks < 0 or marks > MAX_MARKS:
            messagebox.showerror("Invalid Marks",
                                 f"{subject} marks must be between 0 and {MAX_MARKS}.")
            entries[subject].focus()
            return

        total += marks

    max_total = MAX_MARKS * len(SUBJECTS)
    percentage = (total / max_total) * 100
    grade = get_grade(percentage)
    passed = grade != "F"
    color = GREEN if passed else RED

    # update the result card
    name_result.config(text=name)
    roll_result.config(text=f"Roll No: {roll}")
    grade_label.config(text=grade, fg=color)
    percent_label.config(text=f"{percentage:.2f}%")
    total_label.config(text=f"Total: {total:.0f} / {max_total}")
    status_label.config(text="PASS" if passed else "FAIL", fg=color)
    progress.config(style="Pass.Horizontal.TProgressbar" if passed
                    else "Fail.Horizontal.TProgressbar")
    progress["value"] = percentage


def redo():
    """Redo: empty all fields and the result card so a new calculation can start."""
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    for subject in SUBJECTS:
        entries[subject].delete(0, tk.END)
    reset_result()
    name_entry.focus()


# ---------- Window ----------
root = tk.Tk()
root.title("Student Grade Calculator")
root.geometry("760x760")
root.resizable(False, False)
root.config(bg=BG)

# progress bar styles (green for pass, red for fail)
style = ttk.Style()
style.theme_use("clam")
style.configure("Pass.Horizontal.TProgressbar", troughcolor=BORDER,
                background=GREEN, thickness=14)
style.configure("Fail.Horizontal.TProgressbar", troughcolor=BORDER,
                background=RED, thickness=14)

# ---------- Header ----------
header = tk.Frame(root, bg=HEADER)
header.pack(fill="x")
tk.Label(header, text="Student Grade Calculator", font=("Segoe UI", 17, "bold"),
         bg=HEADER, fg="white").pack(pady=(14, 0))
tk.Label(header, text="Enter marks and get your grade instantly", font=("Segoe UI", 9),
         bg=HEADER, fg=MUTED).pack(pady=(0, 14))

# ---------- Input card ----------
input_card = tk.Frame(root, bg=CARD, padx=20, pady=15)
input_card.pack(fill="x", padx=20, pady=(18, 8))

tk.Label(input_card, text="Student Details", font=("Segoe UI", 12, "bold"),
         bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

tk.Label(input_card, text="Name", font=("Segoe UI", 10), bg=CARD,
         fg=MUTED).grid(row=1, column=0, sticky="w", pady=4)
name_entry = make_entry(input_card)
name_entry.grid(row=1, column=1, padx=(15, 0), pady=4, ipady=3)

tk.Label(input_card, text="Roll No", font=("Segoe UI", 10), bg=CARD,
         fg=MUTED).grid(row=2, column=0, sticky="w", pady=4)
roll_entry = make_entry(input_card)
roll_entry.grid(row=2, column=1, padx=(15, 0), pady=4, ipady=3)

entries = {}
for i, subject in enumerate(SUBJECTS, start=3):
    tk.Label(input_card, text=f"{subject} (/{MAX_MARKS})", font=("Segoe UI", 10),
             bg=CARD, fg=MUTED).grid(row=i, column=0, sticky="w", pady=4)
    entry = make_entry(input_card)
    entry.grid(row=i, column=1, padx=(15, 0), pady=4, ipady=3)
    entries[subject] = entry

# ---------- Buttons ----------
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=8)

calc_btn = tk.Button(btn_frame, text="Calculate", font=("Segoe UI", 11, "bold"),
                     bg=GREEN_DARK, fg="white", activebackground=GREEN,
                     activeforeground="white", relief="flat", width=10,
                     cursor="hand2", command=calculate)
calc_btn.grid(row=0, column=0, padx=6, ipady=4)

redo_btn = tk.Button(btn_frame, text="Redo", font=("Segoe UI", 11, "bold"),
                      bg=ORANGE, fg="white", activebackground=ORANGE_DARK,
                      activeforeground="white", relief="flat", width=10,
                      cursor="hand2", command=redo)
redo_btn.grid(row=0, column=1, padx=6, ipady=4)

exit_btn = tk.Button(btn_frame, text="Exit", font=("Segoe UI", 11, "bold"),
                     bg=GREY, fg="white", activebackground=GREY_DARK,
                     activeforeground="white", relief="flat", width=10,
                     cursor="hand2", command=root.destroy)
exit_btn.grid(row=0, column=2, padx=6, ipady=4)


# ---------- Result card ----------
result_card = tk.Frame(root, bg=CARD, padx=20, pady=15)
result_card.pack(fill="x", padx=20, pady=(8, 18))

tk.Label(result_card, text="Result", font=("Segoe UI", 12, "bold"),
         bg=CARD, fg=TEXT).pack(anchor="w")

name_result = tk.Label(result_card, font=("Segoe UI", 11, "bold"), bg=CARD, fg=TEXT)
name_result.pack(pady=(6, 0))

roll_result = tk.Label(result_card, font=("Segoe UI", 10), bg=CARD, fg=MUTED)
roll_result.pack()

grade_label = tk.Label(result_card, font=("Segoe UI", 44, "bold"), bg=CARD)
grade_label.pack()

percent_label = tk.Label(result_card, font=("Segoe UI", 14, "bold"), bg=CARD, fg=TEXT)
percent_label.pack()

progress = ttk.Progressbar(result_card, length=300, maximum=100,
                           style="Pass.Horizontal.TProgressbar")
progress.pack(pady=8)

total_label = tk.Label(result_card, font=("Segoe UI", 10), bg=CARD, fg=MUTED)
total_label.pack()

status_label = tk.Label(result_card, font=("Segoe UI", 14, "bold"), bg=CARD)
status_label.pack(pady=(4, 0))

# ---------- Start ----------
reset_result()
root.bind("<Return>", calculate)  # press Enter to calculate
name_entry.focus()
root.mainloop()