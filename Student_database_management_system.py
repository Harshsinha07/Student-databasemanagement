import tkinter as tk
from tkinter import ttk, messagebox
import pickle
class Student:
    def __init__(self, roll_no, name, course):
        self.roll_no = roll_no
        self.name = name
        self.course = course

    def __str__(self):
        return f"Roll No: {self.roll_no}, Name: {self.name}, Course: {self.course}"
class StudentDatabase:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def get_students(self):
        return self.students

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.students, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.students = pickle.load(file)
        except FileNotFoundError:
            self.students = []
class StudentDatabaseApp:
    def __init__(self, root):
        self.database = StudentDatabase()
        self.root = root
        self.root.title("Student Database Management System")

        self.roll_no_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.course_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Add Student Frame
        add_frame = ttk.LabelFrame(self.root, text="Add Student")
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(add_frame, text="Roll No:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(add_frame, textvariable=self.roll_no_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(add_frame, textvariable=self.name_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Course:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(add_frame, textvariable=self.course_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Add Student", command=self.add_student).grid(row=3, column=0, columnspan=2, pady=10)

        # Student List Frame
        list_frame = ttk.LabelFrame(self.root, text="Student List")
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.student_listbox = tk.Listbox(list_frame, height=10)
        self.student_listbox.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(list_frame, text="Load Students", command=self.load_students).grid(row=1, column=0, pady=10)
        ttk.Button(list_frame, text="Save Students", command=self.save_students).grid(row=2, column=0, pady=10)

    def add_student(self):
        roll_no = self.roll_no_var.get()
        name = self.name_var.get()
        course = self.course_var.get()

        if roll_no and name and course:
            student = Student(roll_no, name, course)
            self.database.add_student(student)
            self.student_listbox.insert(tk.END, str(student))
            self.clear_fields()
        else:
            messagebox.showwarning("Input Error", "All fields are required")

    def clear_fields(self):
        self.roll_no_var.set("") 
        self.name_var.set("")
        self.course_var.set("")

    def save_students(self):
        self.database.save_to_file("students.dat")
        messagebox.showinfo("Save Successful", "Students saved to file")

    def load_students(self):
        self.database.load_from_file("students.dat")
        self.student_listbox.delete(0, tk.END)
        for student in self.database.get_students():
            self.student_listbox.insert(tk.END, str(student))
        messagebox.showinfo("Load Successful", "Students loaded from file")
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDatabaseApp(root)
    root.mainloop()
