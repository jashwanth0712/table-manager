import tkinter as tk
from tkinter import ttk
import sqlite3

class ViewPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.page_name = "View"

        # Label to display the content
        self.page_label = tk.Label(self, text="select table name")
        self.page_label.pack(pady=10, padx=10, anchor="w")

        # Dropdown to display table names
        self.table_dropdown = ttk.Combobox(self, state="readonly")
        self.table_dropdown.pack(pady=5, padx=10)
        
        # Button to fetch table details
        self.fetch_button = tk.Button(self, text="Fetch Table Details", command=self.fetch_table_details)
        self.fetch_button.pack(pady=5, padx=10)

        # Treeview to display table details
        self.treeview = ttk.Treeview(self)
        self.treeview.pack(pady=10, padx=10, fill="both", expand=True)

        # Initialize database connection
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

        # Populate table names in the dropdown
        self.populate_table_dropdown()

    def populate_table_dropdown(self):
        # Fetch table names from SQLite database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in self.cursor.fetchall()]

        # Insert table names into the dropdown
        self.table_dropdown['values'] = tables

    def fetch_table_details(self):
        # Clear existing treeview items
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Get selected table name from the dropdown
        table_name = self.table_dropdown.get()

        # Fetch table details from SQLite database
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]

        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()

        # Display table details in treeview
        self.treeview['columns'] = columns
        for col in columns:
            self.treeview.heading(col, text=col)

        for row in rows:
            self.treeview.insert('', 'end', values=row)

if __name__ == "__main__":
    root = tk.Tk()
    view_page = ViewPage(root)
    view_page.pack(fill="both", expand=True)
    root.mainloop()
