from book import Book
from user import Librarian, Borrower
from library import Library
from ui import popup_ui

if __name__ == "__main__":
    my_library = Library()

    # Create users
    librarian = Librarian("Alice", 1)
    borrower = Borrower("Bob", 2)
    my_library.add_user(librarian)
    my_library.add_user(borrower)

    # Create books and add them
    book1 = Book("Hedelmät", "Hedelmät", "15635656")

    librarian.add_book(my_library, book1)

    # Simulate borrowing and returning
    borrower.borrow_book(my_library, book1)
    borrower.return_book(my_library)
    borrower.borrow_book(my_library, book1)

    # Run GUI
    popup_ui(my_library, librarian, borrower)
