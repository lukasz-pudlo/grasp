import pytest
from books.models import PublishingHouse, Book


@pytest.mark.django_db
def test_queryset_poland_method(publishing_houses):
    qs = PublishingHouse.from_country.poland()
    assert qs.count() > 0
    assert all(
        [publishing_house.country == "PL" for publishing_house in qs]
    )


@pytest.mark.django_db
def test_queryset_uk_method(publishing_houses):
    qs = PublishingHouse.from_country.uk()
    assert qs.count() > 0
    assert all(
        [publishing_house.country == "UK" for publishing_house in qs]
    )


@pytest.mark.django_db
def test_book_read_manager(user_books, client):
    qs = Book.read.all()

    assert qs.count() > 0
    assert all(
        [book.status == "RD" for book in qs]
    )
