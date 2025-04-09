import json
from datetime import datetime, timedelta
from book import Book

class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.borrowed_books = {}
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
