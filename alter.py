import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class AlterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.page_name = "Alter"

        # Label to display the selected option
        self.selected_label = tk.Label(self, text="Selected Option: " + self.page_name)
        self.selected_label.pack(side="top", pady=10)

             # Label to display the content
        self.table_name_label = tk.Label(self, text="select table name")
        self.table_name_label.pack(pady=10, padx=10, anchor="w")

        # Dropdown to display table names
        self.table_name_entry = ttk.Combobox(self, state="readonly")
        self.table_name_entry.pack(pady=5, padx=10)

        # Button to fetch table details
        self.fetch_button = tk.Button(self, text="Fetch Table Details", command=self.fetch_table_details)
        self.fetch_button.pack(pady=5)

        # Frame to display column details
        self.column_frame = tk.Frame(self)
        self.column_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Button to add column
        self.add_column_button = tk.Button(self, text="Add Column", command=self.add_column)
        self.add_column_button.pack(pady=5)

        # Button to delete column
        self.delete_column_button = tk.Button(self, text="Delete Column", command=self.delete_column)
        self.delete_column_button.pack(pady=5)

        # Button to save changes
        self.save_button = tk.Button(self, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=10)

        # Store table details fetched from the database
        self.table_columns = []

        # Initialize database connection
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.populate_table_dropdown()


    def fetch_table_details(self):
        # Clear existing column details
        for widget in self.column_frame.winfo_children():
            widget.destroy()

        # Get table name from entry field
        table_name = self.table_name_entry.get()

        # Fetch table details (columns) from the database
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            self.table_columns = self.cursor.fetchall()

            # Display column details
            for column in self.table_columns:
                column_label = tk.Label(self.column_frame, text=f"{column[1]}: {column[2]}")
                column_label.pack()
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def add_column(self):
        # Get table name from entry field
        table_name = self.table_name_entry.get()

        # Create a new window for adding a column
        self.add_column_window = tk.Toplevel(self)
        self.add_column_window.title("Add Column")

        # Entry fields for column name and type
        self.column_name_label = tk.Label(self.add_column_window, text="Column Name:")
        self.column_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.column_name_entry = tk.Entry(self.add_column_window)
        self.column_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.column_type_label = tk.Label(self.add_column_window, text="Column Type:")
        self.column_type_label.grid(row=1, column=0, padx=5, pady=5)
        self.column_type_entry = tk.Entry(self.add_column_window)
        self.column_type_entry.grid(row=1, column=1, padx=5, pady=5)

        # Save button to add the new column
        save_button = tk.Button(self.add_column_window, text="Save", command=lambda: self.save_new_column(table_name))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def save_new_column(self, table_name):
        # Get column name and type from entry fields
        column_name = self.column_name_entry.get()
        column_type = self.column_type_entry.get()

        # Add the new column to the table
        try:
            self.cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            self.connection.commit()
            self.add_column_window.destroy()
            self.fetch_table_details()
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def delete_column(self):
        # Get table name from entry field
        table_name = self.table_name_entry.get()

        # Create a new window for deleting a column
        self.delete_column_window = tk.Toplevel(self)
        self.delete_column_window.title("Delete Column")

        # Dropdown menu to select a column for deletion
        self.column_to_delete_label = tk.Label(self.delete_column_window, text="Select Column to Delete:")
        self.column_to_delete_label.pack()

        column_names = [column[1] for column in self.table_columns]
        self.column_to_delete_var = tk.StringVar(self.delete_column_window)
        self.column_to_delete_var.set(column_names[0])
        self.column_to_delete_dropdown = ttk.OptionMenu(self.delete_column_window, self.column_to_delete_var, *column_names)
        self.column_to_delete_dropdown.pack(pady=10)

        # Save button to delete the selected column
        save_button = tk.Button(self.delete_column_window, text="Save", command=lambda: self.delete_selected_column(table_name))
        save_button.pack(pady=10)

    def delete_selected_column(self, table_name):
        # Get the selected column name
        column_to_delete = self.column_to_delete_var.get()

        # Delete the selected column from the table
        try:
            self.cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_to_delete}")
            self.connection.commit()
            self.delete_column_window.destroy()
            self.fetch_table_details()
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def save_changes(self):
        # Display a confirmation message
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to save the changes?")
        if confirmation:
            # Changes will be saved only if the user confirms

            # Get the table name from the entry field
            table_name = self.table_name_entry.get()

            # The changes have already been committed when adding or deleting columns,
            # so there's no need for additional action here
            messagebox.showinfo("Success", "Changes saved successfully!")
        else:
            # If the user cancels the confirmation, display a message
            messagebox.showinfo("Canceled", "Changes not saved.")
    def populate_table_dropdown(self):
        # Fetch table names from SQLite database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in self.cursor.fetchall()]
        # Insert table names into the dropdown
        self.table_name_entry['values'] = tables
if __name__ == "__main__":
    root = tk.Tk()
    alter_page = AlterPage(root)
    alter_page.pack(fill="both", expand=True)
    root.mainloop()
