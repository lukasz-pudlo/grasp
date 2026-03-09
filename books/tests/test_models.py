import pytest
from django.urls import reverse
from books.models import PublishingHouse


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
    user = user_books[0].reader
    client.force_login(user)

    response = client.get(reverse('books:book-list'))
    print(response)
