import pytest
from books.factories import PublishingHouseFactory, BookFactory, UserFactory


@pytest.fixture
def publishing_houses():
    return PublishingHouseFactory.create_batch(50)


@pytest.fixture
def user_books():
    user = UserFactory()
    return BookFactory.create_batch(100, reader=user)
