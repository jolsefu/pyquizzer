import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv



class QuizzerApp:
    def __init__(self):
        self.question_index = 0
        self.questions = []
        self.enable_timer = False
        self.score = 0
        self.root = None
        self.score_label = None
        self.progress_bar = None

    def delete_all_widgets(self, **kwargs):
        for widget in self.root.winfo_children():
            if kwargs.get('all', False):
                widget.destroy()
            elif widget not in [self.progress_bar, self.score_label]:
                widget.destroy()

    def load_questions(self, file_path):
        questions = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                questions.append(row)
        return questions

    def display_question(self):
        def update_timer(timer_label, time_left):
            if time_left > 0:
                time_left -= 1
                timer_label.config(text=f'Time left: {time_left} seconds')
                self.root.after(1000, update_timer, timer_label, time_left)
            else:
                self.check_answer(selected_answer, correct_answer, question_index)
                if timer_label.winfo_exists():
                    timer_label.config(text=f"Time's up!")

        if self.enable_timer:
            time_left = 5
            timer_label = tk.Label(
                self.root,
                font=('Arial', 12),
                text=f'Time left: {time_left}',
                bg='white',
                fg='red'
            )
            timer_label.pack(pady=10)

            update_timer(timer_label, time_left)

        question_data = self.questions[self.question_index]

        selected_answer = tk.StringVar()
        question_type = len(question_data)
        question = question_data[0]

        if question_type == 6:
            correct_answer = question_data[5]
        elif question_type == 4:
            correct_answer = question_data[3]
        elif question_type == 2:
            correct_answer = question_data[1]

        tk.Label(self.root, text=question, bg='white', fg='black', wraplength=400, pady=10).pack()

        if question_type == 6:
            options = question_data[1:5]

            for option in options:
                tk.Radiobutton(
                    self.root,
                    text=option,
                    variable=selected_answer,
                    value=option,
                    bg='white'
                ).pack(pady=2)

        elif question_type == 4:
            for option in ['True', 'False']:
                tk.Radiobutton(
                    self.root,
                    text=option,
                    variable=selected_answer,
                    value=option,
                    bg='white'
                ).pack(pady=2)

        elif question_type == 2:
            entry = tk.Entry(
                self.root,
                textvariable=selected_answer
            )
            entry.pack(pady=5)

        submit_button = tk.Button(
            self.root,
            text='Submit',
            command=lambda: self.check_answer(selected_answer, correct_answer)
        )
        submit_button.pack(pady=10)

    def check_answer(self, selected_answer, correct_answer):
        self.delete_all_widgets()

        if selected_answer.get().strip().lower() == correct_answer.strip().lower():
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
                text=f'Incorrect! The correct answer is: {correct_answer}',
                fg='red',
                bg='white',
                font=('Arial', 12),
            ).pack(pady=10)

        self.question_index += 1

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

    def main(self):
        file_path = filedialog.askopenfilename(
            title='Select Quiz File',
            filetypes=[('CSV Files', '*.csv')]
        )

        if not file_path:
            print('No file selected. Exiting...')
            return

        self.questions = self.load_questions(file_path)

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

        tk.Label(
            self.root,
            text="Select your options and click 'Start' to begin the quiz.",
            font=('Arial', 12),
            bg='white',
            fg='black'
        ).pack(pady=5)

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

        self.root.mainloop()

def main():
    app = QuizzerApp()
    app.main()



if __name__ == '__main__':
    main()
