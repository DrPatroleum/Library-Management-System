# Library-Management-System
This is a simple library management system implemented using Tkinter, a Python GUI toolkit. The application allows users to manage a collection of books, including adding new books, searching for books, editing book details, and displaying the library's inventory.

## Features

- Add Book: Users can add new books to the library by entering the book's title and author.
- Search Books: Users can search for books in the library by entering a keyword. The application will display the search results, including the title, author, and availability of each book.
- Edit Book Details: Users can double-click on a book in the search results to edit its title, author, and availability. The changes are saved automatically.
- Show Library: Users can view the complete inventory of the library, including all books sorted alphabetically by title.
- Data Persistence: The application loads the book data from an ODS file ("library.ods") on startup and saves any changes back to the file.

## Usage

1. Launch the application.
2. Click the "Add Book" button to add a new book to the library. Enter the title and author of the book in the prompted dialog boxes.
3. Use the "Search" field to enter a keyword and click the "Search Books" button to find books matching the keyword. The search results will be displayed in the table.
4. Double-click on a book in the search results to edit its details. In the edit window, modify the title, author, or availability and click "Save" to apply the changes.
5. Click the "Show Library" button to open a new window displaying the entire library inventory.
6. Close the application window to exit the program. The book data will be automatically saved to the "library.ods" file.

Note: Make sure to have the necessary dependencies installed, including pyexcel_ods3 and tkinter.


## License
This library management system is released under the MIT License. See the LICENSE file for more information.

## Contact
Created by [@DrPatroleum](https://github.com/DrPatroleum) - feel free to contact me!
