# api/test_views.py

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Author, Book

User = get_user_model()

class BookAPITests(APITestCase):
    
    def setUp(self):
        """
        Set up a user and some initial data for testing.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(name='J.R.R. Tolkien')
        self.book1 = Book.objects.create(
            title='The Hobbit', 
            publication_year=1937, 
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='The Lord of the Rings', 
            publication_year=1954, 
            author=self.author
        )
        # Use reverse to generate URLs from their names
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail')
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update')
        self.book_delete_url = reverse('book-delete')

    def test_book_update_view_authenticated(self):
        """
        Ensure authenticated users can update a book.
        """
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title', 'publication_year': 1955, 'author': self.author.pk}
        # Correctly reverse the URL with the book's primary key
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        
    def test_book_delete_view_authenticated(self):
        """
        Ensure authenticated users can delete a book.
        """
        self.client.force_authenticate(user=self.user)
        # Correctly reverse the URL with the book's primary key
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
        
    def test_book_detail_view_authenticated(self):
        """
        Ensure authenticated users can retrieve a single book.
        """
        self.client.force_authenticate(user=self.user)
        # Correctly reverse the URL with the book's primary key
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')