from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Book
from .filters import BookFilter


@login_required
def book_list(request):
    book_filter = BookFilter(
        request.GET,
        queryset=Book.objects.filter(
            reader=request.user).prefetch_related("authors", "languages")
    )

    if request.htmx:
        return render(request, "books/partials/book-container.html", {"filter": book_filter})
    return render(
        request,
        "books/list.html",
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
        "books/detail.html",
        {"book": book}
    )
