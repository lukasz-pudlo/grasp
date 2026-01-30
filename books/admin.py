from django.contrib import admin

from .models import Book, Author, Publication, PublishingHouse


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'reader',
                    'created', 'updated', 'status']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'created', 'updated']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['author', 'book', 'publisher', 'created', 'updated']


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'established', 'created', 'updated']
