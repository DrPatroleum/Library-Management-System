import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import pyexcel_ods3 as pe


class Book:
    def __init__(self, title, author, available):
        self.title = title
        self.author = author
        self.available = available


class Library:
    def __init__(self):
        self.books = []
        self.load_books_from_file()

    def load_books_from_file(self):
        try:
            data = pe.get_data("library.ods")
            sheet = data["Sheet1"]
            for row in sheet:
                if len(row) >= 3:
                    title = row[0]
                    author = row[1]
                    available = row[2]
                    book = Book(title, author, available)
                    self.books.append(book)
        except Exception as e:
            messagebox.showerror("Error", f"Error while reading the file: {e}")

    def save_books_to_file(self):
        data = [["Title", "Author", "Availability"]]
        for book in self.books:
            data.append([book.title, book.author, book.available])
        try:
            pe.save_data("library.ods", {"Sheet1": data})
        except Exception as e:
            messagebox.showerror("Error", f"Error while saving the file: {e}")

    def add_book(self, title, author):
        book = Book(title, author, "Available")
        self.books.append(book)
        self.save_books_to_file()
        messagebox.showinfo("Success", "Book added to the library!")

    def search_books(self, keyword):
        found_books = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                found_books.append(book)
        return found_books


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.library = Library()

        self.title_label = tk.Label(root, text="Library Management")
        self.title_label.pack()

        self.add_button = tk.Button(
            root, text="Add Book", command=self.open_add_book_window)
        self.add_button.pack(pady=5)

        self.search_frame = tk.Frame(root)
        self.search_frame.pack(pady=10)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_label = tk.Label(self.search_frame, text="Search:")
        self.search_label.grid(row=0, column=0, padx=5)

        self.search_button = tk.Button(
            root, text="Search Books", command=self.search_books)
        self.search_button.pack(pady=5)

        self.result_label = tk.Label(root, text="Search Results:")
        self.result_label.pack()

        self.result_count_label = tk.Label(root, text="")
        self.result_count_label.pack()

        self.result_table = ttk.Treeview(root, columns=(
            "Title", "Author", "Availability"), show="headings")
        self.result_table.heading("Title", text="Title")
        self.result_table.heading("Author", text="Author")
        self.result_table.heading("Availability", text="Availability")
        self.result_table.pack()

        self.result_table.bind("<Double-1>", self.edit_book)

        self.show_library_button = tk.Button(
            root, text="Show Library", command=self.show_library)
        self.show_library_button.pack(pady=10)

    def open_add_book_window(self):
        title = simpledialog.askstring("New Book", "Enter the book title:")
        if title:
            author = simpledialog.askstring(
                "New Book", "Enter the book author:")
            if author:
                self.library.add_book(title, author)

    def search_books(self):
        keyword = self.search_entry.get()
        if keyword:
            found_books = self.library.search_books(keyword)
            self.display_search_results(found_books)
        else:
            self.clear_search_results()

    def display_search_results(self, books):
        self.clear_search_results()
        self.result_count_label.config(
            text=f"Number of results found: {len(books)}")
        for book in books:
            self.result_table.insert("", tk.END, values=(
                book.title, book.author, book.available))

    def clear_search_results(self):
        self.result_table.delete(*self.result_table.get_children())
        self.result_count_label.config(text="")

    def edit_book(self, event):
        selected_item = self.result_table.selection()[0]
        book_values = self.result_table.item(selected_item)['values']
        title = book_values[0]
        author = book_values[1]
        availability = book_values[2]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Book")

        title_label = tk.Label(edit_window, text="Title:")
        title_label.pack()

        title_entry = tk.Entry(edit_window)
        title_entry.insert(tk.END, title)
        title_entry.pack()

        author_label = tk.Label(edit_window, text="Author:")
        author_label.pack()

        author_entry = tk.Entry(edit_window)
        author_entry.insert(tk.END, author)
        author_entry.pack()

        availability_label = tk.Label(edit_window, text="Availability:")
        availability_label.pack()

        availability_entry = tk.Entry(edit_window)
        availability_entry.insert(tk.END, availability)
        availability_entry.pack()

        save_button = tk.Button(edit_window, text="Save",
                                command=lambda: self.update_book(selected_item, title_entry.get(), author_entry.get(),
                                                                 availability_entry.get(), edit_window))
        save_button.pack()

    def update_book(self, item, new_title, new_author, availability, edit_window):
        self.result_table.item(item, values=(
            new_title, new_author, availability))
        messagebox.showinfo("Success", "Book updated!")
        self.library.save_books_to_file()
        edit_window.destroy()

    def show_library(self):
        library_window = tk.Toplevel(self.root)
        library_window.title("Library")

        library_table = ttk.Treeview(library_window, columns=(
            "Title", "Author", "Availability"), show="headings")
        library_table.heading("Title", text="Title")
        library_table.heading("Author", text="Author")
        library_table.heading("Availability", text="Availability")
        library_table.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            library_window, orient="vertical", command=library_table.yview)
        scrollbar.pack(side="right", fill="y")

        library_table.configure(yscrollcommand=scrollbar.set)

        books_sorted = sorted(self.library.books,
                              key=lambda book: book.title.lower())

        for index, book in enumerate(books_sorted, start=1):
            library_table.insert("", tk.END, values=(
                book.title, book.author, book.available))

        library_table.column("#0", width=50)
        library_table.heading("#0", text="ID")
        for i, book in enumerate(library_table.get_children(), start=1):
            library_table.set(book, "#0", i)


root = tk.Tk()
root.title("Home Library")

app = LibraryApp(root)
root.mainloop()
