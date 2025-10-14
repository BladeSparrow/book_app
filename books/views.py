from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Author, Publisher
from .serializers import BookSerializer, AuthorSerializer, PublisherSerializer
from django.db import IntegrityError

class PublisherListCreateAPIView(APIView):
    def get(self, request):
        qs = Publisher.objects.all()
        serializer = PublisherSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublisherDetailAPIView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Publisher, pk=pk)
        return Response(PublisherSerializer(obj).data)

    def put(self, request, pk):
        obj = get_object_or_404(Publisher, pk=pk)
        serializer = PublisherSerializer(obj, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = get_object_or_404(Publisher, pk=pk)
        serializer = PublisherSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Publisher, pk=pk)
        try:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response(
                {"detail": "Cannot delete publisher because there are books linked to it."},
                status=status.HTTP_400_BAD_REQUEST
            )


class AuthorListCreateAPIView(APIView):
    def get(self, request):
        qs = Author.objects.all()
        serializer = AuthorSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetailAPIView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Author, pk=pk)
        return Response(AuthorSerializer(obj).data)

    def put(self, request, pk):
        obj = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Author, pk=pk)
        if obj.books.exists():
            return Response(
                {"detail": "Cannot delete author because they have books on the site."},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookListCreateAPIView(APIView):
    def get(self, request):
        qs = Book.objects.select_related('publisher').prefetch_related('authors').all()
        serializer = BookSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPIView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Book, pk=pk)
        return Response(BookSerializer(obj).data)

    def put(self, request, pk):
        obj = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(obj, data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Book, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)