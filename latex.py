import re
import subprocess
import os


class LaTeXReader():
    ''''Latex file reader and converter main class'''
    def __str__():
        return "LaTeXReader"

    def __init__(self, file):
        if not file.endswith(".tex"):
            self.new_file_name = file
            self.new_file_name_tex = file + ".tex"
        self.filename = "latex_template.tex"
        self.reader()
        self.question_pattern = r"(%paste_questions_here\d)"
        self.answer_pattern = r"(%paste_answers_here\d)"
        with open('_open_answer_template.txt', 'r') as f:
            self.open_answer_pattern = f.read()
        with open('_closed_answer_template.txt', 'r') as f:
            self.closed_answer_template = f.read()

    def writer(self, file):
        try:
            with open(self.new_file_name_tex, 'w') as f:
                f.write(file)
        except Exception as e:
            print("Please enter valid .tex file!")
            exit(0)

    def reader(self):
        try:
            with open(self.filename, 'r') as f:
                self.file = f.read()
        except FileNotFoundError as e:
            print("Please enter valid .tex file!")
            exit(0)

    def add_questions(self, number, question):
        self.last_answer = re.findall(
            self.answer_pattern, self.file)[-1]
        self.last_question = re.findall(
            self.question_pattern, self.file)[-1]

        self.new_question = self.last_question + "\n\n" + \
            "\question {0}\n".format(question)

        answer = input("Open or closed typed answers? o/c ")
        if answer == "o":
            self.new_question += r"\n\\begin{solutionorlines}[1in]\n" + \
                r"\\end{solutionorlines}" + r" %paste_questions_here" + \
                str(number+1)
            self.new_answer = self.last_answer + re.sub(
                '_Number_', str(number), self.open_answer_pattern)
            self.new_answer = re.sub(
                '_nextNumber_', str(number+1), self.new_answer)

        elif answer == "c":
            self.new_question += r"\n\\begin{oneparchoices}"
            for num in range(0, 5):
                answer = input("Input answers {}/5 \n".format(str(num+1)))
                if not answer == "q":
                    self.new_question += "\n" + "\choice {}".format(answer)
                else:
                    break
            self.new_answer = self.last_answer + \
                re.sub('_Number_', str(number), self.closed_answer_template)
            self.new_answer = re.sub('_nextNumber_', str(number+1),
                                     self.new_answer)
            self.new_question += "\n" + \
                r"\\end{oneparchoices} %%paste_questions_here" + \
                str(number+1)
        else:
            raise Exception

        self.file = re.sub(self.last_question, self.new_question, self.file)
        self.file = re.sub(self.last_answer, self.new_answer, self.file)
        self.writer(self.file)

    def delete_question(self, question):
        question_pattern = r"(\\question)([\s\S]+)(%question{})".format(
            question)
        self.file = re.sub(question_pattern, "", self.file)
        self.writer(self.file)

    def to_pdf_converter(self):
        pdf_gen = input("Whould you like to generate pdf? Y/N ")
        answers = ['', "YES", "yes", "y", "Y", "Yes"]
        if pdf_gen in answers:
            cmd = ['pdflatex', '-interaction',
                   'nonstopmode', self.new_file_name]
            proc = subprocess.Popen(cmd)
            proc.communicate()
            os.remove("{}.aux".format(self.new_file_name))
            os.remove("{}.log".format(self.new_file_name))
            os.remove("{}.tex".format(self.new_file_name))
        else:
            exit(0)


if __name__ == '__main__':
    filename = input("Enter an end file name: ")
    latex = LaTeXReader(filename)
    answer = input("Do you want to add or delete question? (add/del): ")
    if answer == "add":
        answer = int(input("How many questions you want to have? "))
        for number in range(1, answer+1):
            question = input("Enter your question {}: ".format(str(number)))
            latex.add_questions(number, question)
        latex.to_pdf_converter()
    elif answer == "exit":
        exit(0)
    # elif answer == "del":
    #     num = input("Enter number of the answer u want to delete: ")
    #     latex.delete_question(num)
    else:
        print("No such command")
