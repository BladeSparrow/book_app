from django.urls import path
from .views import (
    PublisherListCreateAPIView, PublisherDetailAPIView,
    AuthorListCreateAPIView, AuthorDetailAPIView,
    BookListCreateAPIView, BookDetailAPIView
)

urlpatterns = [
    path('publishers/', PublisherListCreateAPIView.as_view(), name='publisher-list'),
    path('publishers/<int:pk>/', PublisherDetailAPIView.as_view(), name='publisher-detail'),

    path('authors/', AuthorListCreateAPIView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),

    path('books/', BookListCreateAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
]
