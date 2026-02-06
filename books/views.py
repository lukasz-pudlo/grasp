from django_tables2 import RequestConfig
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Book
from .tables import BookTable


@login_required
def book_list(request):
    table = BookTable(Book.objects.filter(reader=request.user))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    return render(
        request,
        'books/list.html',
        {'table': table}
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
