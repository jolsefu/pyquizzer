import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import datetime



class QuizzerApp:
    def __init__(self):
        self.quiz_file_path = None
        self.question_index = 0
        self.questions = []
        self.enable_timer = False
        self.root = None

        self.selected_answer = None
        self.correct_answer = None

        self.score = 0
        self.total_score = 0
        self.score_label = None
        self.progress_bar = None

        self.timer_label = None
        self.time_left = 0
        self.timer_id = None

    def delete_all_widgets(self, **kwargs):
        for widget in self.root.winfo_children():
            if kwargs.get('all', False):
                widget.destroy()
            elif widget not in [self.progress_bar, self.score_label]:
                widget.destroy()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f'Time left: {self.time_left} seconds')
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.check_answer()

    def display_question(self):
        if self.enable_timer:
            self.time_left = 5

            self.timer_label = tk.Label(
                self.root,
                font=('Arial', 12),
                text=f'Time left: {self.time_left}',
                bg='white',
                fg='red'
            )
            self.timer_label.pack(pady=10)

            self.update_timer()

        question_data = self.questions[self.question_index]

        self.selected_answer = tk.StringVar()
        question_type = len(question_data)
        question = question_data[0]

        if question_type == 6:
            self.correct_answer = question_data[5]
        elif question_type == 4:
            self.correct_answer = question_data[3]
        elif question_type == 2:
            self.correct_answer = question_data[1]

        tk.Label(self.root, text=question, bg='white', fg='black', wraplength=400, pady=10).pack()

        if question_type == 6:
            options = question_data[1:5]

            for option in options:
                tk.Radiobutton(
                    self.root,
                    text=option,
                    variable=self.selected_answer,
                    value=option,
                    bg='white'
                ).pack(pady=2)

        elif question_type == 4:
            for option in ['True', 'False']:
                tk.Radiobutton(
                    self.root,
                    text=option,
                    variable=self.selected_answer,
                    value=option,
                    bg='white'
                ).pack(pady=2)

        elif question_type == 2:
            entry = tk.Entry(
                self.root,
                textvariable=self.selected_answer
            )
            entry.pack(pady=5)

        tk.Button(
            self.root,
            text='Submit',
            command=lambda: self.check_answer()
        ).pack(pady=10)

    def check_answer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.delete_all_widgets()

        if self.selected_answer.get().strip().lower() == self.correct_answer.strip().lower():
            self.score += 1
            self.score_label.config(text=f'Score {self.score}', fg='green')

            tk.Label(
                self.root,
                text='Correct!',
                fg='green',
                bg='white',
                font=('Arial', 12)
            ).pack(pady=10)
        else:
            tk.Label(
                self.root,
                text=f'Incorrect! The correct answer is: {self.correct_answer}',
                fg='red',
                bg='white',
                font=('Arial', 12),
            ).pack(pady=10)

        self.question_index += 1
        self.total_score += 1

        tk.Button(
            self.root,
            text='Next',
            command=lambda: self.next_question(),
        ).pack(pady=10)

    def next_question(self):
        if self.question_index < len(self.questions):
            self.delete_all_widgets()

            progress = (self.question_index) / len(self.questions) * 100
            self.progress_bar['value'] = progress

            self.display_question()
        else:
            self.delete_all_widgets(all=True)

            tk.Label(
                self.root,
                text=f'Quiz Completed!',
                fg='black',
                bg='white',
                font=('Arial', 16),
            ).pack(pady=10)

            tk.Label(
                self.root,
                text=f'Your total score is {self.score}',
                fg='green',
                bg='white',
                font=('Arial', 16),
            ).pack(pady=10)

            score_data = {
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'score': self.score,
                'total_score': self.total_score,
                'quiz_file': self.quiz_file_path.split('/')[-1]
            }

            with open('scores.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['date', 'score', 'total_score', 'quiz_file'])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(score_data)

    def start_quiz(self):
        self.delete_all_widgets()

        self.score = 0
        self.score_label = tk.Label(self.root, text=f'Score {self.score}', font=('Arial', 16), bg='white', fg='green')
        self.score_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(
            self.root,
            orient='horizontal',
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)

        self.next_question()

    def load_questions(self, file_path):
        questions = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                questions.append(row)
        return questions

    def show_scores(self):
        self.delete_all_widgets()

        tk.Label(
            self.root,
            text='Quiz Scores',
            font=('Arial', 16),
            bg='white',
            fg='black'
        ).pack(pady=10)

        with open('scores.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skip first row
            for row in reader:
                tk.Label(
                    text=f'Quiz {row[3]} with a score of {row[1]}/{row[2]} on {row[0]}',
                    bg='white',
                    fg='black'
                ).pack(pady=5)

    def load_quiz_file(self):
        def load_quiz_file(self):
            file_path = filedialog.askopenfilename(
                title='Select Quiz File',
                filetypes=[('CSV Files', '*.csv')]
            )
            if file_path:
                self.delete_all_widgets()
                with open(file_path, 'r') as file:
                    first_row = file.readline().strip()
                    if first_row.lower() == 'quiz':
                        self.questions = self.load_questions(file_path)
                        self.quiz_file_path = file_path
                        self.quiz_settings()
                    elif first_row.lower() == 'scores':
                        self.show_scores()

        tk.Button(
            text='Load Quiz File or Scores',
            command=lambda: load_quiz_file(self),
            font=('Arial', 12),
            bg='blue',
            fg='white'
        ).pack(pady=10)

    def quiz_settings(self):
        tk.Label(
            self.root,
            text="Select your options and click 'Start' to begin the quiz.",
            font=('Arial', 12),
            bg='white',
            fg='black'
        ).pack(pady=10)

        enable_timer_var = tk.BooleanVar(value=False)
        self.enable_timer = enable_timer_var.get()

        tk.Checkbutton(
            self.root,
            text='Enable 1 Minute Timer',
            variable=enable_timer_var,
            onvalue=True,
            offvalue=False,
            bg='white',
            command=lambda: setattr(self, 'enable_timer', enable_timer_var.get())
        ).pack(pady=5)

        tk.Button(self.root, text='Start', command=self.start_quiz, font=('Arial', 12), bg='blue', fg='white').pack(pady=20)

    def main(self):
        self.root = tk.Tk()
        self.root.title('Quizzer')
        self.root.geometry('600x500')
        self.root.configure(bg='white')

        tk.Label(
            self.root,
            text='Welcome to Quizzer!',
            font=('Arial', 16),
            bg='white',
            fg='black'
        ).pack(pady=10)

        self.load_quiz_file()

        self.root.mainloop()

def main():
    app = QuizzerApp()
    app.main()



if __name__ == '__main__':
    main()
