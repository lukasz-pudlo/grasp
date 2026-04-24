import random

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from books.models import Book, Fragment, Sentence, Word
from books.filters import BookFilter
from books.forms import BookForm, BookAddForm


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
def book_detail(request, pk):
    book = get_object_or_404(
        Book,
        pk=pk,
        reader=request.user
    )

    fragments = Fragment.objects.filter(book=book)

    return render(
        request,
        "book_detail.html",
        {
            "book": book,
            "fragments": fragments
        }
    )


@login_required
def book_edit(request, pk):
    book = get_object_or_404(
        Book,
        pk=pk,
        reader=request.user
    )
    form = BookForm(instance=book)

    context = {
        "book": book,
        "form": form
    }

    return render(
        request,
        "books.html#book-edit",
        context
    )


def book_edit_submit(request, pk):
    book = get_object_or_404(
        Book,
        pk=pk,
        reader=request.user
    )

    context = {
        "book": book
    }

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        else:
            return render(request, "books.html#book-edit", context)
    return render(request, "books.html#book-row", context)


def book_add(request):
    context = {
        "form": BookAddForm()
    }

    return render(request, "books.html#book-add", context)


def book_add_submit(request):
    context = {}
    form = BookAddForm(request.POST)
    context["form"] = form
    if form.is_valid():
        book = form.save(commit=False)
        user = request.user
        book.reader = user
        context["book"] = form.save()
    else:
        return render(request, "books.html#book-add", context)
    return render(request, "books.html#book-row", context)


def book_add_cancel(request):
    return HttpResponse()


def fragment_detail(request, pk):
    fragment = get_object_or_404(
        Fragment,
        pk=pk
    )

    return render(
        request,
        "book_detail.html#fragment-detail",
        {
            "fragment": fragment
        }
    )


def sentence_list(request, pk):
    fragment = get_object_or_404(Fragment, pk=pk)
    sentences = Sentence.objects.filter(
        fragment=fragment
    )

    return render(
        request,
        "book_detail.html#sentence-list",
        {
            "sentences": sentences,
            "fragment": fragment
        }
    )


def word_list(request, pk):
    sentence = get_object_or_404(Sentence, pk=pk)
    words = Word.objects.filter(
        sentence=sentence
    )

    return render(
        request,
        "book_detail.html#word-list",
        {
            "sentence": sentence,
            "words": words
        }
    )


def learn_words(request, pk, round):
    sentence = get_object_or_404(Sentence, pk=pk)
    words = Word.objects.filter(
        sentence=sentence)

    learn_words = []

    # We have the sentence and we have the word.
    # Choose a number of random words that will have
    # all but the first letter removed.
    word_list = list(words)
    words_to_truncate = random.sample(word_list, int(round))
    for word in words:
        if word in words_to_truncate:
            print(f"Word {word.text} identified to be truncated")
            learn_words.append(word.text[0])
        else:
            print(f"Word {word.text} to be added in full")
            learn_words.append(word.text)
    print(f"learn_words after the loop: {learn_words}")

    zipped_words = zip(learn_words, words)

    return render(
        request,
        "book_detail.html#learn_words",
        {
            "zipped_words": zipped_words,
            "sentence": sentence,
            "round": int(round) + 1
        }
    )


def reveal_word(request, round, pk):
    word = get_object_or_404(Word, pk=pk)

    return render(
        request,
        "book_detail.html#reveal_word",
        {
            "word": word,
            "round": round
        }
    )
