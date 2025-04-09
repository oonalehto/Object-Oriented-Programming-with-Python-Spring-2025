import json
from datetime import datetime, timedelta

# Book Class
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

# User Base Class
class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def view_books(self, library):
        print(f"Kirjastossa on {len(library.books)} kirjaa. Käytä hakutoimintoa nähdäksesi ne.")

# Librarian Class
class Librarian(User):
    def add_book(self, library, book):
        library.books.append(book)
        library.save_data()
        print(f"Book '{book.title}' added to the library.")

    def remove_book(self, library, book):
        if book in library.books:
            library.books.remove(book)
            library.save_data()
            print(f"Book '{book.title}' removed from the library.")
        else:
            print("Book not found.")

# Borrower Class
class Borrower(User):
    def borrow_book(self, library, book):
        if book in library.books:
            library.books.remove(book)
            due_date = datetime.now() + timedelta(days=14)  # 2 weeks loan period
            library.borrowed_books[self.user_id] = (book, due_date)
            library.save_data()
            print(f"{self.name} borrowed '{book.title}'. Due date: {due_date.strftime('%Y-%m-%d')}")
        else:
            print("Book is not available.")

    def return_book(self, library):
        if self.user_id in library.borrowed_books:
            returned_book, due_date = library.borrowed_books.pop(self.user_id)
            library.books.append(returned_book)
            library.save_data()
            print(f"{self.name} returned '{returned_book.title}'.")
            if datetime.now() > due_date:
                print("Late return! You may have a fine.")
        else:
            print("No book to return.")

# Catalog Class for Searching Books
class Catalog:
    @staticmethod
    def search_by_title(library, title):
        results = [book for book in library.books if title.lower() in book.title.lower()]
        return results if results else "No books found."

    @staticmethod
    def search_by_author(library, author):
        results = [book for book in library.books if author.lower() in book.author.lower()]
        return results if results else "No books found."

# Library Class
class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.borrowed_books = {}  # user_id -> (Book, Due Date)
        self.load_data()

    def add_user(self, user):
        self.users.append(user)
        self.save_data()

    def borrow_book(self, user, book):
        user.borrow_book(self, book)

    def return_book(self, user):
        user.return_book(self)

    def save_data(self):
        data = {
            "books": [(book.title, book.author, book.isbn) for book in self.books],
            "borrowed_books": {user_id: (book.title, book.author, book.isbn, due_date.strftime('%Y-%m-%d'))
                                for user_id, (book, due_date) in self.borrowed_books.items()}
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)
                self.books = [Book(title, author, isbn) for title, author, isbn in data.get("books", [])]
                self.borrowed_books = {
                    int(user_id): (Book(title, author, isbn), datetime.strptime(due_date, '%Y-%m-%d'))
                    for user_id, (title, author, isbn, due_date) in data.get("borrowed_books", {}).items()
                }
        except FileNotFoundError:
            pass

# Interactive search and management
def interactive_search(library):
    while True:
        print("\nValitse toiminto:")
        print("1. Hae kirjaa nimen perusteella")
        print("2. Hae kirjaa kirjailijan perusteella")
        print("3. Näytä kaikki kirjat")
        print("4. Lisää uusi kirja")
        print("5. Poista kirja")
        print("6. Poistu")
        choice = input("Valinta: ")

        if choice == "1":
            title = input("Anna kirjan nimi tai osa siitä: ")
            results = Catalog.search_by_title(library, title)
        elif choice == "2":
            author = input("Anna kirjailijan nimi tai osa siitä: ")
            results = Catalog.search_by_author(library, author)
        elif choice == "3":
            results = library.books if library.books else "Ei kirjoja saatavilla."
        elif choice == "4":
            title = input("Kirjan nimi: ")
            author = input("Kirjailija: ")
            isbn = input("ISBN: ")
            new_book = Book(title, author, isbn)
            library.books.append(new_book)
            library.save_data()
            print(f"Kirja '{title}' lisätty kirjastoon.")
            continue
        elif choice == "5":
            if not library.books:
                print("Kirjastossa ei ole kirjoja.")
                continue
            print("\nKirjat kirjastossa:")
            for idx, book in enumerate(library.books, 1):
                print(f"{idx}. {book}")
            try:
                selection = int(input("Anna poistettavan kirjan numero: "))
                if 1 <= selection <= len(library.books):
                    removed_book = library.books.pop(selection - 1)
                    library.save_data()
                    print(f"Kirja '{removed_book.title}' poistettu.")
                else:
                    print("Virheellinen numero.")
            except ValueError:
                print("Anna kelvollinen numero.")
            continue
        elif choice == "6":
            print("Poistutaan valikosta.")
            break
        else:
            print("Virheellinen valinta.")
            continue

        # Näytä hakutulokset
        if isinstance(results, list):
            if not results:
                print("Ei tuloksia.")
            else:
                print("\nHakutulokset:")
                for book in results:
                    print(f"- {book}")
        else:
            print(results)

# Main Function for Testing
if __name__ == "__main__":
    # Initialize Library
    my_library = Library()
    
    # Create Users
    librarian = Librarian("Alice", 1)
    borrower = Borrower("Bob", 2)
    my_library.add_user(librarian)
    my_library.add_user(borrower)

    # Create Books
    book1 = Book("1984", "George Orwell", "123456")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "789101")
    
    # Add Books to Library
    librarian.add_book(my_library, book1)
    librarian.add_book(my_library, book2)
    
    # Borrow/Return examples
    borrower.borrow_book(my_library, book1)
    borrower.return_book(my_library)

    # Käynnistä interaktiivinen valikko
    interactive_search(my_library)
