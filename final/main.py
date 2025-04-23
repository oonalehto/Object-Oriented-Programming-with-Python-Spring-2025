## AUTRHORS: Oona, Jonna & Rosa ##
## PROJECT: Object-Oriented Programming - Spring 2025 ##


from book import Book
from user import Librarian, Borrower
from library import Library
from ui import popup_ui

if __name__ == "__main__":
    my_library = Library()

    # Käyttäjät
    librarian = Librarian("Tuomas", 1)
    borrower = Borrower("Oona", 2)
    borrower1 = Borrower("Jonna", 3)
    borrower2 = Borrower("Rosa", 4)
    
    my_library.add_user(librarian)
    my_library.add_user(borrower)
    my_library.add_user(borrower1)
    my_library.add_user(borrower2)

    # Run GUI
    popup_ui(my_library, librarian, borrower)
