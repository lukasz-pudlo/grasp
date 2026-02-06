from django_tables2 import tables

from .models import Book


class BookTable(tables.Table):
    class Meta:
        model = Book
        fields = ('title', 'edition', 'status')
