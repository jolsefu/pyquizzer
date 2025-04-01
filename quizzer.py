import tkinter as tk
from tkinter import filedialog
import csv

def delete_all_widgets(root, *args):
    for widget in root.winfo_children():
        if widget not in args:
            widget.destroy()

def load_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            questions.append(row)
    return questions

def update_timer(root, score_label, timer_label):
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f'Time left: {time_left} seconds')
        root.after(1000, update_timer)
    else:
        delete_all_widgets(root, score_label, timer_label)
        timer_label.config(text=f"Time's up!")
        tk.Label(root)

def display_question(root, question_data, question_index, score, score_label, **kwargs):
    if enable_timer.get():
        time_left = 60
        timer_label = tk.Label(
            root,
            text=f'Time left: {time_left}',
            bg='white',
            fg='red'
        ).pack(pady=10)
        update_timer(root, question_index, score, score_label, timer_label)

    selected_answer = tk.StringVar()
    question_type = len(question_data)
    question = question_data[0]

    tk.Label(root, text=question, bg='white', fg='black', wraplength=400, pady=10).pack()

    if question_type == 6:
        options = question_data[1:5]
        correct_answer = question_data[5]

        for option in options:
            tk.Radiobutton(
                root,
                text=option,
                variable=selected_answer,
                value=option,
                bg='white'
            ).pack(pady=2)

    elif question_type == 4:
        correct_answer = question_data[3]

        for option in ['True', 'False']:
            tk.Radiobutton(
                root,
                text=option,
                variable=selected_answer,
                value=option,
                bg='white'
            ).pack(pady=2)

    elif question_type == 2:
        correct_answer = question_data[1]
        entry = tk.Entry(
            root,
            textvariable=selected_answer
        )
        entry.pack(pady=5)

    tk.Button(
        root,
        text='Submit',
        command=lambda: check_answer(selected_answer, correct_answer, root, question_index, score, score_label)
    ).pack(pady=5)

def check_answer(selected_answer, correct_answer, root, question_index, score, score_label):
    delete_all_widgets(root, score_label)

    if selected_answer.get().strip().lower() == correct_answer.strip().lower():
        score += 1
        score_label.config(text=f'Score {score}', fg='green')

        tk.Label(
            root,
            text='Correct!',
            fg='green',
            bg='white',
            font=('Arial', 12)
        ).pack(pady=10)
    else:
        tk.Label(
            root,
            text=f'Incorrect! The correct answer is: {correct_answer}',
            fg='red',
            bg='white',
            font=('Arial', 12),
        ).pack(pady=10)

    tk.Button(
        root,
        text='Next',
        command=lambda: next_question(root, question_index + 1, score, score_label),
    ).pack(pady=10)

def next_question(root, question_index, score, score_label):
    if question_index < len(questions):
        delete_all_widgets(root, score_label)
        display_question(root, questions[question_index], question_index, score, score_label)
    else:
        delete_all_widgets(root)

        tk.Label(
            root,
            text=f'Quiz Completed!',
            fg='black',
            bg='white',
            font=('Arial', 16),
        ).pack(pady=10)

        tk.Label(
            root,
            text=f'Your total score is {score}',
            fg='green',
            bg='white',
            font=('Arial', 16),
        ).pack(pady=10)

def main():
    global questions, enable_timer, selected_answer

    file_path = filedialog.askopenfilename(
        title='Select Quiz File',
        filetypes=[('CSV Files', '*.csv')]
    )

    if not file_path:
        print('No file selected. Exiting...')
        return

    questions = load_questions(file_path)

    root = tk.Tk()
    root.title('Quizzer')
    root.geometry('600x500')
    root.configure(bg='white')

    tk.Label(
        root,
        text='Welcome to Quizzer!',
        font=('Arial', 16),
        bg='white',
        fg='black'
    ).pack(pady=10)

    tk.Label(
        root,
        text="Select your options and click 'Start' to begin the quiz.",
        font=('Arial', 12),
        bg='white',
        fg='black'
    ).pack(pady=5)

    enable_timer = tk.BooleanVar(value=False)

    tk.Checkbutton(
        root,
        text='Enable 1 Minute Timer',
        variable=enable_timer,
        onvalue=True,
        offvalue=False,
        bg='white',
    ).pack(pady=5)

    def start_quiz():
        score = 0
        score_label = tk.Label(root, text=f'Score {score}', font=('Arial', 16), bg='white', fg='green')
        score_label.pack(pady=10)

        next_question(root, 0, score, score_label)

    tk.Button(root, text='Start', command=start_quiz, font=('Arial', 12), bg='blue', fg='white').pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    main()
