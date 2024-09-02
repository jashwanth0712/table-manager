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

        # Open the first page
        self.open_page("View")

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

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
