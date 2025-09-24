# api/serializers.py
from rest_framework import serializers
from .models import Author, Book
from django.db.models import Prefetch

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model, including custom validation.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validation to ensure the publication year is not in the future.
        """
        import datetime
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model, with nested books.
    This serializer handles the one-to-many relationship
    by including a serialized list of related books.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']