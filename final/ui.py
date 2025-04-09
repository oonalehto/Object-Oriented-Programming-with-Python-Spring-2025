import tkinter as tk
from tkinter import simpledialog, messagebox
from catalog import Catalog

def popup_ui(library, librarian, borrower):
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
