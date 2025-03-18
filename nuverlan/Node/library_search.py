```python
class Library:
    def __init__(self):
        self.books = [
            {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
            {"title": "1984", "author": "George Orwell"},
            {"title": "Pride and Prejudice", "author": "Jane Austen"},
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
            {"title": "Moby-Dick", "author": "Herman Melville"}
        ]

    def search_books(self, search_term, by='title'):
        results = []
        if by not in ['title', 'author']:
            raise ValueError("Search 'by' must be either 'title' or 'author'")
        
        for book in self.books:
            if search_term.lower() in book[by].lower():
                results.append(book)
        return results

# Example usage:
# library = Library()
# print(library.search_books("Scott", by='author'))
# print(library.search_books("Pride", by='title'))
```