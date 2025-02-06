# library.py (Main module)
from books import Book
from members import Member
from transactions import Transaction
from database import Database

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []  # List of books in the library
        self.members = []  # List of registered members
        self.transactions = []  # List of book lending transactions
        self.database = Database()
        self.load_data()

    def load_data(self):
        self.books = self.database.load_books()
        self.members = self.database.load_members()
        self.transactions = self.database.load_transactions()

    def save_data(self):
        self.database.save_books(self.books)
        self.database.save_members(self.members)
        self.database.save_transactions(self.transactions)

    def add_book(self, book):
        if isinstance(book, Book):  # Objects passed as function arguments
            self.books.append(book)
            self.save_data()

    def register_member(self, member):
        if isinstance(member, Member):
            self.members.append(member)
            self.save_data()

    def lend_book(self, book_title, member_id):
        for book in self.books:
            if book.title == book_title and book.is_available:
                for member in self.members:
                    if member.member_id == member_id:
                        member.borrow_book(book)
                        transaction = Transaction(member, book, "borrowed")
                        self.transactions.append(transaction)
                        self.save_data()
                        return f"{book_title} has been borrowed by {member.name}."
        return "Book not available or member not found."

    def return_book(self, book_title, member_id):
        for member in self.members:
            if member.member_id == member_id:
                result = member.return_book(book_title)
                if "returned" in result:
                    for book in self.books:
                        if book.title == book_title:
                            transaction = Transaction(member, book, "returned")
                            self.transactions.append(transaction)
                            self.save_data()
                            break
                return result
        return "Member not found."

    def list_books(self):
        return [str(book) for book in self.books]

    def list_members(self):
        return [str(member) for member in self.members]

    def list_transactions(self):
        return [str(transaction) for transaction in self.transactions]

# database.py (Module for handling data storage)
import json

class Database:
    def load_books(self):
        try:
            with open("data/books.json", "r") as file:
                return [Book(**book) for book in json.load(file)]
        except FileNotFoundError:
            return []

    def save_books(self, books):
        with open("data/books.json", "w") as file:
            json.dump([book.__dict__ for book in books], file)

    def load_members(self):
        try:
            with open("data/members.json", "r") as file:
                return [Member(**member) for member in json.load(file)]
        except FileNotFoundError:
            return []

    def save_members(self, members):
        with open("data/members.json", "w") as file:
            json.dump([member.__dict__ for member in members], file)

    def load_transactions(self):
        try:
            with open("data/transactions.json", "r") as file:
                return [Transaction(**transaction) for transaction in json.load(file)]
        except FileNotFoundError:
            return []

    def save_transactions(self, transactions):
        with open("data/transactions.json", "w") as file:
            json.dump([transaction.__dict__ for transaction in transactions], file)

# books.py (Module for book management)
class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} ({self.genre})"

# members.py (Module for member management)
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # List data structure

    def borrow_book(self, book):
        if book.is_available:
            self.borrowed_books.append(book)
            book.is_available = False

    def return_book(self, book_title):
        for book in self.borrowed_books:
            if book.title == book_title:
                book.is_available = True
                self.borrowed_books.remove(book)
                return f"{book_title} has been returned."
        return "Book not found in borrowed list."

    def __str__(self):
        return f"Member {self.name}, ID: {self.member_id}"

# transactions.py (Module for transaction management)
from datetime import datetime

class Transaction:
    def __init__(self, member, book, action):
        self.member = member
        self.book = book
        self.action = action
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.timestamp}: {self.member.name} {self.action} '{self.book.title}'"
