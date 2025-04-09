from datetime import datetime, timedelta

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def view_books(self, library):
        print(f"Kirjastossa on {len(library.books)} kirjaa. Käytä hakutoimintoa nähdäksesi ne.")

class Librarian(User):
    def add_book(self, library, book):
        library.books.append(book)
        library.save_data()
        print(f"Book '{book.title}' added to the library.")

class Borrower(User):
    def borrow_book(self, library, book):
        if book in library.books:
            library.books.remove(book)
            due_date = datetime.now() + timedelta(days=14)
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
