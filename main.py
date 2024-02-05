import tkinter as tk
from tkinter import ttk
from view import ViewPage
from create import CreatePage
from alter import AlterPage
from insert import InsertPage
from update import UpdatePage

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Navigation App")

        self.pages = {}
        self.current_page = None

        # Create a frame to hold the navigation bar
        self.navbar_frame = tk.Frame(self)
        self.navbar_frame.pack(side="top", fill="x")

        # Create navigation buttons
        buttons = ["View", "Create", "Update", "Alter", "Insert"]
        for button_text in buttons:
            button = ttk.Button(self.navbar_frame, text=button_text,
                                command=lambda b=button_text: self.open_page(b))
            button.pack(side="left", padx=5, pady=5)

        # Create a frame to hold the content
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

    def open_page(self, page_name):
        # Clear the content frame
        for child in self.content_frame.winfo_children():
            child.destroy()

        # Check if the page is not created yet
        if page_name == "View":
            self.current_page = ViewPage(self.content_frame)
        elif page_name == "Create":
            self.current_page = CreatePage(self.content_frame)
        elif page_name == "Update":
            self.current_page = UpdatePage(self.content_frame)
        elif page_name == "Alter":
            self.current_page = AlterPage(self.content_frame)
        elif page_name == "Insert":
            self.current_page = InsertPage(self.content_frame)

        self.current_page.pack(fill="both", expand=True)

import sqlite3

def add_student_table():
    # Connect to the SQLite database
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create student table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                        id INTEGER PRIMARY KEY,
                        roll_number INTEGER,
                        name TEXT
                    )''')

    # Add 10 students to the student table
    students = [
        (101, 'John Doe'),
        (102, 'Jane Smith'),
        (103, 'Michael Johnson'),
        (104, 'Emily Brown'),
        (105, 'William Davis'),
        (106, 'Emma Wilson'),
        (107, 'James Taylor'),
        (108, 'Olivia Martinez'),
        (109, 'Daniel Anderson'),
        (110, 'Sophia Thomas')
    ]

    # Insert students into the student table
    cursor.executemany("INSERT INTO student (roll_number, name) VALUES (?, ?)", students)

    # Commit changes and close connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
