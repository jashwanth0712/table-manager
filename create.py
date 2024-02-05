import tkinter as tk
from tkinter import ttk
import sqlite3

class CreatePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.page_name = "Create"

        # Label to display the selected option
        self.selected_label = tk.Label(self, text="Selected Option: " + self.page_name)
        self.selected_label.pack(side="top", pady=10)

        # Label to display the content
        self.page_label = tk.Label(self, text="Create Table")
        self.page_label.pack(pady=10)

        # Table name entry
        self.table_name_label = tk.Label(self, text="Table Name:")
        self.table_name_label.pack()
        self.table_name_entry = tk.Entry(self)
        self.table_name_entry.pack(pady=5)

        # Columns frame
        self.columns_frame = tk.Frame(self)
        self.columns_frame.pack(pady=10)

        self.columns = []

        # Add initial column fields
        self.add_column_field()

        # Button to add column
        self.add_column_button = tk.Button(self, text="Add Column", command=self.add_column_field)
        self.add_column_button.pack(pady=5)

        # Button to create table
        self.create_button = tk.Button(self, text="Create Table", command=self.create_table)
        self.create_button.pack(pady=10)

        # Frame to display table structure
        self.table_structure_frame = tk.Frame(self)
        self.table_structure_frame.pack(pady=10)

    def add_column_field(self):
        column_frame = tk.Frame(self.columns_frame)
        column_frame.pack()

        column_name_label = tk.Label(column_frame, text="Column Name:")
        column_name_label.grid(row=0, column=0)
        column_name_entry = tk.Entry(column_frame)
        column_name_entry.grid(row=0, column=1)

        column_type_label = tk.Label(column_frame, text="Data Type:")
        column_type_label.grid(row=1, column=0)
        column_type_entry = tk.Entry(column_frame)
        column_type_entry.grid(row=1, column=1)

        self.columns.append((column_name_entry, column_type_entry))

    def create_table(self):
        # Get table name
        table_name = self.table_name_entry.get()

        # Get column names and data types
        columns = [(entry1.get(), entry2.get()) for entry1, entry2 in self.columns]

        # Create table in SQLite database
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ("
                       f"{', '.join([f'{col[0]} {col[1]}' for col in columns])}"
                       ")")

        connection.commit()
        connection.close()

        # Display table structure
        self.display_table_structure(table_name, columns)

    def display_table_structure(self, table_name, columns):
        structure_text = f"Table Name: {table_name}\n\n"
        structure_text += "Column Name\tData Type\n"
        structure_text += "----------------------------------\n"
        for column_name, data_type in columns:
            structure_text += f"{column_name}\t\t{data_type}\n"

        structure_label = tk.Label(self.table_structure_frame, text=structure_text, justify="left")
        structure_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    create_page = CreatePage(root)
    create_page.pack(fill="both", expand=True)
    root.mainloop()
