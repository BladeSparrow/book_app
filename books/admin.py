from django.contrib import admin
from .models import Book, Author, Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	list_display = ('name', 'website')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'publisher', 'published_date', 'price')
	filter_horizontal = ('authors',)
