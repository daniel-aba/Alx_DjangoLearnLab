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
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

    def test_authenticated_user_can_login(self):
        """
        Ensure a user can log in with correct credentials.
        """
        response = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(response)

    def test_book_list_view_authenticated(self):
        """
        Ensure authenticated users can list books.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_book_list_view_unauthenticated(self):
        """
        Ensure unauthenticated users can list books (read-only access).
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_book_create_view_authenticated(self):
        """
        Ensure authenticated users can create a new book.
        """
        self.client.force_authenticate(user=self.user)
        data = {'title': 'The Silmarillion', 'publication_year': 1977, 'author': self.author.pk}
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title='The Silmarillion').publication_year, 1977)
    
    def test_book_create_view_unauthenticated(self):
        """
        Ensure unauthenticated users cannot create a book.
        """
        data = {'title': 'The Silmarillion', 'publication_year': 1977, 'author': self.author.pk}
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_book_update_view_authenticated(self):
        """
        Ensure authenticated users can update a book.
        """
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title', 'publication_year': 1955, 'author': self.author.pk}
        response = self.client.put(self.book_update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        
    def test_book_delete_view_authenticated(self):
        """
        Ensure authenticated users can delete a book.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
        
    def test_filter_by_title(self):
        """
        Ensure filtering by title works correctly.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.book_list_url, {'title': 'The Hobbit'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')
        
    def test_search_by_author_name(self):
        """
        Ensure searching by author name works correctly.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.book_list_url, {'search': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_ordering_by_publication_year(self):
        """
        Ensure ordering by publication year works correctly.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'The Lord of the Rings')
        self.assertEqual(response.data[1]['title'], 'The Hobbit')