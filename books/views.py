from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Book
from .filters import BookFilter


@login_required
def book_list(request):
    book_filter = BookFilter(
        request.GET,
        queryset=Book.objects.filter(
            reader=request.user).prefetch_related("authors", "languages", "publications")
    )

    if request.htmx:
        return render(request, "books.html#book-container", {"filter": book_filter})
    return render(
        request,
        "books.html",
        {"filter": book_filter}
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
        "books.html#book-detail",
        {"book": book}
    )
