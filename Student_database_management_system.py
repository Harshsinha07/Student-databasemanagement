import json
import tkinter as tk
from tkinter import ttk, messagebox
import os

DATA_FILE = "students.json"


# --------------------- JSON STORAGE ---------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# --------------------- MAIN APP ---------------------
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager - Dark Mode")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e1e")

        self.data = load_data()

        self.setup_styles()
        self.create_widgets()
        self.refresh_table()

    # ----------------- Dark Mode Styling -----------------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#2d2d2d",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#2d2d2d",
                        bordercolor="#3c3c3c",
                        borderwidth=0)

        style.configure("Treeview.Heading",
                        background="#3c3c3c",
                        foreground="white",
                        font=("Calibri", 12, "bold"))

        style.map("Treeview",
                  background=[("selected", "#007acc")])

    # ------------------ UI LAYOUT ------------------
    def create_widgets(self):
        # ---------- TOP BAR ----------
        top_frame = tk.Frame(self.root, bg="#1e1e1e")
        top_frame.pack(fill=tk.X, pady=5)

        tk.Label(top_frame, text="Search:", fg="white", bg="#1e1e1e",
                 font=("Calibri", 12)).pack(side=tk.LEFT, padx=10)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(top_frame, textvariable=self.search_var,
                                font=("Calibri", 12), bg="#2d2d2d",
                                fg="white", insertbackground="white", width=25)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        # Filter dropdown
        tk.Label(top_frame, text="Filter by Course:", fg="white",
                 bg="#1e1e1e", font=("Calibri", 12)).pack(side=tk.LEFT, padx=10)

        self.filter_var = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(top_frame, textvariable=self.filter_var,
                                            values=["All"], state="readonly", width=15)
        self.filter_dropdown.pack(side=tk.LEFT)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        # Buttons
        ttk.Button(top_frame, text="Add Student", command=self.open_add_window).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="Update Student", command=self.open_update_window).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="Delete", command=self.delete_student).pack(side=tk.RIGHT, padx=5)

        # ---------- STUDENT TABLE ----------
        self.table = ttk.Treeview(self.root, columns=("id", "name", "age", "course"), show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Name")
        self.table.heading("age", text="Age")
        self.table.heading("course", text="Course")
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ----------------------- CRUD WINDOWS -----------------------
    def open_add_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Student")
        win.geometry("300x300")
        win.configure(bg="#1e1e1e")

        id_var = tk.StringVar()
        name_var = tk.StringVar()
        age_var = tk.StringVar()
        course_var = tk.StringVar()

        fields = [("ID", id_var), ("Name", name_var), ("Age", age_var), ("Course", course_var)]
        for idx, (label, var) in enumerate(fields):
            tk.Label(win, text=label, bg="#1e1e1e", fg="white", font=("Calibri", 12)).pack(pady=3)
            tk.Entry(win, textvariable=var, bg="#2d2d2d", fg="white",
                     insertbackground="white").pack()

        def save():
            if not id_var.get() or not name_var.get() or not age_var.get() or not course_var.get():
                messagebox.showwarning("Error", "All fields required")
                return

            self.data.append({
                "id": id_var.get(),
                "name": name_var.get(),
                "age": age_var.get(),
                "course": course_var.get()
            })

            save_data(self.data)
            self.refresh_table()
            win.destroy()

        tk.Button(win, text="Save", command=save, bg="#007acc", fg="white").pack(pady=10)

    def open_update_window(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Error", "Select a student first")
            return

        values = self.table.item(selected, "values")
        sid, old_name, old_age, old_course = values

        win = tk.Toplevel(self.root)
        win.title("Update Student")
        win.geometry("300x300")
        win.configure(bg="#1e1e1e")

        name_var = tk.StringVar(value=old_name)
        age_var = tk.StringVar(value=old_age)
        course_var = tk.StringVar(value=old_course)

        tk.Label(win, text="Name", bg="#1e1e1e", fg="white").pack()
        tk.Entry(win, textvariable=name_var, bg="#2d2d2d", fg="white").pack()

        tk.Label(win, text="Age", bg="#1e1e1e", fg="white").pack()
        tk.Entry(win, textvariable=age_var, bg="#2d2d2d", fg="white").pack()

        tk.Label(win, text="Course", bg="#1e1e1e", fg="white").pack()
        tk.Entry(win, textvariable=course_var, bg="#2d2d2d", fg="white").pack()

        def update():
            for student in self.data:
                if student["id"] == sid:
                    student["name"] = name_var.get()
                    student["age"] = age_var.get()
                    student["course"] = course_var.get()

            save_data(self.data)
            self.refresh_table()
            win.destroy()

        tk.Button(win, text="Update", bg="#007acc", fg="white",
                  command=update).pack(pady=10)

    # ----------------------- DELETE -----------------------
    def delete_student(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Error", "Select a student first")
            return

        sid = self.table.item(selected, "values")[0]

        self.data = [s for s in self.data if s["id"] != sid]
        save_data(self.data)
        self.refresh_table()

    # ----------------------- REFRESH TABLE -----------------------
    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        search = self.search_var.get().lower()
        course_filter = self.filter_var.get()

        courses = {"All"}
        for s in self.data:
            courses.add(s["course"])
        self.filter_dropdown["values"] = list(courses)

        for s in self.data:
            if search and search not in s["name"].lower() and search not in s["id"].lower():
                continue
            if course_filter != "All" and s["course"] != course_filter:
                continue
            self.table.insert("", tk.END, values=(s["id"], s["name"], s["age"], s["course"]))


# --------------------- RUN APP ---------------------
root = tk.Tk()
app = StudentApp(root)
root.mainloop()
