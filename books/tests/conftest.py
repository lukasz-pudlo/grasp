import pytest
from books.factories import PublishingHouseFactory


@pytest.fixture
def publishing_houses():
    return PublishingHouseFactory.create_batch(50)
