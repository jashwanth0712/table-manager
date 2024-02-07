import tkinter as tk
from tkinter import ttk
import sqlite3

class InsertPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.page_name = "Insert"
        self.data_entries = {}  # Store entry fields for data insertion

        # Label to display the selected option
        self.selected_label = tk.Label(self, text="Selected Option: " + self.page_name)
        self.selected_label.pack(side="top", pady=10)

        # Label to display the content
        self.page_label = tk.Label(self, text="Insert Data into Table")
        self.page_label.pack(pady=10)

        # Label to display the content
        self.table_name_label = tk.Label(self, text="select table name")
        self.table_name_label.pack(pady=10, padx=10, anchor="w")

        # Dropdown to display table names
        self.table_name_entry = ttk.Combobox(self, state="readonly")
        self.table_name_entry.pack(pady=5, padx=10)

        # Button to fetch table details
        self.fetch_button = tk.Button(self, text="Fetch Table Details", command=self.fetch_table_details)
        self.fetch_button.pack(pady=5)

        

        # Treeview to display table details
        self.treeview = ttk.Treeview(self)
        self.treeview.pack(pady=10, padx=10, fill="both", expand=True)

        # Initialize database connection
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.populate_table_dropdown()


    def fetch_table_details(self):
        # Clear existing treeview items
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Get table name from entry field
        table_name = self.table_name_entry.get()

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

        # Create entry fields for data insertion
        self.create_entry_fields(columns)
        # Button to insert data
        self.insert_button = tk.Button(self, text="Insert Data", command=self.insert_data)
        self.insert_button.pack(pady=10)

    def create_entry_fields(self, columns):
        # Clear existing entry fields
        for entry in self.data_entries.values():
            entry.destroy()
        self.data_entries = {}

        # Create entry fields for each column
        for col in columns:
            label = tk.Label(self, text=col + ":")
            label.pack()
            entry = tk.Entry(self)
            entry.pack()
            self.data_entries[col] = entry

    def insert_data(self):
        # Get table name from entry field
        table_name = self.table_name_entry.get()

        # Fetch column names from SQLite database
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]

        # Prepare data to insert
        data = []
        for col in columns:
            entry = self.data_entries[col].get()
            data.append(entry if entry else 'NULL')

        # Insert data into the table
        self.cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})", data)
        self.connection.commit()

        # Fetch and display updated table details
        self.fetch_table_details()

        # Notify the user
        tk.messagebox.showinfo("Success", "Data inserted successfully!")

        self.connection.close()
    def populate_table_dropdown(self):
        # Fetch table names from SQLite database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in self.cursor.fetchall()]

        # Insert table names into the dropdown
        self.table_name_entry['values'] = tables
if __name__ == "__main__":
    root = tk.Tk()
    insert_page = InsertPage(root)
    insert_page.pack(fill="both", expand=True)
    root.mainloop()
