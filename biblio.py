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

    def remove_book(self, book):
        self.books.remove(book)
        self.save_books_to_file()
        messagebox.showinfo("Success", "Book removed from the library!")

    def update_book(self, book, new_title, new_author, availability):
        book.title = new_title
        book.author = new_author
        book.available = availability
        self.save_books_to_file()
        messagebox.showinfo("Success", "Book updated!")

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

        self.title_label = tk.Label(
            root, text="Library Management", font=("Arial", 18, "bold"))
        self.title_label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack()

        self.add_button = tk.Button(
            button_frame, text="Add Book", command=self.open_add_book_window, font=("Arial", 12))
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_frame = tk.Frame(root)
        self.search_frame.pack(pady=10)

        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 12))
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_label = tk.Label(
            self.search_frame, text="Search:", font=("Arial", 12))
        self.search_label.grid(row=0, column=0, padx=5)

        self.search_button = tk.Button(
            self.search_frame, text="Search Books", command=self.search_books, font=("Arial", 12))
        self.search_button.grid(row=0, column=2, padx=5)

        self.result_label = tk.Label(
            root, text="Search Results:", font=("Arial", 14, "bold"))
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
            root, text="Show Library", command=self.show_library, font=("Arial", 12))
        self.show_library_button.pack(pady=10)

        self.book_count_label = tk.Label(
            root, text=f"Total Books: {len(self.library.books)}", font=("Arial", 12))
        self.book_count_label.pack()

    def open_add_book_window(self):
        title = simpledialog.askstring(
            "New Book", "Enter the book title:", parent=self.root)
        if title:
            author = simpledialog.askstring(
                "New Book", "Enter the book author:", parent=self.root)
            if author:
                self.library.add_book(title, author)
                self.book_count_label.config(
                    text=f"Total Books: {len(self.library.books)}")

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

        title_label = tk.Label(edit_window, text="Title:", font=("Arial", 12))
        title_label.pack()

        title_entry = tk.Entry(edit_window, font=("Arial", 12))
        title_entry.insert(tk.END, title)
        title_entry.pack()

        author_label = tk.Label(
            edit_window, text="Author:", font=("Arial", 12))
        author_label.pack()

        author_entry = tk.Entry(edit_window, font=("Arial", 12))
        author_entry.insert(tk.END, author)
        author_entry.pack()

        availability_label = tk.Label(
            edit_window, text="Availability:", font=("Arial", 12))
        availability_label.pack()

        availability_entry = tk.Entry(edit_window, font=("Arial", 12))
        availability_entry.insert(tk.END, availability)
        availability_entry.pack()

        delete_button = tk.Button(edit_window, text="Delete Book", command=lambda: self.delete_book(
            selected_item, edit_window), font=("Arial", 12), bg="red", fg="white")
        delete_button.pack(pady=5)

        save_button = tk.Button(edit_window, text="Save",
                                command=lambda: self.update_book(selected_item, title_entry.get(), author_entry.get(),
                                                                 availability_entry.get(), edit_window), font=("Arial", 12))
        save_button.pack()

    def delete_book(self, item, edit_window):
        self.result_table.delete(item)
        messagebox.showinfo("Success", "Book deleted!")
        self.library.remove_book(item)
        edit_window.destroy()

    def update_book(self, item, new_title, new_author, availability, edit_window):
        if new_title.strip() == "" or new_author.strip() == "":
            messagebox.showerror("Error", "Title and author cannot be empty!")
        else:
            selected_item = self.result_table.selection()[0]
            book_values = self.result_table.item(selected_item)['values']
            title = book_values[0]
            author = book_values[1]
            availability = book_values[2]

            book = Book(title, author, availability)
            self.library.update_book(book, new_title, new_author, availability)
            self.result_table.set(item, "Title", new_title)
            self.result_table.set(item, "Author", new_author)
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
