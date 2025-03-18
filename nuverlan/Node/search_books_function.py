```python
class Library:
    def __init__(self):
        self.books = [
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
            {"title": "1984", "author": "George Orwell"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
            {"title": "Pride and Prejudice", "author": "Jane Austen"},
            {"title": "The Catcher in the Rye", "author": "J.D. Salinger"}
        ]

    def search_books(self, keyword):
        results = []
        for book in self.books:
            if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower():
                results.append(book)
        return results

# Example Usage
library = Library()
search_results = library.search_books("Orwell")
print(search_results)
```