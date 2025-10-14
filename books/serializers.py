from rest_framework import serializers
from .models import Book, Author, Publisher

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'website']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio']

class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(), source='publisher', write_only=True
    )
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all(), source='authors', write_only=True
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'publisher', 'publisher_id',
            'authors', 'author_ids', 'published_date', 'isbn', 'price'
        ]
