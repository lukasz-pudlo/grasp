from django.contrib import admin

from .models import Book, Author, Publication, PublishingHouse, BookLanguage, Country, TextFragment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'edition', 'reader',
                    'created', 'updated', 'status']
    list_filter = ['status', 'edition', 'reader', 'created', 'updated']
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
    list_display = ['author', 'book',
                    'publisher', 'date', 'created', 'updated']
    list_filter = ['author', 'book', 'publisher', 'date']
    search_fields = ['author', 'book', 'publisher', 'date']
    ordering = ['author']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'country',
                    'established', 'created', 'updated']
    list_filter = ['name']
    search_fields = ['name', 'country']
    ordering = ['name']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(BookLanguage)
class BookLanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "language_tag"]
    search_fields = ["name", "language_tag"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(TextFragment)
class TextFragmentAdmin(admin.ModelAdmin):
    list_display = ["book", "text", "created", "updated"]
    search_fields = ["book", "text"]
    show_facets = admin.ShowFacets.ALWAYS
