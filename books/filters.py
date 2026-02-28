import django_filters

from books.models import Book


class BookFilter(django_filters.FilterSet):
    book_status = django_filters.ChoiceFilter(
        choices=Book.Status,
        field_name="status",
        lookup_expr="iexact",
        empty_label="All"
    )

    class Meta:
        model = Book
        fields = ("book_status",)
