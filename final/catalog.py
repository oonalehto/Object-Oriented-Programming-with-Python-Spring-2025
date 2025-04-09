class Catalog:
    @staticmethod
    def search_by_title(library, title):
        results = [book for book in library.books if title.lower() in book.title.lower()]
        return results if results else "No books found."

    @staticmethod
    def search_by_author(library, author):
        results = [book for book in library.books if author.lower() in book.author.lower()]
        return results if results else "No books found."
