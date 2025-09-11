### Update Operation

**Command:**
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)

Nineteen Eighty-Four
# The updated title is stored in the variable `book.title`.