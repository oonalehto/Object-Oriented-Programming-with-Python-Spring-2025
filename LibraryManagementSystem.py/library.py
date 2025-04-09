import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime, timedelta
import json

# Book, User, Librarian, Borrower, Catalog, Library classit (sama kuin alkuperäisessä koodissa)
# ... (käytetään samoja luokkia kuin aiemmin – ei toisteta tässä uudelleen tilan säästämiseksi)

# GUI Class
class LibraryApp:
    def __init__(self, root, library):
        self.root = root
        self.library = library
        self.root.title("Kirjastonhallinta")
        self.root.geometry("700x500")

        self.create_widgets()

    def create_widgets(self):
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=10)

        tk.Button(self.root, text="Hae nimellä", command=self.search_by_title).pack()
        tk.Button(self.root, text="Hae kirjailijalla", command=self.search_by_author).pack()

        self.book_list = tk.Listbox(self.root, width=80, height=15)
        self.book_list.pack(pady=10)

        self.populate_book_list()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Lisää kirja", command=self.add_book).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Poista kirja", command=self.remove_book).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Lainaa kirja", command=self.borrow_book).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Palauta kirja", command=self.return_book).grid(row=0, column=3, padx=5)

    def populate_book_list(self, books=None):
        self.book_list.delete(0, tk.END)
        show_books = books if books is not None else self.library.books
        for book in show_books:
            self.book_list.insert(tk.END, str(book))

    def search_by_title(self):
        title = self.search_entry.get()
        results = Catalog.search_by_title(self.library, title)
        self.populate_book_list(results if isinstance(results, list) else [])

    def search_by_author(self):
        author = self.search_entry.get()
        results = Catalog.search_by_author(self.library, author)
        self.populate_book_list(results if isinstance(results, list) else [])

    def add_book(self):
        title = simpledialog.askstring("Lisää kirja", "Kirjan nimi:")
        author = simpledialog.askstring("Lisää kirja", "Kirjailija:")
        isbn = simpledialog.askstring("Lisää kirja", "ISBN:")
        if title and author and isbn:
            book = Book(title, author, isbn)
            self.library.books.append(book)
            self.library.save_data()
            self.populate_book_list()

    def remove_book(self):
        selected = self.book_list.curselection()
        if not selected:
            return
        index = selected[0]
        book = self.library.books[index]
        self.library.books.remove(book)
        self.library.save_data()
        self.populate_book_list()

    def borrow_book(self):
        selected = self.book_list.curselection()
        if not selected:
            return
        try:
            user_id = int(simpledialog.askstring("Lainaa kirja", "Syötä lainaajan ID:"))
        except:
            messagebox.showerror("Virhe", "Virheellinen käyttäjän ID")
            return
        user = next((u for u in self.library.users if u.user_id == user_id and isinstance(u, Borrower)), None)
        if not user:
            messagebox.showerror("Virhe", "Lainaajaa ei löytynyt.")
            return
        book = self.library.books[selected[0]]
        user.borrow_book(self.library, book)
        self.populate_book_list()

    def return_book(self):
        try:
            user_id = int(simpledialog.askstring("Palauta kirja", "Syötä lainaajan ID:"))
        except:
            messagebox.showerror("Virhe", "Virheellinen käyttäjän ID")
            return
        user = next((u for u in self.library.users if u.user_id == user_id and isinstance(u, Borrower)), None)
        if not user:
            messagebox.showerror("Virhe", "Lainaajaa ei löytynyt.")
            return
        user.return_book(self.library)
        self.populate_book_list()

# Pääohjelma
if __name__ == "__main__":
    my_library = Library()
    librarian = Librarian("Alice", 1)
    borrower = Borrower("Bob", 2)
    my_library.add_user(librarian)
    my_library.add_user(borrower)

    # Esimerkkikirjat (jos tyhjä kirjasto)
    if not my_library.books:
        librarian.add_book(my_library, Book("1984", "George Orwell", "123456"))
        librarian.add_book(my_library, Book("To Kill a Mockingbird", "Harper Lee", "789101"))
        librarian.add_book(my_library, Book("Hedelmät", "Hedelmät", "15635656"))

    root = tk.Tk()
    app = LibraryApp(root, my_library)
    root.mainloop()
