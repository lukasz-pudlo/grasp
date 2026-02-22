from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Book


@login_required
def book_list(request):
    books = Book.objects.filter(reader=request.user)

    return render(
        request,
        'books/list.html',
        {'books': books}
    )


@login_required
def book_detail(request, id):
    book = get_object_or_404(
        Book,
        id=id,
        reader=request.user
    )

    return render(
        request,
        'books/detail.html',
        {'book': book}
    )
