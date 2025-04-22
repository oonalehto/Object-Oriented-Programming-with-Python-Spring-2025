
## AUTHORS: Oona, Jonna & Rosa ##
## PROJECT: Object-Oriented-Programming Spring 2025 ##

import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import simpledialog, messagebox

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

# Borrower Class
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

# GUI
def popup_ui(library):
    def search_books():
        query = simpledialog.askstring("Haku", "Anna kirjan nimi tai kirjailija:")
        if not query:
            return
        results_title = Catalog.search_by_title(library, query)
        results_author = Catalog.search_by_author(library, query)
        results = set(results_title if isinstance(results_title, list) else []) | \
                  set(results_author if isinstance(results_author, list) else [])
        if results:
            msg = "\n".join(str(book) for book in results)
        else:
            msg = "Ei tuloksia."
        messagebox.showinfo("Hakutulokset", msg)

    def add_book_popup():
        title = simpledialog.askstring("Lisää kirja", "Kirjan nimi:")
        author = simpledialog.askstring("Lisää kirja", "Kirjailija:")
        isbn = simpledialog.askstring("Lisää kirja", "ISBN:")
        if title and author and isbn:
            new_book = Book(title, author, isbn)
            librarian.add_book(library, new_book)
            messagebox.showinfo("Lisäys", f"Kirja '{title}' lisätty.")
        else:
            messagebox.showwarning("Virhe", "Kaikki kentät ovat pakollisia.")

    def list_books():
        if not library.books:
            messagebox.showinfo("Kirjat", "Ei kirjoja kirjastossa.")
        else:
            msg = "\n".join(str(book) for book in library.books)
            messagebox.showinfo("Kirjat", msg)

    def borrow_book_popup():
        try:
            user_id = int(simpledialog.askstring("Lainaa kirja", "Anna käyttäjän ID:"))
            user = next((u for u in library.users if u.user_id == user_id and isinstance(u, Borrower)), None)
            if not user:
                messagebox.showerror("Virhe", "Lainaajaa ei löytynyt.")
                return
            if not library.books:
                messagebox.showinfo("Ei kirjoja", "Ei kirjoja saatavilla.")
                return
            choices = "\n".join([f"{i+1}. {book}" for i, book in enumerate(library.books)])
            selection = simpledialog.askinteger("Valitse kirja", f"Valitse numero:\n{choices}")
            if selection is None or selection < 1 or selection > len(library.books):
                messagebox.showerror("Virhe", "Virheellinen valinta.")
                return
            book = library.books[selection - 1]
            library.borrow_book(user, book)
            messagebox.showinfo("Lainattu", f"'{book.title}' lainattu käyttäjälle {user.name}.")
        except Exception as e:
            messagebox.showerror("Virhe", f"Tapahtui virhe: {e}")

    def return_book_popup():
        try:
            user_id = int(simpledialog.askstring("Palauta kirja", "Anna käyttäjän ID:"))
            user = next((u for u in library.users if u.user_id == user_id and isinstance(u, Borrower)), None)
            if not user:
                messagebox.showerror("Virhe", "Käyttäjää ei löytynyt.")
                return
            if user_id not in library.borrowed_books:
                messagebox.showinfo("Palautus", "Ei kirjoja palautettavana.")
                return
            library.return_book(user)
            messagebox.showinfo("Palautus", f"{user.name} palautti kirjan.")
        except Exception as e:
            messagebox.showerror("Virhe", f"Tapahtui virhe: {e}")

    def delete_book_popup():
        if not library.books:
            messagebox.showinfo("Poista kirja", "Ei kirjoja poistettavana.")
            return
        choices = "\n".join([f"{i+1}. {book}" for i, book in enumerate(library.books)])
        try:
            selection = simpledialog.askinteger("Poista kirja", f"Valitse poistettava kirja:\n{choices}")
            if selection is None or selection < 1 or selection > len(library.books):
                messagebox.showerror("Virhe", "Virheellinen valinta.")
                return
            removed_book = library.books.pop(selection - 1)
            library.save_data()
            messagebox.showinfo("Poistettu", f"Kirja '{removed_book.title}' poistettu.")
        except Exception as e:
            messagebox.showerror("Virhe", f"Tapahtui virhe: {e}")

    root = tk.Tk()
    root.title("Kirjasto")
    root.geometry("300x350")

    tk.Label(root, text="Valitse toiminto:", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Hae kirjaa", width=25, command=search_books).pack(pady=5)
    tk.Button(root, text="Lisää uusi kirja", width=25, command=add_book_popup).pack(pady=5)
    tk.Button(root, text="Näytä kaikki kirjat", width=25, command=list_books).pack(pady=5)
    tk.Button(root, text="Lainaa kirja", width=25, command=borrow_book_popup).pack(pady=5)
    tk.Button(root, text="Palauta kirja", width=25, command=return_book_popup).pack(pady=5)
    tk.Button(root, text="Poista kirja", width=25, command=delete_book_popup).pack(pady=5)
    tk.Button(root, text="Sulje", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

# Pääohjelma
if __name__ == "__main__":
    my_library = Library()

    # Käyttäjät
    librarian = Librarian("Alice", 1)
    borrower = Borrower("Bob", 2)
    my_library.add_user(librarian)
    my_library.add_user(borrower)

    # Esimerkkikirjat
    book1 = Book("1984", "George Orwell", "123456")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "789101")
    book3 = Book("Hedelmät", "Hedelmät", "15635656")

    librarian.add_book(my_library, book1)
    librarian.add_book(my_library, book2)
    librarian.add_book(my_library, book3)

    borrower.borrow_book(my_library, book1)
    borrower.return_book(my_library)
    borrower.borrow_book(my_library, book3)

    popup_ui(my_library)
