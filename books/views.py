from django.shortcuts import get_object_or_404, render

from .models import Book


def book_list(request):
    books = Book.objects.all()

    return render(
        request,
        'books/list.html',
        {'books': books}
    )


def book_detail(request, id):
    book = get_object_or_404(
        Book,
        id=id
    )

    return render(
        request,
        'books/detail.html',
        {'book': book}
    )
