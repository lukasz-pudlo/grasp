from django.contrib import admin

from .models import Book, Author, Publication, PublishingHouse


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'reader',
                    'created', 'updated', 'status']
    list_filter = ['status', 'reader', 'created', 'updated']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['title', 'status']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'created', 'updated']
    list_filter = ['last_name', 'created', 'updated']
    search_fields = ['last_name']
    ordering = ['last_name']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['author', 'book', 'publisher', 'created', 'updated']
    list_filter = ['author', 'book', 'publisher']
    search_fields = ['author', 'book', 'publisher']
    ordering = ['author']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'established', 'created', 'updated']
    list_filter = ['name']
    search_fields = ['name', 'location']
    ordering = ['name']
    show_facets = admin.ShowFacets.ALWAYS
