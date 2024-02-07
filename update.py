import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class UpdatePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.page_name = "Update"
  
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

        # Primary key entry
        self.primary_key_label = tk.Label(self, text="Enter id of the row you want to update:")
        self.primary_key_label.pack()
        self.primary_key_entry = tk.Entry(self)
        self.primary_key_entry.pack(pady=5)

       

        # Frame to display data for update
        self.update_frame = tk.Frame(self)
        self.update_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Button to update data
        self.update_button = tk.Button(self, text="Update Data", command=self.update_data)
        self.update_button.pack(pady=10)

        # Store table details fetched from the database
        self.table_columns = []

        # Initialize database connection
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.populate_table_dropdown()

    def fetch_all_table_details(self):
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


    def fetch_table_details(self):
        self.fetch_all_table_details()
        # Clear existing data for update
        for widget in self.update_frame.winfo_children():
            widget.destroy()

        # Get table name from entry field
        table_name = self.table_name_entry.get()
        # Fetch table details (columns) from the database
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            self.table_columns = self.cursor.fetchall()

            
            # Display entry fields for data update
            for column in self.table_columns:
                column_label = tk.Label(self.update_frame, text=f"{column[1]}:")
                column_label.grid(row=self.table_columns.index(column), column=0, padx=5, pady=5)
                entry = tk.Entry(self.update_frame)
                entry.grid(row=self.table_columns.index(column), column=1, padx=5, pady=5)
                setattr(self, f"{column[1]}_entry", entry)  # Store entry widgets dynamically
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def update_data(self):
        # Get table name from entry field
        table_name = self.table_name_entry.get()

        # Get primary key value
        primary_key_value = self.primary_key_entry.get()

        # Prepare update query
        update_query = f"UPDATE {table_name} SET "
        update_data = []

        # Construct the update query dynamically
        for column in self.table_columns:
            column_name = column[1]
            entry_value = getattr(self, f"{column_name}_entry").get()
            if entry_value:
                update_query += f"{column_name} = ?, "
                update_data.append(entry_value)

        # Remove the trailing comma and space from the update query
        update_query = update_query[:-2]

        # Add the condition for the primary key
        update_query += f" WHERE id = ?"
        update_data.append(primary_key_value)

        # Execute the update query
        try:
            self.cursor.execute(update_query, update_data)
            self.connection.commit()
            messagebox.showinfo("Success", "Data updated successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def populate_table_dropdown(self):
        # Fetch table names from SQLite database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in self.cursor.fetchall()]

        # Insert table names into the dropdown
        self.table_name_entry['values'] = tables