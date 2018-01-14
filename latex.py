import re
import subprocess


class LaTeXReader():
    ''''Latex file reader and converter main class'''
    def __str__():
        return "LaTeXReader"

    def __init__(self, file):
        if not file.endswith(".tex"):
            file += ".tex"
        self.filename = file
        self.reader()
        self.question_pattern = "(%question\d)"
        self.question_pattern_for_last_answer = "(%new_answer_here\d)"
        with open('answer_template.txt', 'r') as f:
            self.answer_template = f.read()
        with open('closed_answer_template.txt', 'r') as f:
            self.closed_answer_template = f.read()

        self.last_answer = re.findall(
            self.question_pattern_for_last_answer, self.file)[-1]
        self.last_question_number = len(re.findall(
            self.question_pattern, self.file))
        self.next_question_number = self.last_question_number + 1

    def writer(self, file):
        try:
            with open(self.filename, 'w') as f:
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

    def add_questions(self, question):
        self.last_question = re.findall(self.question_pattern, self.file)[-1]
        self.new_question = self.last_question + "\n\n" + \
            "\question {0}\n".format(question)

        answer = input("Open or closed typed answers? o/c\n")
        if answer == "o":

            self.new_question += r"\n\\begin{solutionorlines}[0.5in]\n" + \
                r"\\end{solutionorlines}" + "%question" + \
                str(self.next_question_number)
            self.new_answer = re.sub('_Number_', str(
                self.next_question_number), self.answer_template)

        elif answer == "c":
            self.new_question += r"\n\\begin{oneparchoices}"
            for num in range(0, 5):
                answer = input("Input answers {}/5 \n".format(str(num+1)))
                if not answer == "q":
                    self.new_question += "\n" + "\choice {}".format(answer)
                else:
                    break
            self.new_answer = self.last_answer + re.sub('_Number_', str(
                self.next_question_number), self.closed_answer_template)
            self.new_question += "\n" + \
                r"\\end{oneparchoices} %question" + \
                str(self.next_question_number)
        else:
            raise Exception

        self.file = re.sub(self.last_question, self.new_question, self.file)
        self.file = re.sub(self.last_answer, self.new_answer, self.file)
        self.writer(self.file)
        self.to_pdf_converter()

    def delete_question(self, question):
        question_pattern = r"(\\question)([\s\S]+)(%question{})".format(
            question)
        self.file = re.sub(question_pattern, "", self.file)
        self.writer(self.file)

    def to_pdf_converter(self):
        pdf_gen = input("Whould you like to generate pdf? Y/N ")
        answers = ['', "YES", "yes", "y", "Y", "Yes"]
        if pdf_gen in answers:
            cmd = ['pdflatex', '-interaction', 'nonstopmode', self.filename]
            proc = subprocess.Popen(cmd)
            proc.communicate()
        else:
            exit(0)


if __name__ == '__main__':
    filename = input("Enter a file name: ")
    latex = LaTeXReader(filename)
    answer = input("Do you want to add or delete question? (add/del): ")
    if answer == "add":
        question = input("Enter your question: ")
        latex.add_questions(question)
    elif answer == "exit":
        exit(0)
    elif answer == "del":
        num = input("Enter number of the answer u want to delete: ")
        latex.delete_question(num)
    else:
        print("No such command")
