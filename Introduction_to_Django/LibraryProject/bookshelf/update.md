### Update Operation

**Command:**
```python
book_to_update = Book.objects.get(title="1984")
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()
print(book_to_update.title)

Nineteen Eighty-Four
# The updated title is stored in the variable `book_to_update.title`.