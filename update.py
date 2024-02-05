import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Import messagebox module separately
import sqlite3

class UpdatePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.page_name = "Update"

        # Label to display the selected option
        self.selected_label = tk.Label(self, text="Selected Option: " + self.page_name)
        self.selected_label.pack(side="top", pady=10)

        # Label to display the content
        self.page_label = tk.Label(self, text="Update Data in Table")
        self.page_label.pack(pady=10)

        # Table name entry
        self.table_name_label = tk.Label(self, text="Table Name:")
        self.table_name_label.pack()
        self.table_name_entry = tk.Entry(self)
        self.table_name_entry.pack(pady=5)

        # Button to fetch table details
        self.fetch_button = tk.Button(self, text="Fetch Table Details", command=self.fetch_table_details)
        self.fetch_button.pack(pady=5)

        # Button to save changes
        self.save_button = tk.Button(self, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=10)

        # Treeview to display table details
        self.treeview = ttk.Treeview(self, show="headings")
        self.treeview.pack(pady=10, padx=10, fill="both", expand=True)

        # Store table details fetched from the database
        self.table_data = []

        # Initialize database connection
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

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
            # Add an "Edit" button for each row
            edit_button = ttk.Button(self.treeview, text="Edit", command=lambda r=row: self.edit_row(r))
            self.treeview.insert('', 'end', values=row, tags='button')
            self.treeview.set(row, '#6', edit_button)  # Add the edit_button to the last column

        # Store table details
        self.table_data = rows

    def save_changes(self):
        # Update table with modified data
        table_name = self.table_name_entry.get()
        
        for i, row in enumerate(self.table_data):
            for j, value in enumerate(row):
                new_value = self.treeview.item(self.treeview.get_children()[i])['values'][j]
                if new_value != value:
                    self.cursor.execute(f"UPDATE {table_name} SET {self.treeview['columns'][j]} = ? WHERE rowid = ?", (new_value, row[0]))

        self.connection.commit()
        self.fetch_table_details()
        messagebox.showinfo("Success", "Changes saved successfully!")  # Use messagebox from tkinter

    def edit_row(self, row):
        # Create a new window for editing
        self.edit_window = tk.Toplevel(self)
        self.edit_window.title("Edit Row")

        # Labels and entry fields to display row data
        self.edit_fields = []
        for index, value in enumerate(row):
            label = tk.Label(self.edit_window, text=self.treeview.heading(index)["text"])
            label.grid(row=index, column=0, padx=5, pady=5)
            entry = tk.Entry(self.edit_window)
            entry.grid(row=index, column=1, padx=5, pady=5)
            entry.insert(0, value)
            self.edit_fields.append(entry)

        # Save button to commit changes
        save_button = tk.Button(self.edit_window, text="Save", command=self.save_edit)
        save_button.grid(row=len(row), column=0, columnspan=2, pady=10)

    def save_edit(self):
        table_name = self.table_name_entry.get()
        row_id = self.table_data[self.treeview.index(self.treeview.selection())][0]

        # Get new values from entry fields
        new_values = [entry.get() for entry in self.edit_fields]

        # Update the database with the new values
        for index, value in enumerate(new_values):
            self.cursor.execute(f"UPDATE {table_name} SET {self.treeview.heading(index)['text']} = ? WHERE rowid = ?", (value, row_id))

        self.connection.commit()
        self.fetch_table_details()
        self.edit_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    update_page = UpdatePage(root)
    update_page.pack(fill="both", expand=True)
    root.mainloop()
