from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book, BorrowRecord

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken



class AuthorAPITestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.author_data = {"name": "John Doe", "bio": "A famous author"}
        self.author = Author.objects.create(name="Jane Doe", bio="Another famous author")

    def test_create_author(self):
        response = self.client.post('/Author', self.author_data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.author_data['name'])

    def test_get_authors(self):
        response = self.client.get('/Author')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class BorrowRecordAPITestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", 
            author=self.author, 
            isbn="1234567890123", 
            available_copies=5
        )
        self.borrow_record_data = {"book": self.book.id, "borrowed_by": "User 1"}

    def test_borrow_book(self):
        response = self.client.post('/borrow/', self.borrow_record_data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 4)

    def test_return_book(self):
        borrow_record = BorrowRecord.objects.create(book=self.book, borrowed_by="User 2")
        response = self.client.put(f'/borrow/{borrow_record.id}/return/')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 5)


