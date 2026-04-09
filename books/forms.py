from django import forms
from books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "authors", "edition", "status",)


class BookAddForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "edition", "status", "languages",)
