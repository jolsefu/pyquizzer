import tkinter as tk
import csv

def load_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            questions.append(row)
    return questions

def display_question(root, question_data, question_index, score, score_label):
    for widget in root.winfo_children():
        if widget != score_label:
            widget.destroy()

    question_type = len(question_data)
    question = question_data[0]

    tk.Label(root, text=question, bg='white', fg='black', wraplength=400, pady=10).pack()

    if question_type == 6:
        options = question_data[1:5]
        correct_answer = question_data[5]

        selected_option = tk.StringVar(value="")

        for option in options:
            tk.Radiobutton(
                root,
                text=option,
                variable=selected_option,
                value=option,
                bg='white'
            ).pack(pady=2)

        def submit_answer():
            check_answer(selected_option.get(), correct_answer, root, question_index, score, score_label)

        tk.Button(
            root,
            text='Submit',
            command=submit_answer
        ).pack(pady=10)

def check_answer(selected_answer, correct_answer, root, question_index, score, score_label):
    if selected_answer.strip().lower() == correct_answer.strip().lower():
        score += 1

    score_label.config(text=f'Score {score}')
    next_question(root, question_index + 1, score, score_label)

def next_question(root, question_index, score, score_label):
    if question_index < len(questions):
        display_question(root, questions[question_index], question_index, score, score_label)
    else:
        for widget in root.winfo_children():
                widget.destroy()
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
            fg='black',
            bg='white',
            font=('Arial', 16),
            ).pack(pady=10)

def main():
    global questions
    questions = load_questions('quizzer.csv')

    root = tk.Tk()
    root.title('Quizzer')
    root.geometry('400x300')
    root.configure(bg='white')

    score = 0
    score_label = tk.Label(root, text=f'Score: {score}', font=('Arial', 16), bg='white')
    score_label.pack(pady=10)

    next_question(root, 0, score, score_label)

    root.mainloop()

if __name__ == '__main__':
    main()
