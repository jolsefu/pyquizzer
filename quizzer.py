import tkinter as tk
import csv

def load_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            questions.append(row)
    return questions

def next_question(root, curr_question, score, score_label):
    if curr_question < len(questions):
        display_question(root, curr_question, score, score_label)
    else:
        for widget in root.winfo_children():
            widget.destroy()
        tk.Label(root, text=f'Quiz Completed! Your score is {score / len(questions)}')

def main():
    global questions
    questions = load_questions('quizzer.csv')

    root = tk.Tk()
    root.title("Quizzer")
    root.geometry("400x300")
    root.configure(bg='lightblue')

    score = 0
    score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 16), bg='lightblue')
    score_label.pack(pady=10)

    next_question(root, 0, score, score_label)

    root.mainloop()

if __name__ == '__main__':
    main()
